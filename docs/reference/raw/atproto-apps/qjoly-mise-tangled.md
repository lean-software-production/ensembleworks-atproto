# qjoly/mise-tangled

> Source: https://github.com/qjoly/mise-tangled
> Resolved: https://api.github.com/repos/qjoly/mise-tangled; https://api.github.com/repos/qjoly/mise-tangled/readme
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode github-repo; 4 response(s) archived in build/reference-wiki/http/github-com-75d44129/ (git-ignored): build/reference-wiki/http/github-com-75d44129/005.json (HTTP 200, sha256 0c0654635949), build/reference-wiki/http/github-com-75d44129/006.txt (HTTP 200, sha256 3fdb265cbe04), build/reference-wiki/http/github-com-75d44129/007.json (HTTP 200, sha256 59a1a4e1df21), build/reference-wiki/http/github-com-75d44129/008.json (HTTP 200, sha256 4ac7c6cbc9a6)
> Extraction: Repository metadata, README (verbatim) and top-level listing via read-only GitHub REST API.
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: MIT — GitHub repo qjoly/mise-tangled LICENSE file (MIT, Copyright (c) 2026 qjoly)
> Attribution: Copyright (c) 2026 qjoly; qjoly/mise-tangled

## Repository metadata (GitHub REST API)

- Full name: qjoly/mise-tangled
- Description: mise backend plugin: install binaries attached to tangled.org tags
- Homepage: none
- Default branch: main
- License: MIT
- Primary language: Lua
- Topics: none
- Created: 2026-08-17T10:45:15Z
- Last pushed: 2026-10-03T11:34:04Z
- Stars at collection: 1
- Forks at collection: 0
- Open issues at collection: 1
- Archived: False
- Fork: False

## README

### mise-tangled

[![ci](https://github.com/qjoly/mise-tangled/actions/workflows/ci.yml/badge.svg)](https://github.com/qjoly/mise-tangled/actions/workflows/ci.yml)

A [mise](https://mise.jdx.dev) backend plugin that installs binaries attached to
[tangled](https://tangled.org) tags.

Tangled release artifacts are `sh.tangled.repo.artifact` records living in the PDS of whoever
uploaded them, with the binary stored as an atproto blob. The plugin resolves a tag to its
artifact and installs it.

#### Install

```bash
mise plugin install tangled https://github.com/qjoly/mise-tangled
```

The repo lives on GitHub and is mirrored on tangled.

#### Usage

```bash
mise ls-remote 'tangled:tangled.org/core'
mise use 'tangled:tangled.org/core@1.2.0-alpha'
```

Tool syntax is `tangled:<handle-or-did>/<repo>`. Only tags that carry an artifact show up as
versions.

The plugin picks the artifact on its own when the file name contains the OS and the architecture
(`linux`, `darwin`/`macos`, `amd64`/`x86_64`, `arm64`/`aarch64`). Otherwise, name it:

```toml
[tools]
"tangled:tangled.org/core" = { version = "1.2.0-alpha", asset = "appview-v{version}-x86_64-linux", bin = "appview" }
```

Use single braces in `mise.toml`: mise renders the file as a template first and eats one brace
pair. Both `{version}` and `{{version}}` are accepted, so either form works.

##### Options

| Option | Default | Purpose |
|---|---|---|
| `asset` | auto by os/arch | artifact name, templated with `{version}`, `{os}`, `{arch}` |
| `allowed_uploaders` | none | extra DIDs whose artifacts are trusted, comma separated |
| `bin` | repo name | binary name in `bin/` (single-file artifacts only) |
| `appview` | `https://api.tangled.org` | appview XRPC host |
| `resolver` | `https://slingshot.microcosm.blue` | handle -> DID resolver |
| `git_host` | `https://tangled.org` | host used for `git ls-remote` |
| `repo_url` | none | full clone URL, overrides `git_host` |

Self-hosted knot:

```toml
"tangled:did:plc:xxxx/mytool" = { version = "latest", repo_url = "https://knot.example.com/did:plc:xxxx/mytool" }
```

#### How it works

1. `git ls-remote --tags --refs` -> tag names and the hash of their tag object
2. `sh.tangled.repo.getRepo` -> the repo's own DID
3. `sh.tangled.repo.listArtifacts` -> artifacts of every uploader, filtered on the tag hash
4. `com.atproto.sync.getBlob` on the uploader's PDS -> the bytes

#### Who is trusted

An artifact record lives in the uploader's own PDS, and nothing stops a stranger from attaching
one to your tag. The appview aggregates them all, so the plugin keeps only the artifacts whose
uploader is the repo owner, the repo DID itself, or a collaborator listed by
`sh.tangled.repo.listCollaborators`. Add other DIDs with the `allowed_uploaders` option if you
know what you are trusting.

The blob CID is a CIDv1 `raw` + `sha2-256`. The plugin reads the expected sha256 out of the CID
and checks it after download, so nobody has to publish a checksum file next to the binary. If the
CID has any other shape, or if no `sha256sum` or `shasum` is available, the install stops instead
of accepting unverified bytes.

#### Publishing artifacts from tangled CI

[`examples/tangled-release.yml`](examples/tangled-release.yml) is a working workflow: it
cross compiles a Go binary for four platforms on every `v*` tag, uploads each one with
`com.atproto.repo.uploadBlob` and creates one artifact record per file. Three things matter for
this plugin to find them:

- the tag has to be annotated (`git tag -a`), since a record points at a tag object
- the identity signing the records has to be the repo owner or a collaborator
- put the OS and the architecture in the file name, separated by `-`, `_` or `.`, as in
  `mytool-v1.2.0-linux-amd64`, and no `asset` option is needed

#### Caveats

- The lexicon caps an artifact at 50 MB, so publish large binaries compressed.
- Tags must be annotated. Artifacts point at a tag object, and a lightweight tag creates none.
- `mise ls-remote` hides prereleases, so `1.2.0-alpha` style tags only show up on explicit install.
- Requires `git` and a sha256 tool in `PATH`. Windows is not supported yet.

#### Development

```bash
mise run test          # offline: parsing, artifact matching, CID decoding, hooks load
mise run lint          # stylua
mise run link          # link the plugin into mise and clear its cache
mise run integration   # installs a real artifact from tangled, needs network
```

CI runs `test` on Linux and macOS, `lint`, and `integration` as a non-blocking job since it
depends on the appview being reachable.

#### License

MIT


## Top-level files

- `.github` (dir)
- `.gitignore` (file)
- `CHANGELOG.md` (file)
- `LICENSE` (file)
- `README.md` (file)
- `examples` (dir)
- `hooks` (dir)
- `metadata.lua` (file)
- `mise.toml` (file)
- `stylua.toml` (file)
- `test` (dir)


## License notice (verbatim, from https://raw.githubusercontent.com/qjoly/mise-tangled/main/LICENSE)

```
MIT License

Copyright (c) 2026 qjoly

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
