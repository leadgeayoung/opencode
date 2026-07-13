"""Builder Engine — deterministic state machine for the Builder orchestrator.

No LLM calls. No fuzzy logic. Pure deterministic state transitions,
circuit breaker management, response validation, and state persistence.
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional, Any

import yaml


class StateMachine:
    """Parses state-machine.yaml and provides transition lookups."""

    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(config_dir, "state-machine.yaml")
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._transitions: dict[tuple[str, str], dict] = {}
        for t in data.get("transitions", []):
            key = (t["from"], t["status"])
            self._transitions[key] = {
                "to": t["to"],
                "resets": t.get("resets", []),
                "increments": t.get("increments", []),
            }

        self._counters: dict[str, dict] = {}
        for c in data.get("counters", []):
            self._counters[c["name"]] = {
                "max": c["max"],
                "scope": c.get("scope", "local"),
                "reset_on": c.get("reset_on"),
                "entry_reset": c.get("entry_reset"),
            }

        self._agents: dict[str, list[str]] = {}
        for name, cfg in data.get("agents", {}).items():
            self._agents[name] = cfg["states"]

        self._valid_states = set()
        self._valid_statuses = set()
        for (f, s) in self._transitions:
            self._valid_states.add(f)
            self._valid_states.add(self._transitions[(f, s)]["to"])
            self._valid_statuses.add(s)

    def transition(self, current_state: str, status: str) -> dict:
        """Look up transition. Returns {to, resets, increments} or raises KeyError."""
        key = (current_state, status)
        if key not in self._transitions:
            available = [s for (f, s) in self._transitions if f == current_state]
            raise KeyError(
                f"No transition defined for state='{current_state}' status='{status}'. "
                f"Available statuses: {available}"
            )
        return dict(self._transitions[key])

    def get_agents_for_state(self, state: str) -> list[str]:
        return [name for name, states in self._agents.items() if state in states]

    def get_counter_config(self, name: str) -> Optional[dict]:
        return self._counters.get(name)

    @property
    def all_states(self) -> list[str]:
        return sorted(self._valid_states)


class CircuitBreaker:
    """Counter lifecycle management."""

    def __init__(self, state_machine: StateMachine):
        self._sm = state_machine

    def increment(self, counters: dict, name: str, count: int = 1) -> dict:
        """Increment a counter. Returns {counters, tripped, tripped_at}."""
        cfg = self._sm.get_counter_config(name)
        if cfg is None:
            return {"counters": counters, "tripped": False, "tripped_at": None}

        current = counters.get(name, 0)
        current += count
        counters[name] = current

        tripped = current >= cfg["max"]
        return {
            "counters": dict(counters),
            "tripped": tripped,
            "tripped_at": name if tripped else None,
        }

    def reset_all_on_entry(self, counters: dict, state: str) -> dict:
        """Reset all counters whose entry_reset matches the given state."""
        changed = False
        for name, cfg in self._sm._counters.items():
            if cfg.get("entry_reset") == state:
                if counters.get(name, 0) != 0:
                    counters[name] = 0
                    changed = True
        return {"counters": dict(counters), "changed": changed}

    def global_check(self, counters: dict) -> dict:
        """Check total_system_retries threshold."""
        val = counters.get("total_system_retries", 0)
        max_val = self._sm.get_counter_config("total_system_retries").get("max", 7)
        tripped = val >= max_val
        return {
            "tripped": tripped,
            "current": val,
            "max": max_val,
            "message": (
                f"系统已进行多次跨阶段修复仍未成功 (total_retries={val})。"
                f"为防止陷入死循环，已暂停执行。请人工介入指导方向。"
                if tripped
                else None
            ),
        }

    def apply_transition_effects(self, counters: dict, transition: dict, state: str) -> dict:
        """Apply resets and increments from a transition."""
        counters = dict(counters)
        for name in transition.get("resets", []):
            counters[name] = 0
        for name in transition.get("increments", []):
            counters = self.increment(counters, name)["counters"]
        counters = self.reset_all_on_entry(counters, transition["to"])["counters"]
        return counters


class ResponseValidator:
    """Validate subagent JSON responses against schema + artifact rules."""

    SCHEMA_PATH = "state-schema.json"

    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(config_dir, self.SCHEMA_PATH)
        with open(schema_path, encoding="utf-8") as f:
            self._schema = json.load(f)

    def validate(self, response_str: str) -> dict:
        """
        Validate a subagent response string.

        Returns {valid: bool, errors: list[str]}.
        """
        errors = []

        # Parse JSON
        try:
            data = json.loads(response_str)
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [f"Invalid JSON: {e}"]}

        if not isinstance(data, dict):
            return {"valid": False, "errors": ["Response must be a JSON object"]}

        # Check required fields
        for field in ("status", "summary", "artifacts", "issues"):
            if field not in data:
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return {"valid": False, "errors": errors}

        # Validate status
        valid_statuses = {"ok", "failed", "blocked"}
        if data["status"] not in valid_statuses:
            errors.append(
                f"Invalid status '{data['status']}'. Must be one of {valid_statuses}"
            )

        # Validate summary length
        if len(data.get("summary", "")) > 500:
            errors.append("Summary exceeds 500 characters")

        # Validate artifacts
        if not isinstance(data.get("artifacts"), list):
            errors.append("'artifacts' must be an array")
        else:
            for i, art in enumerate(data["artifacts"]):
                art_errors = self._validate_artifact(art)
                for ae in art_errors:
                    errors.append(f"artifacts[{i}]: {ae}")

        # Validate issues
        if not isinstance(data.get("issues"), list):
            errors.append("'issues' must be an array")
        else:
            valid_severities = {"error", "warning", "info"}
            for i, issue in enumerate(data["issues"]):
                if not isinstance(issue, dict):
                    errors.append(f"issues[{i}]: must be an object")
                    continue
                if issue.get("severity") not in valid_severities:
                    errors.append(
                        f"issues[{i}]: invalid severity '{issue.get('severity')}'"
                    )
                if len(issue.get("message", "")) > 500:
                    errors.append(f"issues[{i}]: message exceeds 500 characters")

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_artifact(self, art: dict) -> list[str]:
        errors = []
        if not isinstance(art, dict):
            return ["must be an object"]

        for required in ("type", "path"):
            if required not in art:
                errors.append(f"missing required field '{required}'")

        if "type" in art:
            valid_types = {"code", "doc", "spec", "log", "research", "test"}
            if art["type"] not in valid_types:
                errors.append(f"invalid type '{art['type']}'")

        if "path" in art:
            if not isinstance(art["path"], str) or not art["path"]:
                errors.append("'path' must be a non-empty string")
            elif art["path"].startswith("/") or art["path"].startswith("\\"):
                errors.append("'path' must be relative, not absolute")

        if "summary" in art and len(art["summary"]) > 200:
            errors.append("'summary' exceeds 200 characters")

        # Reject inline content
        for forbidden in ("content", "body", "data"):
            if forbidden in art:
                errors.append(f"inline '{forbidden}' detected — use path references only")

        return errors


class StateStore:
    """Read/write .opencode/knowledge/state/current.json."""

    DEFAULT_STATE = {
        "workflow_state": "WAIT",
        "circuit_breaker": {
            "outer_loop": 0,
            "debug_attempts": 0,
            "review_attempts": 0,
            "clarify_attempts": 0,
            "total_system_retries": 0,
        },
        "last_updated": "",
    }

    def __init__(self, state_path: Optional[str] = None, schema_dir: Optional[str] = None):
        if state_path is None:
            # Default: project's .opencode/knowledge/state/current.json
            state_path = os.path.join(
                os.getcwd(), ".opencode", "knowledge", "state", "current.json"
            )
        self._state_path = state_path
        if schema_dir is None:
            schema_dir = os.path.dirname(os.path.abspath(__file__))
        self._schema_path = os.path.join(schema_dir, "state-schema.json")

    def load(self) -> dict:
        """Load state from disk. Returns the state dict."""
        if not os.path.exists(self._state_path):
            return self._default()
        try:
            with open(self._state_path, encoding="utf-8") as f:
                data = json.load(f)
            # Ensure all required fields exist
            for key, val in self.DEFAULT_STATE.items():
                if key not in data:
                    data[key] = val
            return data
        except (json.JSONDecodeError, OSError):
            return self._default()

    def save(self, state: dict) -> dict:
        """Save state to disk (with schema validation). Returns {ok, error}."""
        try:
            # Basic validation
            required = {"workflow_state", "circuit_breaker"}
            missing = required - set(state.keys())
            if missing:
                return {"ok": False, "error": f"Missing required fields: {missing}"}

            valid_states = {
                "CLARIFY", "RESEARCH", "DESIGN", "BUILD",
                "POLISH", "DELIVER", "LEARN", "WAIT", "DONE",
            }
            if state["workflow_state"] not in valid_states:
                return {
                    "ok": False,
                    "error": f"Invalid workflow_state '{state['workflow_state']}'",
                }

            state["last_updated"] = datetime.now(timezone.utc).isoformat()

            os.makedirs(os.path.dirname(self._state_path), exist_ok=True)
            with open(self._state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            return {"ok": True, "error": None}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    def _default(self) -> dict:
        return dict(self.DEFAULT_STATE)


class WorkflowRunner:
    """
    Reads workflow.yaml and orchestrates the per-turn workflow.

    Call workflow_step() in a loop with LLM results.
    Engine action steps run automatically.
    LLM action steps return instructions for the LLM to follow.
    """

    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(config_dir, "workflow.yaml")
        with open(path, encoding="utf-8") as f:
            self._wf = yaml.safe_load(f)

        self._turn_steps = self._wf.get("turn", [])
        self._step_idx = -1
        self._context: dict[str, Any] = {}
        self._current_step: Optional[dict] = None
        self._turn_active = False
        self._config_dir = config_dir

    def init(self) -> dict:
        """Run init steps (sync_rules). Returns log of actions."""
        log = []
        for step in self._wf.get("init", []):
            if step["id"] == "sync_rules":
                src = os.path.join(self._config_dir, "rules.yaml")
                tgt = os.path.join(os.getcwd(), "AGENTS.md")
                try:
                    with open(src, encoding="utf-8") as f:
                        content = f.read()
                    with open(tgt, "w", encoding="utf-8") as f:
                        f.write(content)
                    log.append(f"init: wrote rules.yaml → AGENTS.md")
                except OSError as e:
                    log.append(f"init: FAILED rules.yaml → AGENTS.md: {e}")
        return {"action": "init_done", "engine_log": log}

    def start_turn(self, user_message: str, state: dict) -> dict:
        """Start a new turn with a user message. Returns first action."""
        self._context = {"user_message": user_message, "state": state}
        self._step_idx = -1
        self._turn_active = True
        self._engine_log: list[str] = []
        return self._advance()

    def submit(self, data: dict) -> dict:
        """Submit LLM or subagent result for the current step. Returns next action."""
        if not self._turn_active:
            return {"action": "error", "message": "No active turn. Call start_turn first."}

        step = self._current_step
        if step["action"] == "llm":
            llm_value = data.get("value", "")
            status = data.get("status", "")

            # Subagent result: LLM ran task() and got a result
            if status and step.get("task") == "dispatch":
                self._context["subagent_result"] = llm_value
                self._context["subagent_status"] = status
                return self._advance()

            # Normal LLM step result (classify or dispatch prompt)
            self._context[step.get("store", step["id"])] = llm_value
            return self._advance()

        return {"action": "error", "message": f"Step {step['id']} is not an llm step"}

    def _advance(self) -> dict:
        """Move to the next step and return the action."""
        self._step_idx += 1
        if self._step_idx >= len(self._turn_steps):
            self._turn_active = False
            return {"action": "turn_done", "engine_log": self._engine_log}

        step = self._turn_steps[self._step_idx]
        self._current_step = step

        if step["action"] == "engine":
            return self._run_engine_step(step)
        elif step["action"] == "llm":
            return self._prepare_llm_step(step)
        else:
            return {"action": "error", "message": f"Unknown action: {step['action']}"}

    def _run_engine_step(self, step: dict) -> dict:
        """Execute an engine step internally and advance."""
        sid = step["id"]

        if sid == "load_state":
            state = self._context.get("state")
            self._engine_log.append(f"load_state → {state.get('workflow_state', '?')}")
            return self._advance()

        if sid == "branch":
            es = self._context.get("state", {})
            ws = es.get("workflow_state", "")
            if ws in ("WAIT", "DONE"):
                self._engine_log.append(f"branch: {ws} → classify_intent")
                return self._advance()
            else:
                self._engine_log.append(f"branch: {ws} → dispatch")
                while self._step_idx + 1 < len(self._turn_steps):
                    next_step = self._turn_steps[self._step_idx + 1]
                    if next_step["id"] == "dispatch":
                        break
                    self._step_idx += 1
                return self._advance()

        if sid == "transition":
            es = self._context.get("state", {})
            cs = es.get("workflow_state", "?")
            st = self._context.get("classify_intent", self._context.get("subagent_status", "?"))
            log_entry = f"state_transition({cs}, {st})"
            try:
                sm = StateMachine(self._config_dir)
                result = sm.transition(cs, st)
                bk = CircuitBreaker(sm)
                counters = bk.apply_transition_effects(dict(es.get("circuit_breaker", {})), result, cs)
                es["workflow_state"] = result["to"]
                es["circuit_breaker"] = counters
                self._context["state"] = es
                self._engine_log.append(f"{log_entry} → {result['to']}")
            except KeyError as e:
                self._engine_log.append(f"{log_entry} FAILED: {e}")
            return self._advance()

        if sid == "evaluate":
            inp_val = self._context.get("subagent_result", "")
            validator = ResponseValidator(self._config_dir)
            result = validator.validate(inp_val) if isinstance(inp_val, str) else {"valid": False, "errors": ["not a string"]}
            self._context["validation"] = result
            self._engine_log.append(
                f"validate_response → {'valid' if result.get('valid') else 'INVALID: ' + str(result.get('errors', []))}"
            )
            return self._advance()

        if sid == "breaker":
            ss = self._context.get("subagent_status", "")
            if ss in ("failed", "blocked"):
                es = self._context.get("state", {})
                cnt = es.get("circuit_breaker", {})
                sm = StateMachine(self._config_dir)
                bk = CircuitBreaker(sm)
                result = bk.increment(cnt, "total_system_retries")
                es["circuit_breaker"] = result["counters"]
                self._context["state"] = es
                self._engine_log.append(
                    f"breaker_increment(total_system_retries) → {result['counters'].get('total_system_retries')}"
                    f"{' TRIPPED' if result.get('tripped') else ''}"
                )
                if result.get("tripped"):
                    return {"action": "halt", "engine_log": self._engine_log, "message": "total_system_retries threshold reached"}
            else:
                self._engine_log.append("breaker: skipped (status not failed/blocked)")
            return self._advance()

        if sid == "global_check":
            es = self._context.get("state", {})
            cnt = es.get("circuit_breaker", {})
            sm = StateMachine(self._config_dir)
            bk = CircuitBreaker(sm)
            result = bk.global_check(cnt)
            self._engine_log.append(
                f"global_check → {result.get('current')}/{result.get('max')}"
                f"{' TRIPPED' if result.get('tripped') else ''}"
            )
            if result.get("tripped"):
                return {"action": "halt", "message": result.get("message"), "engine_log": self._engine_log}
            return self._advance()

        if sid == "advance":
            es = self._context.get("state", {})
            cs = es.get("workflow_state", "?")
            st = self._context.get("subagent_status", "?") or "?"
            log_entry = f"state_transition({cs}, {st})"
            try:
                sm = StateMachine(self._config_dir)
                result = sm.transition(cs, st)
                bk = CircuitBreaker(sm)
                counters = bk.apply_transition_effects(dict(es.get("circuit_breaker", {})), result, cs)
                es["workflow_state"] = result["to"]
                es["circuit_breaker"] = counters
                self._context["state"] = es
                self._engine_log.append(f"{log_entry} → {result['to']}")
            except KeyError as e:
                self._engine_log.append(f"{log_entry} FAILED: {e}")
            return self._advance()

        self._engine_log.append(f"engine_step: {sid}")
        return self._advance()

    def _prepare_llm_step(self, step: dict) -> dict:
        """Prepare instructions for an LLM action step."""
        task = step.get("task", "")
        if task == "classify":
            return {
                "action": "classify",
                "instruction": (
                    "Classify into ONE intent. "
                    "Valid options: bug, feature, optimization, question, other, satisfied. "
                    "Pick the closest match even if uncertain. "
                    "You may ask ONLY to clarify which intent the user means. "
                    "Do NOT ask about technology, implementation, design, or requirements "
                    "— those are handled by subagents in later stages."
                ),
                "valid_intents": ["bug", "feature", "optimization", "question", "other", "satisfied"],
                "message": self._context.get("user_message", ""),
                "engine_log": self._engine_log,
            }
        if task == "dispatch":
            state = self._context.get("state", {})
            ws = state.get("workflow_state", "")
            sm = StateMachine(self._config_dir)
            agents = sm.get_agents_for_state(ws)
            agent_str = ", ".join(agents) if agents else "general"
            return {
                "action": "dispatch",
                "agent": agent_str,
                "workflow_state": ws,
                "engine_log": self._engine_log,
                "instruction": f"Write a task prompt for the subagent (workflow_state={ws})",
            }
        return {
            "action": "error",
            "message": f"Unknown llm task: {task}",
            "engine_log": self._engine_log,
        }
