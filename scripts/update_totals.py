"""Fill the totals block at the top of the Fall and Spring Players pages.

usage: NODE_PATH=<dir containing node_modules/jsdom> python3 -I scripts/update_totals.py <path to the data repo's public/players.json>

Writes, between <!--tot--> and <!--/tot-->, the grand totals across both seasons (large numbers) and one row
per season with that season's own counts. The current page's row is marked aria-current.
 - different players: unique normalized names in the master list (players.json)
 - teams, hometowns: from the data each Players page shows (scripts/page_stats.js runs the pages in jsdom)
 - clubs: the cards on clubs.html (data-f / data-s), so the numbers agree with the Clubs page
Run it after regenerating either page or clubs.html."""
import json, re, os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
master = json.load(open(sys.argv[1], encoding='utf-8'))
key = lambda p: re.sub(r'[^a-z ]', '', (p['First Name'] + ' ' + p['Last Name']).lower()).strip()
players = len({key(p) for p in master})
st = json.loads(subprocess.run(['node', os.path.join(ROOT, 'scripts', 'page_stats.js'), 'index.html', 'spring-players.html'],
                               capture_output=True, text=True, check=True).stdout)
fall, spring = st['index.html'], st['spring-players.html']
clubs_html = open(os.path.join(ROOT, 'clubs.html'), encoding='utf-8').read()
cl_all = len(re.findall(r'data-f=', clubs_html))
cl_f = len(re.findall(r'data-f="[1-9]\d*"', clubs_html))
cl_s = len(re.findall(r'data-s="[1-9]\d*"', clubs_html))
teams = len(set(fall['teams']) | set(spring['teams']))
homes = len(set(fall['homes']) | set(spring['homes']))
grand = ''.join(f'<span><b>{n}</b>{l}</span>' for n, l in [(players, 'players'), (teams, 'teams'), (homes, 'hometowns'), (cl_all, 'clubs')])
def row(name, href, s, clubs, cur):
    c = ' aria-current="page"' if cur else ''
    return (f'<a href="{href}"{c}><b>{name}</b>{s["players"]} players · {len(s["teams"])} teams · '
            f'{len(s["homes"])} hometowns · {clubs} clubs</a>')
for f, cur in (('index.html', 'fall'), ('spring-players.html', 'spring')):
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()
    block = ('<!--tot--><div class="stats" id="stats">' + grand + '</div><nav class="seasons" id="seasons" aria-label="Seasons">'
             + row('Fall 2026', './', fall, cl_f, cur == 'fall')
             + row('Spring 2026', './spring-players.html', spring, cl_s, cur == 'spring') + '</nav><!--/tot-->')
    s2 = re.sub(r'<!--tot-->.*?<!--/tot-->', lambda m: block, s, count=1, flags=re.S)
    assert s2 != s or block in s, 'totals block not found in ' + f
    open(p, 'w', encoding='utf-8').write(s2)
print(f'grand: {players} players, {teams} teams, {homes} hometowns, {cl_all} clubs | Fall {fall["players"]}/{len(fall["teams"])}/{len(fall["homes"])}/{cl_f} | Spring {spring["players"]}/{len(spring["teams"])}/{len(spring["homes"])}/{cl_s}')
