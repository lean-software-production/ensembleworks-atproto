import { spawn } from 'node:child_process';
import { open, readFile, readdir, rename, mkdir } from 'node:fs/promises';
import { resolve, relative, dirname, join, sep } from 'node:path';
import { createEvent, digest, type EventRecord } from '@ensemble/protocol';
export interface Transport { putEvent(rkey: string, record: EventRecord): Promise<{uri: string; cid: string}> }
export interface WatchOptions {
  dir: string; stateFile: string; namespace: string; destination: string; transport: Transport;
  report?: (issue: Issue) => void;
}
export interface Issue { kind: 'malformed' | 'publish' | 'source' | 'invalid'; sourcePath?: string; line?: number; message: string }
interface Entry { record: EventRecord; signature: string; publishedSignature?: string; uri?: string; cid?: string; attempts: number; error?: string }
interface Ledger { version: 1; binding: string; entries: Record<string, Entry>; issues?: Issue[] }
export interface ScanResult { files: number; completeLines: number; published: number; unchanged: number; partialFiles: number; issues: Issue[] }
// util-linux flock holds an OS advisory lock. The helper exits when its stdin pipe
// closes, including SIGKILL of the watcher. Lockfile existence is never ownership.
async function acquireLock(path: string): Promise<() => Promise<void>> {
  const child = spawn('flock', ['--exclusive','--nonblock',path,process.execPath,'-e',
    "process.stdout.write('locked\\n'); process.stdin.resume(); process.stdin.on('end',()=>process.exit(0));"], {stdio:['pipe','pipe','pipe']});
  const exited = new Promise<void>(resolve => child.once('exit',()=>resolve()));
  await new Promise<void>((resolve,reject) => {
    child.once('error',()=>reject(new Error('Cannot acquire checkpoint lock; util-linux flock is required')));
    child.once('exit',()=>reject(new Error('Checkpoint is locked by another watcher')));
    child.stdout.once('data',()=>resolve());
  });
  return async () => { child.stdin.end(); await exited; };
}
async function save(path: string, ledger: Ledger) {
  const temporary = `${path}.tmp`;
  const handle = await open(temporary, 'w', 0o600);
  try { await handle.writeFile(JSON.stringify(ledger)); await handle.sync(); } finally { await handle.close(); }
  await rename(temporary, path);
  const directory = await open(dirname(path), 'r');
  try { await directory.sync(); } finally { await directory.close(); }
}
async function* files(dir: string, report: (path: string, error: unknown) => void): AsyncGenerator<string> {
  const children = await readdir(dir, { withFileTypes: true }).catch(error => {
    report(dir, error);
    return [];
  });
  children.sort((a,b) => b.name.localeCompare(a.name, undefined, {numeric:true}));
  for (const child of children) {
    const path = join(dir, child.name);
    // Do not follow symlinks out of an explicitly selected source directory.
    if (child.isDirectory()) yield* files(path, report);
    else if (child.isFile() && /\.jsonl(?:\.\d+)?$/.test(child.name)) yield path;
  }
}
function signature(record: EventRecord) { const { capturedAt, ...stable } = record; return digest(JSON.stringify(stable)); }
/** Full reconciliation deliberately avoids mtime/offset-only cursors: files can be rewritten. */
export async function runOnce(options: WatchOptions): Promise<ScanResult> {
  const dir = resolve(options.dir), stateFile = resolve(options.stateFile);
  await mkdir(dirname(stateFile), {recursive: true});
  const releaseLock = await acquireLock(`${stateFile}.lock`);
  try {
    const binding = digest(JSON.stringify([dir, options.namespace, options.destination]));
    let ledger: Ledger;
    try {
      ledger = JSON.parse(await readFile(stateFile, 'utf8'));
      if (ledger.version !== 1 || ledger.binding !== binding || !ledger.entries) throw new Error('Checkpoint version/destination/source mismatch');
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
      ledger = { version: 1, binding, entries: {} };
    }
    const result: ScanResult = {files: 0, completeLines: 0, published: 0, unchanged: 0, partialFiles: 0, issues: []};
    const issue = (value: Issue) => { result.issues.push(value); options.report?.(value); };
    const candidates = new Map<string, EventRecord>();
    for await (const path of files(dir, (path, error) => issue({
      kind:'source', sourcePath:relative(dir,path).split(sep).join('/') || '.',
      message:`Source directory read failed: ${(error as NodeJS.ErrnoException).code ?? 'unknown'}; will rescan`,
    }))) {
      if (resolve(path) === stateFile) continue;
      result.files++;
      const sourcePath = relative(dir, path).split(sep).join('/');
      let bytes: Buffer;
      try { bytes = await readFile(path); } catch (error) { issue({kind:'source',sourcePath,message:`Source read failed: ${(error as NodeJS.ErrnoException).code ?? 'unknown'}`}); continue; }
      const lastNewline = bytes.lastIndexOf(10);
      if (lastNewline < bytes.length - 1) result.partialFiles++;
      if (lastNewline < 0) continue;
      // Fatal UTF-8 decoding avoids replacing corrupt bytes with U+FFFD silently.
      const lines = bytes.subarray(0,lastNewline).toString('binary').split('\n');
      const occurrences = new Map<string, number>();
      for (let i = 0; i < lines.length; i++) {
        const raw = Buffer.from(lines[i], 'binary');
        let payloadJson: string;
        try { payloadJson = new TextDecoder('utf-8', {fatal: true, ignoreBOM: true}).decode(raw); JSON.parse(payloadJson); }
        catch { issue({kind:'malformed',sourcePath,line:i+1,message:'Invalid JSON or UTF-8 in completed line; retained in source and rescanned'}); continue; }
        result.completeLines++;
        const hash = digest(payloadJson), occurrence = occurrences.get(hash) ?? 0;
        occurrences.set(hash, occurrence + 1);
        try {
          const {rkey, record} = createEvent({payloadJson,sourcePath,sourceLine:i+1,namespace:options.namespace,streamPath:sourcePath.replace(/\.jsonl\.\d+$/, '.jsonl'),occurrence});
          candidates.set(rkey, record);
        } catch (error) { issue({kind:'invalid',sourcePath,line:i+1,message:(error as Error).message}); }
      }
    }
    for (const [rkey, record] of candidates) {
      const previous = ledger.entries[rkey], nextSignature = signature(record);
      if (previous?.signature === nextSignature) { result.unchanged++; continue; }
      ledger.entries[rkey] = {record,signature:nextSignature,publishedSignature:previous?.publishedSignature,uri:previous?.uri,cid:previous?.cid,attempts:0};
    }
    // Persist pending records BEFORE publication, so an ambiguous response can be retried with
    // exactly the same rkey and bytes, even when the source later disappears.
    ledger.issues = result.issues;
    await save(stateFile,ledger);
    for (const [rkey, entry] of Object.entries(ledger.entries)) {
      if (entry.publishedSignature === entry.signature) continue;
      entry.attempts++;
      try {
        const written = await options.transport.putEvent(rkey,entry.record);
        entry.uri = written.uri; entry.cid = written.cid; entry.publishedSignature = entry.signature; delete entry.error;
        result.published++;
      } catch {
        // Transport exceptions may contain credentials or native payload. Keep output metadata-only.
        entry.error = 'Publication failed; pending record retained for retry';
        issue({kind:'publish',sourcePath:entry.record.sourcePath,line:entry.record.sourceLine,message:entry.error});
      }
      await save(stateFile,ledger);
    }
    return result;
  } finally { await releaseLock(); }
}
export async function watchDirectory(options: WatchOptions & {intervalMs?: number; maxRetryMs?: number; signal?: AbortSignal; onScan?: (result: ScanResult) => void}) {
  const interval = options.intervalMs ?? 1000, maximum = options.maxRetryMs ?? 30000;
  if (!Number.isFinite(interval) || interval < 10 || !Number.isFinite(maximum) || maximum < interval) throw new Error('Invalid polling/backoff interval');
  let delay = interval;
  while (!options.signal?.aborted) {
    const result = await runOnce(options); options.onScan?.(result);
    delay = result.issues.some(issue => issue.kind === 'publish' || issue.kind === 'source') ? Math.min(maximum,delay * 2) : interval;
    if (options.signal?.aborted) break;
    await new Promise<void>(done => {
      const finish = () => { clearTimeout(timer); options.signal?.removeEventListener('abort',finish); done(); };
      const timer = setTimeout(finish,delay);
      options.signal?.addEventListener('abort',finish,{once:true});
    });
  }
}
