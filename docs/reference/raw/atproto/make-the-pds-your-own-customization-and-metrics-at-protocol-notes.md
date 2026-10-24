# Make the PDS Your Own: Customization and Metrics - AT Protocol (source notes)

> Source: https://atproto.com/blog/pds-customization-and-metrics
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-04 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Footer: "Copyright (CC-BY) Bluesky Social PBC 2026. All rights reserved." - unversioned CC-BY, ambiguous, treated conservatively. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/atproto-com-4c1bf70e/001.md.
> Work: https://atproto.com/blog/pds-customization-and-metrics
> Quotations: 15 characters verbatim in this file; 15 of 90 allowed for this work across the knowledge base.

## About this source

A release blog post on atproto.com about a reference PDS release (Bluesky Social PBC). No explicit date in the content; it refers back to an account management post from June and a summer PDS to-do list.

## Key facts

- The release has four parts: account-management customization, OpenTelemetry support, bigger default blob sizes, and a fix for the connected-apps list.
- Branding variables for the reference PDS (set in `pds.env`): `PDS_SERVICE_NAME` (defaults to hostname plus "PDS"), `PDS_LOGO_URL`, `PDS_PRIMARY_COLOR`, `PDS_ERROR_COLOR`, `PDS_WARNING_COLOR`, `PDS_INFO_COLOR`, `PDS_SUCCESS_COLOR`, footer links `PDS_HOME_URL`, `PDS_TERMS_OF_SERVICE_URL`, `PDS_PRIVACY_POLICY_URL`, `PDS_SUPPORT_URL`, and auth-screen backgrounds `PDS_BACKGROUND_LIGHT_URL` and `PDS_BACKGROUND_DARK_URL`. Name and logo also appear in transactional emails. The text colour on the primary colour is derived automatically.
- OpenTelemetry for traces, metrics and logs is off by default. Enable with `NODE_OPTIONS`, `OTEL_EXPORTER_OTLP_ENDPOINT` (example `http://localhost:4318`) and `OTEL_SERVICE_NAME`.
- Automatic instrumentation covers inbound and outbound HTTP, the SQLite layer, S3-compatible blob storage, and Node runtime metrics. XRPC spans are normalized by method, for example `GET /xrpc/com.atproto.repo.getRecord`, with the NSID as an attribute.
- Custom counters: `account.created`, `session.created`, `oauth.authorization`.
- A `monitoring/` directory in the reference PDS repo provides a Prometheus, Grafana and node_exporter stack with a "PDS Overview" dashboard; no OpenTelemetry Collector because Prometheus v3 can receive OTLP directly. The post says the sample stack can run in under 1GB of memory and binds to localhost by default.
- Default maximum blob size raised to 300M, mainly for longer videos; this changes what the installer writes to `pds.env`, so existing PDSes must set `PDS_BLOB_UPLOAD_LIMIT=314572800` themselves.
- `com.atproto.server.describeServer` now advertises `blobUploadLimit` (example value 314572800), so clients can split or reject uploads.
- The connected-apps list on the account management page previously could omit sessions not recently refreshed; now fixed, so older entries may reappear.
- Relevance: describes operator-side knobs and observability for a self-hosted PDS, including blob size limits relevant to storing session artifacts.

## Related

- PDS account management post, reference PDS repository `bluesky-social/pds`, atproto data validation guide.
