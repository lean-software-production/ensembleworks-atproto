import {mkdir,writeFile,access} from 'node:fs/promises';
import {randomBytes} from 'node:crypto';
await mkdir('.local',{recursive:true,mode:0o700});
try {await access('.local/pds.env');} catch {
 await writeFile('.local/pds.env',`PDS_JWT_SECRET=${randomBytes(32).toString('hex')}\nPDS_ADMIN_PASSWORD=${randomBytes(32).toString('hex')}\nPDS_PLC_ROTATION_KEY_K256_PRIVATE_KEY_HEX=${randomBytes(32).toString('hex')}\n`,{mode:0o600});
}
try {await access('.local/feed.env');} catch {
 await writeFile('.local/feed.env',`FEED_LOGIN_PASSWORD=${randomBytes(24).toString('base64url')}\nFEED_SESSION_SECRET=${randomBytes(32).toString('hex')}\n`,{mode:0o600});
}
