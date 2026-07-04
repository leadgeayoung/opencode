# 12 — Themes & Keybinds

---

# Part A: Theme System (06a-themes)

## Overview

OpenCode ships with **50+ built-in themes**. The theme is set via the top-level `theme` key — **never** `tui.theme`.

```jsonc
// opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "tokyonight"
}
```

The TUI picks the theme on launch. Change at runtime via `Ctrl+X T` (theme list).

## Popular Built-in Themes

| Theme | Notes |
|-------|-------|
| `opencode` | Default OpenCode theme |
| `catppuccin` | Latte, Frappé, Macchiato, Mocha variants |
| `tokyonight` | Night owl blue-based theme |
| `dracula` | Dark vampire theme |
| `nord` | Arctic, bluish pastel |
| `solarized` | Light/dark scientific palette |
| `gruvbox` | Retro groove (dark/light) |
| `onedark` | Atom One Dark |
| `monokai` | High-contrast vibrant |
| `ayu` | Light/mirage/dark variants |
| `github-dark` | GitHub dark mode |
| `github-light` | GitHub light mode |
| `solarized-dark` | Dark variant of solarized |
| `solarized-light` | Light variant of solarized |
| `night-owl` | VS Code Night Owl |
| `palenight` | Material Palenight |
| `material` | Material Design dark |
| `onehalf` | One Half Dark/Light |
| `everforest` | Warm green-tinted |
| `rose-pine` | Rosé Pine (dawn/moon/main variants) |
| `kanagawa` | Sumi-ink inspired |
| `melange` | Warm earthy tones |
| `tender` | Soft contrast dark |
| `synthwave` | Synthwave '84 retro |
| `cyberpunk` | Neon cyberpunk |
| `nord-light` | Light variant of nord |
| `flexoki` | Ink-like light/dark |
| `adrift` | Oceanic drift |
| `alabaster` | Minimal light |
| `barebones` | Spartan minimal |
| `breeze` | KDE Breeze |
| `cobalt2` | Cobalt2 by Wes Bos |
| `decay` | Decay dark |
| `deeper` | Deep dark |
| `earthly` | Earth tones |
| `edge` | Edge dark/light |
| `falcon` | Falcon dark |
| `flat` | Flat UI colors |
| `gitpod` | GitPod dark |
| `green` | Green monochrome |
| `ic-green-ppl` | Green PPL variant |
| `lunar` | Lunar dark |
| `miasma` | Miasma dark |
| `mono` | Monochrome |
| `nebula` | Nebula night sky |
| `notepad` | Notepad-like light |
| `nubia` | Nubia dark |
| `ocean` | Ocean blue |
| `one` | One Dark/Light |
| `onedarker` | Darker One Dark |
| `oxide` | Oxide dark |
| `pink` | Pink monochrome |
| `plastic` | Plastic theme |
| `purple` | Purple monochrome |
| `red` | Red monochrome |
| `rose` | Rose tinted |
| `royal` | Royal blue |
| `seashell` | Seashell light |
| `solarized-osaka` | Solarized Osaka variant |
| `sonokai` | Sonokai dark |
| `taonic` | Taonic dark |
| `tokyonight-moon` | Tokyo Night Moon variant |
| `tokyonight-storm` | Tokyo Night Storm variant |
| `windows` | Windows classic colors |
| `windows-light` | Windows light |
| `yellow` | Yellow monochrome |
| `zen` | Zen minimal |

> The above is a representative list. Run `Ctrl+X T` in the TUI to see all available themes on your installation.

## Theme List Command

`Ctrl+X T` (config key: `theme_list`) opens an interactive theme picker. Navigate with arrow keys, preview applies in real-time, press Enter to confirm.

## Custom Theme Colors

Define an inline theme object instead of a string name:

