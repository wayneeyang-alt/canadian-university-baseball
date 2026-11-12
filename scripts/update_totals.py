"""Write the all-seasons totals line on the Fall and Spring Players pages.

usage: python3 -I scripts/update_totals.py <path to the data repo's public/players.json>
Counts rows and programs from the DATA array in index.html (Fall) and spring-players.html (Spring).
Run it after regenerating either page.
"""
import json, re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(f):
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    return json.loads(re.search(r'const DATA=(\[.*?\]);', s, re.S).group(1))
fall, spring = load('index.html'), load('spring-players.html')
master = json.load(open(sys.argv[1], encoding='utf-8'))   # the master list: every player, both seasons
def key(p): return re.sub(r'[^a-z ]', '', (p['First Name'] + ' ' + p['Last Name']).lower()).strip()
players = len({key(p) for p in master})
hometowns = len({(p['Hometown'].strip().lower(), p['Province'].strip().lower()) for p in master if p['Hometown'].strip()})
clubs = open(os.path.join(ROOT, 'clubs.html'), encoding='utf-8').read().count('data-f=')
programs = len({r['Team'] for r in fall} | {r['Team'] for r in spring})
line = (f'<p class="all" id="all">All rosters, Fall 2026 and Spring 2026: <b>{players}</b> different players, <b>{programs}</b> teams, '
        f'<b>{hometowns}</b> hometowns, <b>{clubs}</b> clubs (Fall {len(fall)} players, Spring {len(spring)}).</p>')
for f in ('index.html', 'spring-players.html'):
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<p class="all" id="all">.*?</p>', '', s, flags=re.S)
    s = s.replace('<div class="stats" id="stats"></div>', '<div class="stats" id="stats"></div>' + line, 1)
    if 'class=".all"' not in s and '.all{' not in s:
        s = s.replace('.stats b{', '.all{font:400 13px var(--mono);color:var(--muted);margin:10px 0 0}.all b{color:var(--fg)}\n.stats b{', 1)
    open(p, 'w', encoding='utf-8').write(s)
print(f'totals: {players} unique players, {programs} teams, {hometowns} hometowns, {clubs} clubs (Fall {len(fall)}, Spring {len(spring)})')
