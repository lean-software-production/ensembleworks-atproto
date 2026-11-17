import {Database, PlcServer} from '@did-plc/server';
const db = Database.postgres({url:process.env.DATABASE_URL});
await db.migrateToLatestOrThrow();
const server = PlcServer.create({db, port:2582});
await server.start();
console.log('Local PLC listening on 2582');
