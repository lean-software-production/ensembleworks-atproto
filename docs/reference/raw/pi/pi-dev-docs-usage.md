# Pi Coding Agent

> Source: https://pi.dev/docs/latest/usage
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode html; 1 response(s) archived in build/reference-wiki/http/pi-dev-97d4df2f/ (git-ignored): build/reference-wiki/http/pi-dev-97d4df2f/002.html (HTTP 200, sha256 e5f4b818943a)
> Extraction: Main content extracted from HTML with BeautifulSoup + markdownify; scripts, navigation and footer chrome removed.
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: MIT — pi.dev page footer states 'MIT License'; docs come from earendil-works/pi repo, whose LICENSE is MIT
> Attribution: Mario Zechner and contributors, Pi coding agent documentation (pi.dev)

Navigation

On this page

Documentation

## Documentation

## On this page

On this page

# Use Pi in the terminal

Latest

Run `pi` from the folder you want to work in. Pi uses that folder to discover files, instructions, and configuration, and to group saved sessions. If you have not installed Pi or chosen a model yet, follow the [Quickstart](/docs/latest/quickstart).

Pi may ask whether you trust the working folder before loading its project resources. See [Project trust](/docs/latest/security#understand-project-trust).

The transcript shows your prompts, Pi's responses, tool calls, results, and errors. You write prompts and commands in the editor. The footer shows the current folder, session, model, context usage, and accumulated usage and cost.

## Enter a prompt

[Copied](#enter-a-prompt)

Type a request and press `Enter` to send it. Use `Shift+Enter` to add a line, or press `Ctrl+G` to work on a longer prompt in your configured external editor.

To include files or images:

- Type `@` to search for a file and add it to your prompt.
- Press `Tab` to complete a path.
- Paste an image or drag it into a compatible terminal.

## Follow Pi's work

[Copied](#follow-pis-work)

Pi shows each tool call and result while it works. Press `Ctrl+O` to expand or collapse tool output. Press `Ctrl+T` to show or hide thinking blocks.

The startup header lists the instructions and resources Pi loaded. The editor border indicates the current thinking level. The footer updates as the model uses context and reports usage.

Pi does not ask before every tool call. Review commands and changed files, and use a sandbox for untrusted or unattended work. See [Security](/docs/latest/security).

## Change direction

[Copied](#change-direction)

You can send more input while Pi is working:

| What you want | Action |
| --- | --- |
| Adjust the current task | Type a message and press `Enter` |
| Add work after the current task | Type a message and press `Alt+Enter` |
| Return queued messages to the editor | Press `Alt+Up` |
| Stop the current task | Press `Escape` |

A message sent with `Enter` waits until the current response and its tool calls finish, then guides the next response. A follow-up sent with `Alt+Enter` waits until Pi finishes the current task. Aborting returns queued messages to the editor.

Windows Terminal reserves some Alt shortcuts. See [Terminal Setup](/docs/latest/terminal-setup) for the Windows alternatives.

## Change the model or settings

[Copied](#change-the-model-or-settings)

Type `/` to search the available commands. The commands you will use most often are:

- `/model` selects a model. Press `Ctrl+L` to open the same selector.
- `/thinking` selects how much reasoning the current model uses. Press `Shift+Tab` to cycle through supported levels.
- `/login` and `/logout` manage provider access.
- `/settings` changes common preferences.

Prompt templates, skills, and extensions can add more commands to the same menu. See [Choose a Model](/docs/latest/models), [Configuration](/docs/latest/configuration), or the complete [Slash Commands reference](/docs/latest/slash-commands).

## Continue or start over

[Copied](#continue-or-start-over)

Pi saves sessions automatically unless session persistence is disabled.

- `/new` starts a new session.
- `/resume` opens another saved session.
- `/name` gives the current session a recognizable name.
- `/session` shows its file, ID, message count, token usage, and cost.

Use `/tree`, `/fork`, or `/clone` when you want to explore another approach without losing existing work. Use `/compact` to reduce the conversation history sent to the model. See [Sessions and Context](/docs/latest/sessions) for these workflows.

After leaving Pi, run `pi --continue` from the same folder to resume its most recent session.

## Run a terminal command

[Copied](#run-a-terminal-command)

Prefix a command with `!` to run it and include its output in the conversation:

```
!git status
```

Use `!!` when you want to run a command without sending its output to the model.

## Copy, export, or share results

[Copied](#copy-export-or-share-results)

Press `Ctrl+X` or run `/copy` to copy the last assistant response. Use `/export` to save the session as HTML or JSONL.

Use `/share` to upload the session and get a viewer link. By default, Radius authentication makes the artifact visible to your Radius organization; otherwise, Pi creates a private GitHub gist through the GitHub CLI. The [`sessionShareDestination`](/docs/latest/settings#sessions-and-context) setting can force either destination. Review the session first because it can contain prompts, tool output, file contents, and credentials exposed during the conversation.

## Adjust the terminal

[Copied](#adjust-the-terminal)

Fullscreen mode, the default, keeps the editor and status area fixed while the transcript scrolls within the terminal window. Regular mode uses the terminal's normal scrollback. Choose a mode through `/settings` or `--tui-mode`.

Terminal support for mouse input, keyboard shortcuts, and inline images varies. See [Terminal Setup](/docs/latest/terminal-setup) for platform-specific configuration and [Keybindings](/docs/latest/keybindings) for every configurable shortcut. Run `/hotkeys` to inspect the shortcuts active in your current session.

## Collect diagnostic information

[Copied](#collect-diagnostic-information)

When troubleshooting terminal rendering or conversation state, run `/debug`. Pi writes the rendered terminal lines and current session messages to `pi-debug.log` in your [agent directory](/docs/latest/configuration#agent-directory).

Review this file before sharing it. It can contain prompts, model responses, tool output, file contents, and terminal data.


## License notice (verbatim, from https://raw.githubusercontent.com/earendil-works/pi/main/LICENSE)

```
MIT License

Copyright (c) 2025 Mario Zechner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
