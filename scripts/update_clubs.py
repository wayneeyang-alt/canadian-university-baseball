"""Add Spring 2026 counts to the Clubs page.

usage: python3 -I scripts/update_clubs.py <path to the data repo's public/players.json> <path to scripts/club_aliases.json>
Each club card keeps its Fall count in data-f (first run reads it from the card text) and gets a Spring
count in data-s. Cards show "N players" for one season or "N players: F Fall, S Spring" for both, and a
second link to the Spring Players page. Clubs only Spring players list are added as new cards.
Safe to run again after more Spring rosters are merged."""
import json, re, sys, os, html
from urllib.parse import quote_plus
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
players = [p for p in json.load(open(sys.argv[1], encoding='utf-8')) if p.get('Season') == 'Spring 2026']
alias = json.load(open(sys.argv[2], encoding='utf-8'))
spring = {}
for p in players:
    for c in re.split(r'\s*;\s*|\s+/\s+', p['Club Team'].strip()):
        c = alias.get(c, c).strip()
        if c:
            spring[c] = spring.get(c, 0) + 1
s = open(os.path.join(ROOT, 'clubs.html'), encoding='utf-8').read()
m = re.search(r'(<ul class="tg" id="list">)(.*?)(</ul>\n<div class="note">)', s, re.S)
cards = re.findall(r'<li class="tc".*?</li>', m.group(2), re.S)
key = lambda n: re.sub(r'\s+', ' ', n.lower()).strip()
want = {key(k): (k, v) for k, v in spring.items()}
out = []
seen = set()
for c in cards:
    name = html.unescape(re.search(r'<h3>(.*?)</h3>', c).group(1))
    f = re.search(r'data-f="(\d+)"', c)
    f = int(f.group(1)) if f else int(re.search(r'<div class="tn">(\d+) player', c).group(1))
    sp = want.get(key(name), (None, 0))[1]
    seen.add(key(name))
    out.append((f, sp, name, c))
def tn(f, sp):
    t = f + sp
    base = f'{t} player' + ('' if t == 1 else 's')
    return base if not (f and sp) else f'{base}: {f} Fall, {sp} Spring'
def link(sp, name): return f'<a class="pl" href="./spring-players.html?group=Club+Team&q={quote_plus(name)}">See the Spring players</a>'
final = []
for f, sp, name, c in out:
    c = re.sub(r' data-[fs]="\d+"', '', c)
    c = re.sub(r'<li class="tc"', f'<li class="tc" data-f="{f}" data-s="{sp}"', c, count=1)
    c = re.sub(r'<div class="tn">[^<]*</div>', f'<div class="tn">{tn(f, sp)}</div>', c, count=1)
    c = re.sub(r'<a class="pl" href="\./spring-players\.html[^>]*>[^<]*</a>', '', c)
    if f == 0:
        c = re.sub(r'<a class="pl" href="\./\?group[^>]*>[^<]*</a>', '', c)
    if sp:
        c = c.replace('<div class="lk">', '<div class="lk">' + link(sp, name), 1) if f == 0 else re.sub(r'(<a class="pl" href="\./\?group[^>]*>[^<]*</a>)', lambda mm: mm.group(1) + link(sp, name), c, count=1)
    final.append((f + sp, c))
for k, (name, sp) in sorted(want.items()):
    if k not in seen:
        nm = html.escape(name)
        final.append((sp, f'<li class="tc" data-n="{k}" data-f="0" data-s="{sp}"><h3>{nm}</h3><div class="tn">{tn(0, sp)}</div><div class="lk">{link(sp, name)}</div></li>'))
final.sort(key=lambda x: -x[0])
body = ''.join(c for _, c in final)
s = s[:m.start(2)] + body + s[m.end(2):]
s = re.sub(r'id="c">\d+ clubs', f'id="c">{len(final)} clubs', s)
s = s.replace('A player who lists more than one club is counted under each.', 'A player who lists more than one club is counted under each. Counts cover Fall 2026 and Spring 2026 rosters.') if 'Spring 2026 rosters.' not in s else s
open(os.path.join(ROOT, 'clubs.html'), 'w', encoding='utf-8').write(s)
print(len(final), 'clubs;', sum(1 for f, sp, *_ in out if sp), 'existing clubs gained Spring players;', len(final) - len(out), 'new')
