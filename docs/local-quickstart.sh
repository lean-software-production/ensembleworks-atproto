git clone --branch spike/claude-session-feed https://github.com/lean-software-production/ensembleworks-atproto.git
cd ensembleworks-atproto
npm ci
npm run up
npm run demo:seed
npm run demo:watch -- --docker
