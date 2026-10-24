# Pi Coding Agent

> Source: https://pi.dev/docs/latest/sessions
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode html; 1 response(s) archived in build/reference-wiki/http/pi-dev-8071d281/ (git-ignored): build/reference-wiki/http/pi-dev-8071d281/002.html (HTTP 200, sha256 3996f7dbf1bb)
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

# Sessions and Context

Latest

Pi saves a conversation as a session. The active branch of that session supplies conversation history for the next model request. Use session commands to continue work, explore another branch, or reduce the amount of history sent to the model.

## Continue or switch sessions

[Copied](#continue-or-switch-sessions)

Pi saves sessions automatically unless you start it with `--no-session`.

```
pi --continue
pi --resume
```

`--continue` opens the most recent session for the current working directory. `--resume` opens the session picker. In interactive mode, `/resume` opens the same picker and `/new` starts a new session.

Use `/name` or `--name` to assign a recognizable session name. Run `/session` to verify the current session file, ID, message count, token usage, and cost.

The session picker lets you search, rename, and delete sessions. It can also show paths, change sorting, and limit results to named sessions. See [Keybindings](/docs/latest/keybindings#sessions) for its shortcuts.

## Choose how to branch

[Copied](#choose-how-to-branch)

Pi stores entries as a tree, so returning to an earlier point does not erase the branch you leave.

| Action | Result | Use it when |
| --- | --- | --- |
| `/tree` | Moves within the current session file | Related alternatives should stay together |
| `/fork` | Creates a new session from an earlier user message | The alternative should become separate work |
| `/clone` | Copies the active branch into a new session | You want a separate copy of the current state |

In `/tree`, select a user message to put its text back in the editor. Edit and submit it to create another branch. Selecting an assistant response or another entry continues after that entry with an empty editor.

When you leave a branch, Pi can summarize it and attach that summary to the branch you enter. This preserves relevant work from the abandoned path without including every message from it.

For the persisted tree and entry types, see [Session Format](/docs/latest/session-format).

## Manage conversation context

[Copied](#manage-conversation-context)

The model receives the active branch, not every branch in the session file. Pi combines that history with the system prompt, discovered context files, available tools, and loaded skill descriptions. [How Pi Works](/docs/latest/how-pi-works#context) describes how those inputs are assembled.

The footer shows current context usage. When the active context approaches the model's limit, Pi normally compacts older history automatically. Compaction adds a summary and keeps recent messages. It does not delete the original session entries.

Run `/compact` to compact manually. You can add instructions when the summary should preserve a particular topic or decision. Configure automatic compaction and retained history through [Settings](/docs/latest/settings#compaction).

Compaction can fail if the provider is unavailable or cannot accept the summarization request. Correct the provider problem and run `/compact` again. Disabling automatic compaction does not disable the manual command.

See [Compaction Reference](/docs/latest/compaction) for thresholds, retained boundaries, branch-summary behavior, and extension hooks.

## Control session storage

[Copied](#control-session-storage)

By default, Pi stores sessions under `~/.pi/agent/sessions/`, grouped by working directory. Use `--session-dir`, `PI_CODING_AGENT_SESSION_DIR`, or the `sessionDir` setting to choose another location. The CLI option has highest precedence.

Use `--no-session` for an ephemeral run. An ephemeral session cannot be resumed after Pi exits.

Use `--session` when you already know the session path or ID. Use `--fork` to create a new session from an existing session before interactive mode starts.

## Export or share a session

[Copied](#export-or-share-a-session)

Use `/export` to write the current session as HTML or JSONL. Use `/share` to upload it and get a viewer link. By default, Pi uses a Radius artifact when Radius authentication is configured; otherwise, it uses a private GitHub gist. Set [`sessionShareDestination`](/docs/latest/settings#sessions-and-context) to `gist` or `radius` to force one destination.

Review exported or shared sessions first. They can contain prompts, model responses, tool arguments, command output, file contents, and extension messages.

## Report a bug

[Copied](#report-a-bug)

Run `/bug [description]` to prepare a private report for the Pi developers. You can include the session transcript, omit it, or ask the current model to summarize the problem. Review any transcript or generated summary because it can contain sensitive conversation data.

The report includes environment and provider configuration without credential values, plus recorded error diagnostics. Upload it through `radius.pi.dev` or export the same report as a zip to inspect and share yourself. Uploads do not require a login; Radius authentication attributes the report to your account so the developers can follow up. If an upload fails, Pi offers to export the zip.


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
