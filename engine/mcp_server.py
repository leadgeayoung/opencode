"""MCP stdio server for the Builder Engine.
Protocol: JSON-RPC 2.0 over stdin/stdout.
"""

import json
import sys
import traceback
from pathlib import Path

from builder_engine import StateStore, WorkflowRunner

ENGINE_DIR = Path(__file__).parent
store = StateStore(schema_dir=str(ENGINE_DIR))
runner = WorkflowRunner(str(ENGINE_DIR))
_init_result = runner.init()

TOOLS = [
    {
        "name": "workflow_step",
        "description": "Execute the next step in the Builder workflow. Call in a loop until turn_done.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["init", "result"],
                    "description": "init = start turn, result = return LLM output",
                },
                "value": {
                    "type": "string",
                    "description": "User message (init), or intent/subagent JSON (result)",
                },
                "status": {
                    "type": "string",
                    "description": "Subagent status when returning subagent JSON result",
                },
            },
            "required": ["type"],
        },
    },
]


def handle_initialize(params: dict) -> dict:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "builder-engine", "version": "1.0.0"},
    }


def handle_list_tools() -> dict:
    return {"tools": TOOLS}


def handle_call_tool(name: str, args: dict) -> dict:
    if name != "workflow_step":
        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

    call_type = args.get("type", "init")
    value = args.get("value", "")

    if call_type == "init":
        state = store.load()
        result = runner.start_turn(value, state)
        return {"content": [{"type": "text", "text": json.dumps(result)}]}

    if call_type == "result":
        data = {"value": value}
        status = args.get("status", "")
        if status:
            data["status"] = status
        result = runner.submit(data)
        if result.get("action") == "turn_done" and "state" in runner._context:
            st = runner._context.get("state", {})
            store.save(st)
        if result.get("action") in ("dispatch", "classify", "halt"):
            st = runner._context.get("state", {})
            if st:
                store.save(st)
        return {"content": [{"type": "text", "text": json.dumps(result)}]}

    return {"isError": True, "content": [{"type": "text", "text": f"Unknown type: {call_type}"}]}


def main():
    read_buffer = ""
    request_id_counter = 0
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})
        if method.startswith("notifications/"):
            continue
        result = None
        error = None
        try:
            if method == "initialize":
                result = handle_initialize(params)
            elif method == "tools/list":
                result = handle_list_tools()
            elif method == "tools/call":
                result = handle_call_tool(params["name"], params.get("arguments", {}))
            else:
                error = {"code": -32601, "message": f"Method not found: {method}"}
        except Exception as e:
            error = {"code": -32603, "message": str(e), "data": traceback.format_exc()}
        response = {"jsonrpc": "2.0", "id": msg_id if msg_id is not None else request_id_counter}
        if error:
            response["error"] = error
        else:
            response["result"] = result
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()
        request_id_counter += 1


if __name__ == "__main__":
    main()
