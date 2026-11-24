// Construit une version « fichier unique » (JS et CSS intégrés) pour publier l'app comme page web.
import { build } from 'vite';
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

process.env.SINGLE_FILE = '1';
const outDir = 'dist-single';
await build({
  logLevel: 'warn',
  build: {
    outDir,
    emptyOutDir: true,
    modulePreload: { polyfill: false },
  },
});

const assets = join(outDir, 'assets');
const files = readdirSync(assets);
const read = (ext) =>
  files
    .filter((f) => f.endsWith(ext))
    .map((f) => readFileSync(join(assets, f), 'utf8'))
    .join('\n');
const js = read('.js').replace(/<\/script/gi, '<\\/script');
const css = read('.css');

const html = `<title>Bourse École</title>
<style>${css}
:root{color-scheme:dark}html,body{background:#0b0f17;color:#e2e8f0}</style>
<div id="root"></div>
<script type="module">${js}</script>
`;
writeFileSync(join(outDir, 'bourse-ecole.html'), html);
console.log(`OK : ${outDir}/bourse-ecole.html (${(html.length / 1024).toFixed(0)} Ko)`);
