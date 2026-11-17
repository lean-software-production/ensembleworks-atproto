import { readFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { homedir } from 'node:os';
import { parseArgs } from 'node:util';
import { createTransport } from '@ensemble/transport';
import { digest } from '@ensemble/protocol';
import { runOnce, watchDirectory } from './watcher.js';

async function main() {
  const {values,positionals} = parseArgs({allowPositionals:true,options:{dir:{type:'string'},state:{type:'string'},config:{type:'string'},namespace:{type:'string'},interval:{type:'string'},help:{type:'boolean'}}});
  if (values.help) { console.log('Usage: npm run start -w @ensemble/cli -- once|watch --dir FOLDER [--state FILE] [--config FILE] [--namespace ID] [--interval MS]\nConfig: service, identifier, password, space. Env overrides: PDS_SERVICE, PDS_IDENTIFIER, PDS_PASSWORD, PDS_SPACE. No default source directory.'); return; }
  const mode = positionals[0];
  if (positionals.length !== 1 || !['once','watch'].includes(mode) || !values.dir) throw new Error('Specify once|watch and an explicit --dir (see --help)');
  const config = values.config ? JSON.parse(await readFile(values.config,'utf8')) : {};
  const settings = {
    service:process.env.PDS_SERVICE ?? config.service,
    identifier:process.env.PDS_IDENTIFIER ?? config.identifier,
    password:process.env.PDS_PASSWORD ?? config.password,
    space:process.env.PDS_SPACE ?? config.space,
  };
  for (const key of ['service','identifier','password','space'] as const) if (typeof settings[key] !== 'string' || !settings[key]) throw new Error(`Missing ${key} in config or PDS_${key.toUpperCase()}`);
  const dir = resolve(values.dir), namespace = values.namespace ?? config.namespace ?? digest(dir);
  const destination = JSON.stringify([settings.service,settings.identifier,settings.space]);
  const stateFile = values.state ?? config.stateFile ?? join(process.env.XDG_STATE_HOME ?? join(homedir(),'.local/state'),'ensemble-watcher',`${digest(JSON.stringify([dir,namespace,destination]))}.json`);
  const options = {dir,stateFile,namespace,destination,transport:createTransport(settings),report:(issue: unknown) => console.error(JSON.stringify(issue))};
  if (mode === 'once') { const result = await runOnce(options); console.log(JSON.stringify(result)); if (result.issues.length) process.exitCode = 1; }
  else {
    const controller = new AbortController();
    const stop = () => controller.abort(); process.once('SIGINT',stop); process.once('SIGTERM',stop);
    try { await watchDirectory({...options,intervalMs:values.interval ? Number(values.interval) : 1000,signal:controller.signal,onScan:result => console.log(JSON.stringify(result))}); }
    finally { process.removeListener('SIGINT',stop); process.removeListener('SIGTERM',stop); }
  }
}
main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : '';
  const safe = /^(Specify once\|watch|Missing (service|identifier|password|space) in config|Checkpoint (is locked|version)|Cannot acquire checkpoint lock|Invalid polling|A company Space URI is required)/.test(message);
  console.error(safe ? message : 'Watcher stopped: check configuration, source directory and checkpoint JSON. No credentials or native payload printed.');
  process.exitCode = 1;
});
