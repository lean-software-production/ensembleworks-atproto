# agentclientprotocol/agent-client-protocol

> Source: https://github.com/agentclientprotocol/agent-client-protocol
> Resolved: https://api.github.com/repos/agentclientprotocol/agent-client-protocol; https://api.github.com/repos/agentclientprotocol/agent-client-protocol/readme
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode github-repo; 4 response(s) archived in build/reference-wiki/http/github-com-d261b7d9/ (git-ignored): build/reference-wiki/http/github-com-d261b7d9/005.json (HTTP 200, sha256 81daee6b1ddd), build/reference-wiki/http/github-com-d261b7d9/006.txt (HTTP 200, sha256 56f5d88d9956), build/reference-wiki/http/github-com-d261b7d9/007.json (HTTP 200, sha256 4b7da6285214), build/reference-wiki/http/github-com-d261b7d9/008.json (HTTP 200, sha256 0d462800a4e0)
> Extraction: Repository metadata, README (verbatim) and top-level listing via read-only GitHub REST API.
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: Apache-2.0 — agentclientprotocol/agent-client-protocol LICENSE file (Apache License 2.0; GitHub license API SPDX Apache-2.0)
> Attribution: agentclientprotocol/agent-client-protocol contributors (Apache-2.0 licensed)

## Repository metadata (GitHub REST API)

- Full name: agentclientprotocol/agent-client-protocol
- Description:  A protocol for connecting any editor to any agent
- Homepage: https://agentclientprotocol.com
- Default branch: main
- License: Apache-2.0
- Primary language: Rust
- Topics: none
- Created: 2025-06-23T17:39:36Z
- Last pushed: 2026-10-24T05:55:09Z
- Stars at collection: 4493
- Forks at collection: 447
- Open issues at collection: 35
- Archived: False
- Fork: False

## README

<a href="https://agentclientprotocol.com/" >
  <img alt="Agent Client Protocol" src="https://zed.dev/img/acp/banner-dark.webp">
</a>

### Agent Client Protocol

The Agent Client Protocol (ACP) standardizes communication between _code editors_ (interactive programs for viewing and editing source code) and _coding agents_ (programs that use generative AI to autonomously modify code).

Learn more at [agentclientprotocol.com](https://agentclientprotocol.com/).

#### Rust Crate and Schema Artifacts

This repository's root Rust crate is [`agent-client-protocol-schema`](https://crates.io/crates/agent-client-protocol-schema). It provides the Rust data model for ACP wire messages, including request, response, notification, JSON-RPC envelope, and protocol-version types. Use this crate when you need direct access to ACP protocol types, schema-oriented tooling, or code generation inputs.

If you are implementing a Rust ACP agent or client, start with the higher-level [`agent-client-protocol`](https://crates.io/crates/agent-client-protocol) runtime crate instead. That crate provides the client and agent runtime APIs for ACP integrations; this schema crate is the lower-level protocol type surface.

Generated JSON Schema artifacts live in [`schema/v1`](./schema/v1/) and [`schema/v2`](./schema/v2/). When a schema release is published, the versioned `.json` files are also attached to the corresponding [`schema-v*` GitHub release](https://github.com/agentclientprotocol/agent-client-protocol/releases), which is the recommended download surface for SDK generators and other release automation.

#### Versioning

The Rust crate version and JSON Schema release versions describe the Rust crate and JSON Schema artifacts themselves. The Rust crate is published to crates.io, while the versioned JSON Schema files are attached to GitHub releases rather than published as crates. These versions follow the compatibility expectations of those artifacts: Rust APIs, generated schema structure, artifact layout, and other details that downstream SDKs or code generators may consume.

**The current stable ACP protocol version is `1`.**

ACP wire compatibility is determined separately by the protocol version exchanged during `initialize` via `protocolVersion`. The `version` field in the versioned `schema/*/meta*.json` files also describes the ACP protocol version that the corresponding schema represents.

This means two versions of the JSON Schema artifacts can describe the same wire-compatible ACP protocol version while having different schema structure for SDK generators. For example, a release might change how definitions are organized, named, or emitted in the JSON Schema in a way that affects downstream code generation without changing the JSON messages exchanged by ACP clients and agents.

Consumers should not infer wire compatibility from the crate or schema release version alone. Use the negotiated `protocolVersion` to determine the ACP wire protocol shape and breaking-compatibility level. Within a protocol version, use the exchanged capabilities to decide which optional ACP messages and features are supported. Use artifact versions to manage compatibility with this repository's Rust and schema outputs.

#### Integrations

- [Schema](./schema/v1/schema.json)
- [Agents](https://agentclientprotocol.com/overview/agents)
- [Clients](https://agentclientprotocol.com/overview/clients)
- Official Libraries
  - **Kotlin**: [`acp-kotlin`](https://github.com/agentclientprotocol/kotlin-sdk) - Supports JVM, other targets are in progress, see [samples](https://github.com/agentclientprotocol/kotlin-sdk/tree/master/samples/kotlin-acp-client-sample/src/main/kotlin/com/agentclientprotocol/samples)
  - **Java**: [`java-sdk`](https://github.com/agentclientprotocol/java-sdk) - See [examples](https://github.com/agentclientprotocol/java-sdk/tree/main/examples)
  - **Python**: [`python-sdk`](https://github.com/agentclientprotocol/python-sdk) - See [examples](https://github.com/agentclientprotocol/python-sdk/tree/main/examples)
  - **Rust**: [`agent-client-protocol`](https://crates.io/crates/agent-client-protocol) - See [examples/agent.rs](https://github.com/agentclientprotocol/rust-sdk/blob/main/src/agent-client-protocol/examples/agent.rs) and [examples/client.rs](https://github.com/agentclientprotocol/rust-sdk/blob/main/src/agent-client-protocol/examples/client.rs)
  - **TypeScript**: [`@agentclientprotocol/sdk`](https://www.npmjs.com/package/@agentclientprotocol/sdk) - See [examples/](https://github.com/agentclientprotocol/typescript-sdk/tree/main/src/examples)
- [Community Libraries](https://agentclientprotocol.com/libraries/community)

#### Contributing

ACP is a protocol intended for broad adoption across the ecosystem; we follow a structured process to ensure changes are well-considered. Read the [Contributing Guide](./CONTRIBUTING.md) for more information.

#### Contribution Policy

This project does not require a Contributor License Agreement (CLA). Instead, contributions are accepted under the following terms:

> By contributing to this project, you agree that your contributions will be licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). You affirm that you have the legal right to submit your work, that you are not including code you do not have rights to, and that you understand contributions are made without requiring a Contributor License Agreement (CLA).


## Top-level files

- `.github` (dir)
- `.gitignore` (file)
- `.prettierignore` (file)
- `.prettierrc` (file)
- `.release-plz.toml` (file)
- `AGENTS.md` (file)
- `CHANGELOG.md` (file)
- `CLAUDE.md` (file)
- `CODE_OF_CONDUCT.md` (file)
- `CONTRIBUTING.md` (file)
- `Cargo.lock` (file)
- `Cargo.toml` (file)
- `GOVERNANCE.md` (file)
- `LICENSE` (file)
- `MAINTAINERS.md` (file)
- `README.md` (file)
- `agent-client-protocol-schema` (dir)
- `clippy.toml` (file)
- `deny.toml` (file)
- `docs` (dir)
- `package-lock.json` (file)
- `package.json` (file)
- `schema-generator` (dir)
- `schema` (dir)
- `scripts` (dir)
- `typos.toml` (file)


## License notice (verbatim, from https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/main/LICENSE)

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

   Copyright 2025 Zed Industries, Inc. and contributors

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
