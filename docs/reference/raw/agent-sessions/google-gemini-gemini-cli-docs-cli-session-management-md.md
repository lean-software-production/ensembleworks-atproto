# google-gemini/gemini-cli: docs/cli/session-management.md

> Source: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/session-management.md
> Resolved: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/session-management.md
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode github-blob; 3 response(s) archived in build/reference-wiki/http/github-com-8404d2a7/ (git-ignored): build/reference-wiki/http/github-com-8404d2a7/004.txt (HTTP 200, sha256 849204da2c21), build/reference-wiki/http/github-com-8404d2a7/005.json (HTTP 200, sha256 971802e87fa0), build/reference-wiki/http/github-com-8404d2a7/006.json (HTTP 200, sha256 abbcb77cc853)
> Extraction: Verbatim file content (raw file at ref `main`; latest commit touching path: 93844dfa10f6d71edc09be40dfde205edfbcc939).
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: Apache-2.0 — google-gemini/gemini-cli LICENSE file (Apache License 2.0; GitHub license API SPDX Apache-2.0)
> Attribution: google-gemini/gemini-cli contributors (Apache-2.0 licensed)

# Session management

Session management saves your conversation history so you can resume your work
where you left off. Use these features to review past interactions, manage
history across different projects, and configure how long data is retained.

## Automatic saving

Your session history is recorded automatically as you interact with the model.
This background process ensures your work is preserved even if you interrupt a
session.

- **What is saved:** The complete conversation history, including:
  - Your prompts and the model's responses.
  - All tool executions (inputs and outputs).
  - Token usage statistics (input, output, cached, etc.).
  - Assistant thoughts and reasoning summaries (when available).
- **Location:** Sessions are stored in `~/.gemini/tmp/<project_hash>/chats/`,
  where `<project_hash>` is a unique identifier based on your project's root
  directory.
- **Scope:** Sessions are project-specific. Switching directories to a different
  project switches to that project's session history.

## Resuming sessions

You can resume a previous session to continue the conversation with all prior
context restored. Resuming is supported both through command-line flags and an
interactive browser.

### From the command line

When starting Gemini CLI, use the `--resume` (or `-r`) flag to load existing
sessions.

- **Resume latest:**

  ```bash
  gemini --resume
  ```

  This immediately loads the most recent session.

- **Resume by index:** List available sessions first (see
  [Listing sessions](#listing-sessions)), then use the index number:

  ```bash
  gemini --resume 1
  ```

- **Resume by ID:** You can also provide the full session UUID:
  ```bash
  gemini --resume a1b2c3d4-e5f6-7890-abcd-ef1234567890
  ```

### From the interactive interface

While the CLI is running, use the `/resume` slash command to open the **Session
Browser**:

```text
/resume
```

When typing `/resume` (or `/chat`) in slash completion, commands are grouped
under titled separators:

- `-- auto --` (session browser)
  - `list` is selectable and opens the session browser
- `-- checkpoints --` (manual tagged checkpoint commands)

Unique prefixes such as `/resum` and `/cha` resolve to the same grouped menu.

The Session Browser provides an interactive interface where you can perform the
following actions:

- **Browse:** Scroll through a list of your past sessions.
- **Preview:** See details like the session date, message count, and the first
  user prompt.
- **Search:** Press `/` to enter search mode, then type to filter sessions by ID
  or content.
- **Select:** Press **Enter** to resume the selected session.
- **Esc:** Press **Esc** to exit the Session Browser.

### Manual chat checkpoints

For named branch points inside a session, use chat checkpoints:

```text
/resume save decision-point
/resume list
/resume resume decision-point
```

Compatibility aliases:

- `/chat ...` works for the same commands.
- `/resume checkpoints ...` also remains supported during migration.

## Parallel sessions with Git worktrees

When working on multiple tasks at once, you can use
[Git worktrees](./git-worktrees.md) to give each Gemini session its own copy of
the codebase. This prevents changes in one session from colliding with another.

## Managing sessions

You can list and delete sessions to keep your history organized and manage disk
space.

### Listing sessions

To see a list of all available sessions for the current project from the command
line, use the `--list-sessions` flag:

```bash
gemini --list-sessions
```

Output example:

```text
Available sessions for this project (3):

  1. Fix bug in auth (2 days ago) [a1b2c3d4]
  2. Refactor database schema (5 hours ago) [e5f67890]
  3. Update documentation (Just now) [abcd1234]
```

### Deleting sessions

You can remove old or unwanted sessions to free up space or declutter your
history.

**From the command line:** Use the `--delete-session` flag with an index or ID:

```bash
gemini --delete-session 2
```

**From the Session Browser:**

1.  Open the browser with `/resume`.
2.  Navigate to the session you want to remove.
3.  Press **x**.

## Configuration

You can configure how Gemini CLI manages your session history in your
`settings.json` file. These settings let you control retention policies and
session lengths.

### Session retention

By default, Gemini CLI automatically cleans up old session data to prevent your
history from growing indefinitely. When a session is deleted, Gemini CLI also
removes all associated data, including implementation plans, task trackers, tool
outputs, and activity logs.

The default policy is to **retain sessions for 30 days**.

#### Configuration

You can customize these policies using the `/settings` command or by manually
editing your `settings.json` file:

```json
{
  "general": {
    "sessionRetention": {
      "enabled": true,
      "maxAge": "30d",
      "maxCount": 50
    }
  }
}
```

- **`enabled`**: (boolean) Master switch for session cleanup. Defaults to
  `true`.
- **`maxAge`**: (string) Duration to keep sessions (for example, "24h", "7d",
  "4w"). Sessions older than this are deleted. Defaults to `"30d"`.
- **`maxCount`**: (number) Maximum number of sessions to retain. The oldest
  sessions exceeding this count are deleted. Defaults to undefined (unlimited).
- **`minRetention`**: (string) Minimum retention period (safety limit). Defaults
  to `"1d"`. Sessions newer than this period are never deleted by automatic
  cleanup.

### Session limits

You can limit the length of individual sessions to prevent context windows from
becoming too large and expensive.

```json
{
  "model": {
    "maxSessionTurns": 100
  }
}
```

- **`maxSessionTurns`**: (number) The maximum number of turns (user and model
  exchanges) allowed in a single session. Set to `-1` for unlimited (default).

  **Behavior when limit is reached:**

  - **Interactive mode:** The CLI shows an informational message and stops
    sending requests to the model. You must manually start a new session.
  - **Non-interactive mode:** The CLI exits with an error.

## Next steps

- Explore the [Memory tool](../tools/memory.md) to save persistent information
  across sessions.
- Learn how to [Checkpoint](./checkpointing.md) your session state.
- Check out the [CLI reference](./cli-reference.md) for all command-line flags.


## License notice (verbatim, from https://raw.githubusercontent.com/google-gemini/gemini-cli/main/LICENSE)

```

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
