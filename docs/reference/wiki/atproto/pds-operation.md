# ATProto PDS Operation and Observability

> Sources: atproto.com "Make the PDS your own: customization and metrics" (Bluesky Social PBC; notes only), undated; atproto.com "The Atproto Spaces Alpha is Live" (notes only); both collected 2026-10-23; source inventory: Make the PDS Your Own: Customization and Metrics - AT Protocol (source notes) (attributed source notes; Unknown); The Atproto Spaces Alpha is Live - AT Protocol (source notes) (attributed source notes; Unknown)
> Raw: [PDS customization and metrics post (notes)](../../raw/atproto/make-the-pds-your-own-customization-and-metrics-at-protocol-notes.md); [spaces alpha post (notes)](../../raw/atproto/the-atproto-spaces-alpha-is-live-at-protocol-notes.md)
> Updated: 2026-10-24

## Overview

These sources describe the reference PDS's operator surface:
- branding through `pds.env`,
- built-in OpenTelemetry that is off by default,
- a sample Prometheus/Grafana stack,
- a larger default blob limit.

They also cover the separate **spaces-alpha** Docker image that self-hosters need to experiment with private sessions. A team that wants spaces today has to run the alpha image or use Bluesky's hosted alpha PDS. Data on either may be wiped.

## Reference PDS release: customization and metrics

- **Branding.** `PDS_SERVICE_NAME`, `PDS_LOGO_URL`, a set of `PDS_*_COLOR` variables, footer links such as `PDS_PRIVACY_POLICY_URL`, and auth-screen background URLs. The name and logo also appear in transactional emails.
- **OpenTelemetry** (traces, metrics, logs) is off by default. Enable it with `NODE_OPTIONS`, `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_SERVICE_NAME`.
  - Auto-instrumentation covers HTTP, SQLite, S3-compatible blob storage and Node runtime metrics.
  - XRPC spans are normalised per method.
  - Custom counters include `account.created`, `session.created` and `oauth.authorization`.
- **Monitoring.** A `monitoring/` directory in the reference PDS repo provides Prometheus, Grafana and node_exporter with an overview dashboard. There is no OTel Collector, because Prometheus v3 receives OTLP directly. The post says the stack runs in under 1GB of memory and binds to localhost by default.
- **Blobs.** The default maximum is 300M, and existing installs must set `PDS_BLOB_UPLOAD_LIMIT=314572800`. `describeServer` advertises `blobUploadLimit`. See [ATProto Blobs and Size Limits](blobs-and-size-limits.md).
- **Fix.** The connected-apps list could previously omit sessions that had not refreshed recently.

## Running spaces (alpha)

- Bluesky maintains a tagged image, `ghcr.io/bluesky-social/atproto:pds-spaces-alpha`. The alpha post says it is compatible with the reference PDS distribution and needs no new configuration. It also warns that database schemas may change without clean migrations, and advises against migrating real accounts.
- A hosted alpha PDS needs an invite code. Its data is neither permanent nor stable, and the whole PDS will be deleted after the alpha. Updates are planned for Thursdays and announced on the atmosphere.community forum.
- Ecosystem PDS implementations of the proposed spec: ZDS (Zig), atproto-crates PDS (Rust), rsky PDS (Rust, Blacksky). There is also HappyView, an AppView framework.

## See Also

- [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)
- [ATProto Blobs and Size Limits](blobs-and-size-limits.md)
- [OpenTelemetry GenAI Semantic Conventions](../agent-sessions/agent-session-trace-formats.md)
