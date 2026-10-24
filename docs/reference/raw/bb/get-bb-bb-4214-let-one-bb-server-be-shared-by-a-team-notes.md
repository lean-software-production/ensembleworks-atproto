# get-bb/bb#4214: Let one bb server be shared by a team (multiple users, per-user threads and machines) (source notes)

> Source: https://github.com/get-bb/bb/issues/4214
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-a3bee95d/001.md.
> Work: get-bb/bb#4214
> Quotations: 85 characters verbatim in this file; 85 of 90 allowed for this work across the knowledge base.

## About this source

A feature-request issue, get-bb/bb#4214, titled "Let one bb server be shared by a team (multiple users, per-user threads and machines)". Opened by galitianu on 2026-09-23; still open as of last update 2026-10-02. Labels: remote, security. The body is marked as agent generated.

## Key facts

- The author is building a bb plugin that derives bookkeeping (work done, tests run, decisions, whether agent claims match tool actions) from coding thread events, and wants several people to work in parallel on one large agent-driven task, each on their own laptop with their own provider login.
- Claimed limitation, inferred by the author from reading the code at commit `a60b895` (not from a multi-person setup): a bb server has one identity. Machines are authenticated as one built-in system user (`machine-auth.ts`); in Connect each server and each machine belongs to exactly one `user_id` (`schema.ts`); thread `visibility` is `visible | hidden`, not per-user.
- Consequence described: each person needs their own server, and because a thread's events can be read only on the owner's server, shared facts must carry copied evidence excerpts rather than openable links.
- Requested capabilities: (1) more than one identity per server; (2) teammates enroll their own laptops as execution machines, with provider CLIs authenticating locally so the server never holds provider credentials; (3) thread ownership with per-user rules for see, steer, archive (simplest version: all can read, only owner steers); (4) plugin SDK access to a thread's owner so plugins can attribute events and scope state per person.
- The author wants Account Pooler, secrets and permission limits to remain scoped to a machine or person, not shared.
- Current workaround: one server per person plus an external shared store syncing copied evidence, which duplicates bb's event log, identity and access control.
- Open questions to maintainers: whether multi-user is planned, whether the server DB is meant to hold event logs from many people, and how per-user permissions would interact with per-machine permission limits.
- The author offers to build it upstream (starting with identity, thread ownership and enrollment of machines owned by other users) and will seek contributor approval on Discord before any PR.
- Bot comment (bb-slop-cop, 2026-09-23): classified Type Feature, Priority Medium, Effort High; labels `remote` and `security`; notes a workaround exists and that implementation needs substantial architecture and permission design.
- Comment by twilwa (2026-10-02): expresses interest in multiplayer for bb, considering a plugin and possibly a connectable thin chat client.

## Related

bb Connect; bb plugin SDK; Account Pooler; multi-user thread sharing; other bb remote or sharing issues.
