// Prints the counts each Players page computes for itself, as JSON, by running the page in jsdom.
// usage: NODE_PATH=<dir with node_modules/jsdom> node scripts/page_stats.js index.html spring-players.html
const { JSDOM } = require('jsdom');
const fs = require('fs'), path = require('path');
const root = path.dirname(__dirname);
const out = {};
for (const f of process.argv.slice(2)) {
  const dom = new JSDOM(fs.readFileSync(path.join(root, f), 'utf8'), { runScripts: 'dangerously', url: 'https://example.test/' + f });
  out[f] = JSON.parse(dom.window.eval(`JSON.stringify({players:DATA.length,teams:[...new Set(DATA.map(r=>r.Team))],
    homes:[...new Set(DATA.map(r=>(r.Home||"").trim()).filter(Boolean))],
    clubs:[...new Set(DATA.flatMap(r=>(r["Club Team"]||"").split(/\\s*;\\s*/).map(s=>s.trim().toLowerCase()).filter(Boolean)))]})`));
}
console.log(JSON.stringify(out));
