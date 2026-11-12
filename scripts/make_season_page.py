"""Build a season's Players page from the Fall Players page (index.html) used as a template.

usage: python3 -I scripts/make_season_page.py spring data.json
  data.json is a list of rows shaped like the DATA array in index.html
  (Team, Player, Status, Position, Jersey #, Hometown, Province / State / Country,
   Previous School, Club Team, Eligibility / Yr).
Writes spring-players.html. The Fall page itself is index.html and is not touched.
"""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
season, data_path = sys.argv[1], sys.argv[2]
assert season == 'spring', 'only the spring page is generated from the fall template'
raw = json.load(open(data_path, encoding='utf-8'))
# data_path is the data repo's public/players.json; keep only this season's rows and reshape them
# to the DATA rows the page expects.
POS = {'Pitcher': 'P', 'Infielder': 'INF', 'Outfielder': 'OF', 'Catcher': 'C', 'Utility': 'UTL', 'IF': 'INF', 'Infield': 'INF', 'Outfield': 'OF'}
TEAM = {'University of British Columbia': 'UBC Thunderbirds', 'University of the Fraser Valley': 'UFV'}
def pos(v):
    return '/'.join(POS.get(x.strip(), x.strip()) for x in v.split('/')) if v else ''
rows = [{'Team': TEAM.get(p['School'], p['School']), 'Player': (p['First Name'] + ' ' + p['Last Name']).strip(),
         'Status': 'Confirmed in game' if p['Status'] == 'Confirmed' else 'On team roster',
         'Position': pos(p['Position']), 'Jersey #': p['Jersey #'], 'Hometown': p['Hometown'],
         'Province / State / Country': p['Province'], 'Previous School': p['Previous School'],
         'Club Team': p['Club Team'], 'Eligibility / Yr': p['Year']}
        for p in raw if p.get('Season') == 'Spring 2026']
s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
s = re.sub(r'const DATA=\[.*?\];', lambda m: 'const DATA=' + json.dumps(rows, ensure_ascii=False) + ';', s, count=1, flags=re.S)
n = len({r['Team'] for r in rows})
s = s.replace('Fall 2026 rosters for twenty-two university teams', f'Spring 2026 rosters for {n} college and university teams')
s = s.replace('Fall 2026 · Canadian university teams', 'Spring 2026 · Canadian college and university teams')
s = s.replace('Named in a Fall 2026 game report', 'Named in a Spring 2026 game report')
s = s.replace('<title>Canadian University Baseball Players</title>', '<title>Canadian University Baseball Spring Players</title>')
s = s.replace('<a href="./" aria-current="page">Fall Players</a><a href="./spring-players.html">Spring Players</a>', '<a href="./">Fall Players</a><a href="./spring-players.html" aria-current="page">Spring Players</a>')
s = s.replace('This page lists Fall 2026 rosters.', 'This page lists Spring 2026 rosters (March to May).')
s = re.sub(r'Spring rosters are on the <a href="\./spring-players\.html">Spring Players</a> page\.', 'Fall rosters are on the <a href="./">Fall Players</a> page.', s)
s = s.replace('https://wayneeyang-alt.github.io/canadian-university-baseball/"', 'https://wayneeyang-alt.github.io/canadian-university-baseball/spring-players.html"')
open(os.path.join(ROOT, 'spring-players.html'), 'w', encoding='utf-8').write(s)
print('wrote spring-players.html:', len(rows), 'players,', n, 'teams')
