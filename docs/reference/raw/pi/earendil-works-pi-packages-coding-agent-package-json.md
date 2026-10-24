# earendil-works/pi: packages/coding-agent/package.json

> Source: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/package.json
> Resolved: https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/package.json
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode github-blob; 3 response(s) archived in build/reference-wiki/http/github-com-9c7c725a/ (git-ignored): build/reference-wiki/http/github-com-9c7c725a/004.txt (HTTP 200, sha256 0d1b72e3ce28), build/reference-wiki/http/github-com-9c7c725a/005.json (HTTP 200, sha256 1f496309112c), build/reference-wiki/http/github-com-9c7c725a/006.json (HTTP 200, sha256 9e31814be800)
> Extraction: Verbatim file content (raw file at ref `main`; latest commit touching path: 2685de7a1785f1835a9d3d684e16c29789e4eaa8).
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: MIT — earendil-works/pi LICENSE file: MIT License
> Attribution: Copyright (c) 2025 Mario Zechner, earendil-works/pi

```json
{
	"name": "@earendil-works/pi-coding-agent",
	"version": "1.4.0",
	"description": "Coding agent CLI with read, bash, edit, write tools and session management",
	"type": "module",
	"piConfig": {
		"configDir": ".pi"
	},
	"bin": {
		"pi": "dist/bundle/cli.js"
	},
	"main": "./dist/index.js",
	"types": "./dist/index.d.ts",
	"exports": {
		".": {
			"types": "./dist/index.d.ts",
			"import": "./dist/index.js"
		},
		"./rpc-entry": {
			"import": "./dist/bundle/rpc-entry.js"
		}
	},
	"files": [
		"dist",
		"docs",
		"examples",
		"schemas",
		"containerization.md",
		"CHANGELOG.md"
	],
	"scripts": {
		"clean": "shx rm -rf dist",
		"build": "npm run build:unbundled && node ../../scripts/build-coding-agent-bundle.mjs",
		"build:unbundled": "tsc -p tsconfig.build.json && shx chmod +x dist/cli.js dist/rpc-entry.js && npm run copy-assets",
		"build:binary": "npm --prefix ../tui run build && npm --prefix ../telemetry run build && npm --prefix ../ai run build && npm --prefix ../agent run build && npm run build && bun build --compile --no-compile-autoload-bunfig --no-compile-autoload-dotenv ./dist/bun/cli.js ./src/utils/image-resize-worker.ts ./src/extensions/codemode/worker.ts --outfile dist/pi && npm run copy-binary-assets",
		"copy-assets": "shx mkdir -p dist/modes/interactive/theme && shx cp src/modes/interactive/theme/*.json dist/modes/interactive/theme/ && shx mkdir -p dist/modes/interactive/assets && shx cp src/modes/interactive/assets/*.png dist/modes/interactive/assets/ && shx mkdir -p dist/core/export-html/vendor && shx cp src/core/export-html/template.html src/core/export-html/template.css src/core/export-html/template.js dist/core/export-html/ && shx cp src/core/export-html/vendor/*.js dist/core/export-html/vendor/",
		"copy-binary-assets": "shx cp package.json dist/ && shx cp README.md dist/ && shx cp CHANGELOG.md dist/ && shx mkdir -p dist/theme && shx cp src/modes/interactive/theme/*.json dist/theme/ && shx mkdir -p dist/assets && shx cp src/modes/interactive/assets/*.png dist/assets/ && shx mkdir -p dist/export-html/vendor && shx cp src/core/export-html/template.html dist/export-html/ && shx cp src/core/export-html/vendor/*.js dist/export-html/vendor/ && shx cp -r docs dist/ && shx cp -r examples dist/ && shx cp ../../node_modules/@silvia-odwyer/photon-node/photon_rs_bg.wasm dist/",
		"test": "vitest --run",
		"generate:schemas": "node --import ./src/experimental/source-resolver.ts scripts/generate-schemas.ts",
		"generate:references": "node --import ./src/experimental/source-resolver.ts scripts/generate-references.ts",
		"prepublishOnly": "npm run clean && npm run build"
	},
	"dependencies": {
		"@earendil-works/pi-agent-core": "1.4.0",
		"@earendil-works/pi-ai": "1.4.0",
		"@earendil-works/pi-codemode": "1.4.0",
		"@earendil-works/pi-mcp": "1.4.0",
		"@earendil-works/pi-tui": "1.4.0",
		"@silvia-odwyer/photon-node": "0.3.4",
		"brace-expansion": "5.0.12",
		"chalk": "6.0.0",
		"cross-spawn": "7.0.6",
		"diff": "8.0.4",
		"grok-mermaid": "0.2.3",
		"highlight.js": "10.7.3",
		"hosted-git-info": "9.0.3",
		"ignore": "7.0.8",
		"jiti": "2.7.0",
		"minimatch": "10.2.6",
		"proper-lockfile": "4.1.2",
		"quickjs-wasi": "3.6.2",
		"semver": "7.8.5",
		"typebox": "1.3.27",
		"undici": "8.10.2",
		"yaml": "2.9.0"
	},
	"overrides": {
		"protobufjs": "7.6.6"
	},
	"devDependencies": {
		"@types/cross-spawn": "6.0.6",
		"@types/hosted-git-info": "3.0.5",
		"@types/node": "22.19.19",
		"@types/proper-lockfile": "4.1.4",
		"@types/semver": "7.7.1",
		"marked": "18.0.11",
		"shx": "0.3.4",
		"vitest": "4.1.12"
	},
	"keywords": [
		"coding-agent",
		"ai",
		"llm",
		"cli",
		"tui",
		"agent"
	],
	"author": "Mario Zechner",
	"license": "MIT",
	"repository": {
		"type": "git",
		"url": "git+https://github.com/earendil-works/pi.git",
		"directory": "packages/coding-agent"
	},
	"engines": {
		"node": ">=22.19.0"
	}
}
```


## License notice (verbatim, from https://raw.githubusercontent.com/earendil-works/pi/main/LICENSE)

```
MIT License

Copyright (c) 2025 Mario Zechner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
