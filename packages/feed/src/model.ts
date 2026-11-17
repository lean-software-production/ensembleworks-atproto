export type RecordRow = {uri:string; cid:string; authorDid?:string; value:unknown};
type Obj = Record<string, any>;
const object = (v:unknown):Obj => v !== null && typeof v === 'object' && !Array.isArray(v) ? v : {};
const str = (v:unknown):string => typeof v === 'string' ? v : '';
const authorOf = (row:RecordRow)=>row.authorDid || row.uri.split('/').filter(part=>part.startsWith('did:')).at(-1) || 'Unknown author';
export function sessionsFromRecords(rows:RecordRow[], names:Record<string,string> = {}) {
  const sessions = new Map<string, any>();
  const streamSessions = new Map<string,Set<string>>();
  for (const row of rows) {
    const value=object(row.value);
    if (value.streamId && value.sessionId) {
      const streamKey=`${authorOf(row)}/${value.streamId}`;
      if(!streamSessions.has(streamKey)) streamSessions.set(streamKey,new Set());
      streamSessions.get(streamKey)!.add(value.sessionId);
    }
  }
  for (const row of rows) {
    const value = object(row.value);
    let native:unknown = row.value;
    try { if (typeof value.payloadJson === 'string') native = JSON.parse(value.payloadJson); } catch { native = value.payloadJson; }
    const p = object(native);
    const authorDid = authorOf(row);
    const candidates=streamSessions.get(`${authorDid}/${value.streamId}`);
    const inferredSession=candidates?.size===1?[...candidates][0]:'';
    const id = str(value.sessionId) || str(p.sessionId) || inferredSession || str(value.streamId) || row.uri;
    const key = `${authorDid}/${id}`;
    if (!sessions.has(key)) sessions.set(key,{key,id,authorDid,author:names[authorDid] || authorDid,events:[]});
    sessions.get(key).events.push({ ...row, native, envelope:value, type:str(value.nativeType)||str(p.type)||str(value.$type)||'Unknown event', time:str(value.occurredAt)||str(p.timestamp)||str(value.capturedAt), stream:str(value.streamId), order:Number.isFinite(value.sourceOrder)?value.sourceOrder:Number.isFinite(value.sourceLine)?value.sourceLine:0 });
  }
  for (const session of sessions.values()) {
    // Timestamp establishes a cross-stream chronology. Source order resolves ties;
    // missing timestamps remain inspectable and use stable source order.
    session.events.sort((a:any,b:any)=>a.time.localeCompare(b.time)||a.stream.localeCompare(b.stream)||a.order-b.order||a.uri.localeCompare(b.uri));
    session.startTime = session.events.find((e:any)=>e.time)?.time || '';
    let customTitle='',generatedTitle='',fallbackTitle='';
    session.title = 'Untitled session'; session.project = ''; session.prompt = '';
    for (const event of session.events) {
      const p = object(event.native);
      customTitle = str(p.customTitle)||customTitle;
      generatedTitle = str(p.aiTitle)||generatedTitle;
      fallbackTitle = str(p.title)||str(p.summary)||fallbackTitle;
      session.title = customTitle||generatedTitle||fallbackTitle||'Untitled session';
      session.project = str(p.cwd)||str(p.project)||str(p.repo)||session.project;
      const message = object(p.message);
      if (!session.prompt && (p.type === 'user' || message.role === 'user')) {
        const content = message.content ?? p.content;
        session.prompt = typeof content === 'string' ? content : Array.isArray(content) ? content.filter((x:any)=>x?.type==='text').map((x:any)=>str(x.text)).join('\n') : '';
      }
    }
  }
  return [...sessions.values()].sort((a,b)=>b.startTime.localeCompare(a.startTime)||a.key.localeCompare(b.key));
}
export async function readAllRecords(transport:{listEvents:(opts:{cursor?:string;limit:number})=>Promise<{records:RecordRow[];cursor?:string}>}) {
  const records = new Map<string,RecordRow>(); const seen = new Set<string>(); let cursor:string|undefined;
  for (let page=0;page<10000;page++) {
    const result = await transport.listEvents({cursor,limit:100});
    for (const row of result.records) records.set(row.uri,row);
    if (!result.cursor) return [...records.values()];
    if (seen.has(result.cursor)) throw new Error('PDS pagination repeated a cursor');
    seen.add(result.cursor); cursor=result.cursor;
  }
  throw new Error('PDS pagination limit reached; incomplete snapshot rejected');
}