```jsonc
{
  "theme": {
    "name": "my-custom-theme",
    "black": "#000000",
    "red": "#ff0000",
    "green": "#00ff00",
    "yellow": "#ffff00",
    "blue": "#0000ff",
    "magneta": "#ff00ff",
    "cyan": "#00ffff",
    "white": "#ffffff",
    "brightBlack": "#555555",
    "brightRed": "#ff5555",
    "brightGreen": "#55ff55",
    "brightYellow": "#ffff55",
    "brightBlue": "#5555ff",
    "brightMagneta": "#ff55ff",
    "brightCyan": "#55ffff",
    "brightWhite": "#ffffff",
    "background": "#1a1a2e",
    "foreground": "#e0e0e0",
    "cursor": "#e0e0e0",
    "selectionBackground": "#3d3d5c"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Display name in theme picker |
| `black`–`white` | Yes | 8 standard ANSI colors |
| `brightBlack`–`brightWhite` | Yes | 8 bright ANSI colors |
| `background` | Yes | Terminal background |
| `foreground` | Yes | Default text color |
| `cursor` | Yes | Cursor color |
| `selectionBackground` | Yes | Text selection highlight |

## Theme Scope

- Theme applies to the **TUI only** (terminal UI elements, message panels, input bar, sidebar)
- Does **not** affect the model's output formatting
- Theme file is read on startup; change requires TUI restart (or use theme picker at runtime)

---

# Part B: Keybinding System (06b-keybinds)

## Overview

OpenCode provides **60+ customizable keybindings**. Configuration lives under the `keybinds` key (plural) in the TUI config (`tui.json`/`tui.jsonc`). Do **not** nest under a `tui` section — the `keybinds` key is top-level in the TUI config file.

```jsonc
// tui.json or tui.jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "opencode",
  "keybinds": {
    "leader": "ctrl+x",
    "command_list": "ctrl+p",
    "app_exit": "ctrl+c,ctrl+d,<leader>q"
  }
}
```

**Set OPENCODE_TUI_CONFIG** for a custom TUI config path.

## Leader Key Mechanism

Default leader: `Ctrl+X`.

1. Press and **release** the leader key (`Ctrl+X`)
2. Within `leader_timeout` (default 2000ms), press the action key
3. Example: `Ctrl+X` then `N` = new session

`leader_timeout` configured at the TUI config top level:

```jsonc
{ "leader_timeout": 3000 }
```

## Complete Keybind Reference (ALL Config Keys)

| Config Key | Default | Description |
|---|---|---|
| `leader` | `ctrl+x` | Leader/prefix key |
| `app_exit` | `ctrl+c,ctrl+d,<leader>q` | Exit application |
| `session_new` | `<leader>n` | New session |
| `session_list` | `<leader>l` | List / resume sessions |
| `session_compact` | `<leader>c` | Compact / summarize session |
| `session_interrupt` | `escape` | Interrupt current response |
| `session_fork` | (none) | Fork session (copy history) |
| `session_copy` | (none) | Copy session content |
| `session_rename` | (none) | Rename session |
| `session_export` | `<leader>x` | Export session as Markdown |
| `session_timeline` | `<leader>g` | Session timeline view |
| `session_next` | `<leader>right` | Switch to next session |
| `session_previous` | `<leader>left` | Switch to previous session |
| `session_parent` | `<leader>up` | Go to parent session |
| `messages_undo` | `<leader>u` | Undo last message + file changes |
| `messages_redo` | `<leader>r` | Redo undone message |
| `messages_yank` | `<leader>y` | Copy last assistant response |
| `messages_copy` | (same as yank) | Alias for copy last response |
| `model_list` | `<leader>m` | Open model picker |
| `model_cycle` | (none) | Cycle to next model |
| `model_cycle_recent` | `f2` | Cycle through recent models |
| `model_cycle_recent_reverse` | `shift+f2` | Reverse cycle recent models |
| `variant_cycle` | `ctrl+t` | Cycle model variants (thinking depth) |
| `agent_list` | `<leader>a` | Open agent picker |
| `agent_cycle` | `tab` | Cycle to next agent (Plan↔Build) |
| `agent_cycle_reverse` | `shift+tab` | Cycle to previous agent |
| `command_list` | `ctrl+p` | Command palette |
| `theme_list` | `<leader>t` | Theme picker |
| `thinking_toggle` | `ctrl+t` | Toggle reasoning display |
| `details_toggle` | (none) | Toggle tool execution details |
| `sidebar_toggle` | (none) | Toggle sidebar visibility |
| `header_toggle` | (none) | Toggle header visibility |
| `keyboard_focus` | (none) | Toggle keyboard focus mode |
| `tips_toggle` | `<leader>h` | Toggle tips display |
| `status_view` | `<leader>s` | Status view |
| `editor_open` | `<leader>e` | Open external editor |
| `input_submit` | `enter` | Send / submit message |
| `input_newline` | `shift+enter` | Insert new line (without submit) |
| `input_clear` | `ctrl+c` | Clear input buffer |
| `input_undo` | `ctrl+z,ctrl+-,super+z` | Undo input edit |
| `input_paste` | `ctrl+v` (preventDefault) | Paste from clipboard |
| `input_yank` | (none) | Yank (paste) last killed text |
| `input_delete` | (none) | Delete character |
| `scroll_up` | `pageup,ctrl+alt+b` | Scroll message pane up |
| `scroll_down` | `pagedown,ctrl+alt+f` | Scroll message pane down |
| `scroll_half_up` | `ctrl+alt+u` | Scroll half page up |
| `scroll_half_down` | `ctrl+alt+d` | Scroll half page down |
| `scroll_top` | `ctrl+g,home` | Jump to top of messages |
| `scroll_bottom` | `ctrl+alt+g,end` | Jump to bottom of messages |
| `search_toggle` | (none) | Toggle search in messages |
| `search_next` | (none) | Next search result |
| `search_prev` | (none) | Previous search result |
| `permission_allow` | `y` | Allow permission request |
| `permission_deny` | `n` | Deny permission request |
| `permission_always` | `a` | Always allow (this session) |
| `permission_fullscreen` | `ctrl+f` | Toggle fullscreen permission prompt |
| `popup_cancel` | `ctrl+g,escape` | Cancel popup / abort |
| `popup_confirm` | `enter` | Confirm popup |
| `popup_next` | `tab` | Next popup option |
| `popup_prev` | `shift+tab` | Previous popup option |
| `terminal_suspend` | (none on Win) | Suspend terminal (forced `none` on Windows) |
| `input_history_prev` | `up` | Browse previous input history |
| `input_history_next` | `down` | Browse next input history |
| `input_beginning` | `ctrl+a` | Move cursor to line start |
| `input_end` | `ctrl+e` | Move cursor to line end |
| `input_backward_char` | `ctrl+b` | Back one character |
| `input_forward_char` | `ctrl+f` | Forward one character |
| `input_backward_word` | `alt+b` | Back one word |
| `input_forward_word` | `alt+f` | Forward one word |
| `input_delete_to_start` | `ctrl+u` | Delete to line start |
| `input_delete_to_end` | `ctrl+k` | Delete to line end |
| `input_delete_word` | `ctrl+w` | Delete previous word |
| `input_delete_next_word` | `alt+d` | Delete next word |
| `input_transpose` | `ctrl+t` | Transpose characters |
| `input_delete_char` | `ctrl+d` | Delete character under cursor |

> Note: `input_*` readline-style bindings primarily work in the **Desktop app** (WebView2 input). Terminal TUI delegates to the terminal emulator's own readline handling.

## Key Syntax Reference

| Syntax | Meaning | Example |
|--------|---------|---------|
| `<leader>n` | Leader key then `n` | `<leader>q` = `Ctrl+X` then `Q` |
| `ctrl+x` | Ctrl + X | `ctrl+p` = `Ctrl+P` |
| `ctrl+shift+a` | Ctrl + Shift + A | `ctrl+shift+c` |
| `alt+x` | Alt + X (Meta) | `alt+b` = backward word |
| `shift+tab` | Shift + Tab | Reverse agent cycle |
| `super+z` | Windows/Command + Z | `super+z` (platform-specific) |
| `escape` | Esc key | `escape` to interrupt |
| `enter` | Return/Enter | Submit message |
| `tab` | Tab key | Cycle agent |
| `space` | Spacebar | — |
| `backspace` | Backspace | — |
| `pageup` / `pagedown` | PgUp / PgDn | Scroll messages |
| `home` / `end` | Home / End | Jump to top/bottom |
| `up` / `down` / `left` / `right` | Arrow keys | Navigation |
| `f1`–`f12` | Function keys | `f2` = cycle recent models |

## Disabling a Keybind

Set to the string `"none"`:

```jsonc
{ "keybinds": { "session_compact": "none" } }
```

## Multiple Bindings (Comma-separated)

```jsonc
{ "keybinds": { "app_exit": "ctrl+c,ctrl+d,<leader>q" } }
```

Multiple keys trigger the same action.

## Advanced Binding (Array Form)

```jsonc
{ "keybinds": { "messages_yank": ["<leader>y", "ctrl+shift+c"] } }
```

## Advanced Binding (Object Form)

```jsonc
{
  "keybinds": {
    "input_paste": {
      "key": "ctrl+v",
      "preventDefault": false
    }
  }
}
```

| Object Field | Type | Description |
|---|---|---|
| `key` | string | The key combination |
| `preventDefault` | boolean | Whether to prevent browser default (desktop app) |

## Binding Precedence

- Explicit `keybinds` config overrides defaults
- Multiple bindings for the same action are OR'd (any triggers the action)
- Setting to `"none"` disables all defaults for that action
- Unlisted config keys retain their built-in defaults

## Platform Notes

| Platform | Notes |
|----------|-------|
| **Windows** | `input_undo` adds `ctrl+z` (Windows lacks POSIX suspend); `terminal_suspend` forced to `none`; `Shift+Enter` may require terminal config |
| **macOS** | `super` key maps to Command; `alt` key maps to Option (may need terminal "Use Option as Meta" setting) |
| **Linux** | Standard X11 modifiers; Wayland may need `OC_ALLOW_WAYLAND=1` |

## Related Environment Variables

| Variable | Effect |
|----------|--------|
| `OPENCODE_TUI_CONFIG` | Custom path to TUI config file (default: `~/.config/opencode/tui.json`) |
| `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` | Disable auto-copy-on-drag-select |
| `OPENCODE_DISABLE_AUTOCOMPACT` | Disable automatic session compaction |

## Quick Reference Card

```
Leader key:  Ctrl+X (release, then action)

