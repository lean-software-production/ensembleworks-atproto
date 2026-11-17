import { createHash } from 'node:crypto';
import { Lexicons, type LexiconDoc } from '@atproto/lexicon';
import eventLexicon from '../lexicons/com.ensembleworks.session.event.json' with { type: 'json' };
import chunkLexicon from '../lexicons/com.ensembleworks.session.chunk.json' with { type: 'json' };
import manifestLexicon from '../lexicons/com.ensembleworks.session.chunkManifest.json' with { type: 'json' };
import companySpaceLexicon from '../lexicons/com.ensembleworks.company.json' with { type: 'json' };
export { eventLexicon, chunkLexicon, manifestLexicon, companySpaceLexicon };
export const EVENT_COLLECTION = 'com.ensembleworks.session.event';
export const MAX_PAYLOAD_BYTES = 16 * 1024 * 1024;
export interface EventRecord extends Record<string, unknown> {
  $type: typeof EVENT_COLLECTION;
  schemaVersion: 1;
  harness: string;
  sourceKind: 'jsonl';
  streamId: string;
  sourcePath: string;
  sourceLine: number;
  sourceOrder: number;
  identityKind: 'native-uuid' | 'content';
  payloadEncoding: 'json';
  payloadJson: string;
  payloadDigest: string;
  capturedAt: string;
  sessionId?: string;
  nativeId?: string;
  nativeType?: string;
  parentId?: string;
  occurredAt?: string;
  harnessVersion?: string;
}
const lexicons = new Lexicons([eventLexicon, chunkLexicon, manifestLexicon, companySpaceLexicon] as LexiconDoc[]);
export function validateLexiconRecord(id: string, value: unknown) {
  if (id === EVENT_COLLECTION) {
    const fragment = value && typeof value === 'object' && 'transportType' in value ? 'chunkManifest' : 'native';
    return lexicons.validate(`${id}#${fragment}`, value);
  }
  return lexicons.validate(id, value);
}
export function validateEvent(value: unknown) { return lexicons.validate(`${EVENT_COLLECTION}#native`, value); }
export function assertEvent(value: unknown): asserts value is EventRecord {
  const result = validateEvent(value);
  if (!result.success) throw new Error(`Invalid event: ${result.error.message}`);
  const record = value as EventRecord;
  if (Buffer.byteLength(record.payloadJson, 'utf8') > MAX_PAYLOAD_BYTES) throw new Error('Payload exceeds 16777216 UTF-8 bytes; retained for retry, no truncation');
  JSON.parse(record.payloadJson);
  if (digest(record.payloadJson) !== record.payloadDigest) throw new Error('Payload digest mismatch');
}
export function digest(value: string) { return createHash('sha256').update(value).digest('hex'); }
export function createEvent(input: {payloadJson: string; sourcePath: string; sourceLine: number; namespace: string; streamPath?: string; occurrence?: number; capturedAt?: string}): {rkey: string; record: EventRecord} {
  const native = JSON.parse(input.payloadJson);
  const field = (key: string): string | undefined => native && typeof native === 'object' && typeof native[key] === 'string' ? native[key] : undefined;
  const streamId = digest(JSON.stringify([input.namespace, input.streamPath ?? input.sourcePath]));
  const payloadDigest = digest(input.payloadJson);
  const nativeId = field('uuid');
  const identity = nativeId ? ['uuid', nativeId] : ['content', payloadDigest, input.occurrence ?? 0];
  const rkey = digest(JSON.stringify([streamId, ...identity]));
  const record: EventRecord = {
    $type: EVENT_COLLECTION, schemaVersion: 1, harness: 'claude-code', sourceKind: 'jsonl', streamId,
    sourcePath: input.sourcePath, sourceLine: input.sourceLine, sourceOrder: input.sourceLine - 1,
    identityKind: nativeId ? 'native-uuid' : 'content', payloadEncoding: 'json', payloadJson: input.payloadJson,
    payloadDigest, capturedAt: input.capturedAt ?? new Date().toISOString(),
  };
  for (const [target, source] of Object.entries({nativeId:'uuid',nativeType:'type',sessionId:'sessionId',parentId:'parentUuid',occurredAt:'timestamp',harnessVersion:'version'})) {
    const value = field(source);
    if (value === undefined || Buffer.byteLength(value) > 4096) continue;
    if (target === 'occurredAt' && (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) || !Number.isFinite(Date.parse(value)))) continue;
    if (value !== undefined) (record as unknown as Record<string, unknown>)[target] = value;
  }
  assertEvent(record);
  return { rkey, record };
}
