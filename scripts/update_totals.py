"""Write the all-seasons totals line on the Fall and Spring Players pages.

usage: python3 -I scripts/update_totals.py
Counts rows and programs from the DATA array in index.html (Fall) and spring-players.html (Spring).
Run it after regenerating either page.
"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(f):
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    return json.loads(re.search(r'const DATA=(\[.*?\]);', s, re.S).group(1))
fall, spring = load('index.html'), load('spring-players.html')
players = len(fall) + len(spring)
programs = len({r['Team'] for r in fall} | {r['Team'] for r in spring})
line = (f'<p class="all" id="all">All rosters, Fall 2026 and Spring 2026: <b>{players}</b> players on <b>{programs}</b> teams '
        f'(Fall {len(fall)}, Spring {len(spring)}).</p>')
for f in ('index.html', 'spring-players.html'):
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<p class="all" id="all">.*?</p>', '', s, flags=re.S)
    s = s.replace('<div class="stats" id="stats"></div>', '<div class="stats" id="stats"></div>' + line, 1)
    if 'class=".all"' not in s and '.all{' not in s:
        s = s.replace('.stats b{', '.all{font:400 13px var(--mono);color:var(--muted);margin:10px 0 0}.all b{color:var(--fg)}\n.stats b{', 1)
    open(p, 'w', encoding='utf-8').write(s)
print(f'totals: {players} players, {programs} teams (Fall {len(fall)}, Spring {len(spring)})')