Common shortcuts:
  Ctrl+X N   New session
  Ctrl+X L   Session list
  Ctrl+X U   Undo
  Ctrl+X R   Redo
  Ctrl+X Y   Copy last response
  Ctrl+X C   Compact session
  Ctrl+X M   Model list
  Ctrl+X A   Agent list
  Ctrl+X T   Theme list
  Ctrl+X Q   Exit
  Ctrl+X E   Open editor
  Ctrl+X X   Export session
  Ctrl+X S   Status view
  Ctrl+X B   Sidebar toggle
  Ctrl+X G   Timeline
  Ctrl+X H   Tips toggle
  Ctrl+X F   Fork session (if enabled)
  Ctrl+P     Command palette
  Ctrl+T     Toggle thinking / cycle variants
  Tab        Cycle agent (Plan↔Build)
  Shift+Tab  Reverse cycle agent
  F2         Cycle recent models
  Escape     Interrupt

  PageUp/Ctrl+Alt+B       Scroll up
  PageDown/Ctrl+Alt+F     Scroll down
  Ctrl+Alt+U              Half page up
  Ctrl+Alt+D              Half page down
  Ctrl+G/Home             Jump to top
  Ctrl+Alt+G/End          Jump to bottom

Permission dialogs:
  y      Allow
  n      Deny
  a      Always allow
  Ctrl+F Toggle fullscreen
```
