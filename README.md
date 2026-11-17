# Ensembleworks ATProto

The prototype watches Claude session JSONL files, preserves native events in a company ATProto Space on Bluesky's TypeScript PDS, and displays a live web feed.

## Start the local prototype

Prerequisites: Node **24**, npm, and Docker with **Compose v2** (Docker Desktop on macOS/Windows, or Docker Engine on Linux). Run the watcher in Docker using the commands below; the image supplies Linux `flock` for crash-safe locking. Native watcher mode requires Linux `flock` from **util-linux**. Container image and package pins are listed in the [infrastructure runbook](docs/prototype-infrastructure.md).

From the repository root:

```sh
npm ci --cache /tmp/ensembleworks-npm
node infra/init.mjs
npm run up
npm run demo:seed
npm run demo:once -- --docker
npm run demo:watch -- --docker
```

`init` creates ignored local secrets **before Compose reads its env files**. `up` also calls init itself, waits for the real PDS, bootstraps the local company Space and pilot accounts, and starts the feed. `demo:seed` copies repository synthetic fixtures only when absent and writes an Alice transport config; it preserves existing demo data. `demo:watch` stays in the foreground. No personal session directory is selected automatically.

The `--docker` watcher uses the same Compose network as the PDS and a separate `.local/demo-docker-state.json` checkpoint. Omit `--docker` on Linux to run it directly on the host. Startup respects your Docker context and `DOCKER_CONFIG` rather than replacing Docker Desktop settings. The Docker watcher path has been tested on this Linux server; macOS/Windows host behavior has not been independently tested.

The pinned PDS image is AMD64-only. Compose requests `linux/amd64` explicitly; Apple Silicon needs Docker Desktop's x86 emulation enabled. The other services use their native platform.

Open **http://localhost:3100**. Open `.local/feed.env` in your **local editor** and copy the `FEED_LOGIN_PASSWORD` value directly into the login form. Do not paste the file or password into agent chat or a shared transcript. PDS/account passwords stay in ignored `.local/accounts.json`; the feed login is separate.

On the current server, the ignored `compose.override.yaml` also binds the feed to its Tailscale address: **http://100.124.90.17:3100**. Compose loads this machine-specific override automatically; other checkouts retain the localhost default.

In a second terminal, while the demo watcher runs:

```sh
npm run demo:append
```

The new synthetic event appears as Alice in `synthetic-session` on the feed's next refresh. Demo source, checkpoint, and writer configuration live under `.local`, so reruns and restarts do not depend on temporary directories. After stopping a watch with Ctrl-C, `npm run demo:once` or `npm run demo:watch` resumes without duplicate records.

## Watch a folder you explicitly choose

After `demo:seed` has generated the local pilot writer config, select a directory you intend to share with company members:

```sh
npm run start -w @ensemble/cli -- once --dir "/absolute/path/you-selected" --config .local/demo-writer.json --state .local/selected-state.json --namespace selected-folder-pilot
npm run start -w @ensemble/cli -- watch --dir "/absolute/path/you-selected" --config .local/demo-writer.json --state .local/selected-state.json --namespace selected-folder-pilot
```

These commands use the Alice pilot account. Native contents are preserved, including tool output and unknown events; select synthetic or intentionally shared logs. See the [watcher runbook](docs/claude-watcher.md) for another account, malformed lines, rotation, limits, and retry behavior.

## Stop and resume

Stop the foreground watcher with Ctrl-C, then:

```sh
docker compose stop
# Later:
npm run up
npm run demo:watch
```

Keep `.local` and the `pds-data`/`plc-data` Docker volumes: they hold credentials, identities, Space records, and watcher state. `docker compose down` also preserves volumes; `down -v` intentionally deletes persisted server data and is not a normal restart command. `npm run up` was verified on the existing stack, and independent tests verified exact values/CIDs after restarting Postgres, PLC, PDS and feed.

See the [infrastructure runbook](docs/prototype-infrastructure.md) for auth boundaries, version pins, limits and evidence; the [acceptance test instructions](tests/acceptance/README.md) for end-to-end commands; and the [independent review](docs/prototype-review.md) for results.

See the [knowledge base index](docs/reference/wiki/index.md) for reference articles and research findings.

## License

Original project code and documentation are licensed under [MIT](LICENSE).
Third-party source material in `docs/reference/raw/` retains its original
licenses and attribution, recorded in each file. The bundled
[karpathy-llm-wiki skill](.agents/skills/karpathy-llm-wiki/UPSTREAM.md) retains
its [upstream MIT license](.agents/skills/karpathy-llm-wiki/LICENSE).
Third-party material is not relicensed by this project's MIT license.
