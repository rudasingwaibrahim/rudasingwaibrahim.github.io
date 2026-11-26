#!/usr/bin/env python3
"""Audit mathématique (sympy) de N sujets du DM seconde-ch4-dm1 : réponses justes, une seule bonne réponse
par QCM, pas de valeurs dégénérées, explications cohérentes, rien hors programme.
Usage : python3 tools/devoirs/tests/audit.py [N]   (défaut 300)"""
import json, os, re, subprocess, sys
from collections import Counter
from sympy import isprime, divisors, factorint, Rational, gcd, primerange, integer_nthroot

ICI = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
subprocess.run(['node', os.path.join(ICI, 'dump.js'), str(N), '/tmp/devoirs-audit.json'], check=True)
data = json.load(open('/tmp/devoirs-audit.json'))
err = []
def E(i, q, m): err.append(f'sujet {i} {q}: {m}')
def nb(t): return int(re.sub(r'\\,', '', t))
def num_in(s): return [nb(x) for x in re.findall(r'\d+(?:\\,\d{3})*', s)]
def texfact(n): return ' \\times '.join(f'{p}^{{{e}}}' if e > 1 else str(p) for p, e in sorted(factorint(n).items()))
INTERDIT = re.compile(r'⌊|⌋|lfloor|PGCD|PPCM|pgcd|ppcm|partie entière|modulo|congru|premier(?!s termes)|facteurs premiers|décompos', re.I)
stats = Counter()
for e in data['katexErr']: err.append('KaTeX ' + e)
sigs = set()
for i, S in enumerate(data['sujets']):
    Q = {q['id']: q for q in S['questions']}
    if S['note_parfaite'] != 20: E(i, '-', f"réponses parfaites notées {S['note_parfaite']}")
    if S['note_fausse'] != 0: E(i, '-', f"réponses fausses notées {S['note_fausse']}")
    if sum(q['points'] for q in S['questions']) != 20: E(i, '-', 'total ≠ 20')
    sigs.add(json.dumps([q['enonce'] for q in S['questions']] + [q.get('choix') for q in S['questions']]))
    for q in S['questions']:
        txt = ' '.join(str(q.get(k) or '') for k in ('enonce', 'expl', 'aff', 'aide', 'texte')) + ' '.join(q.get('choix') or [])
        if re.search(r'NaN|undefined|Infinity|null|\[object', txt): E(i, q['id'], 'valeur non définie dans le texte')
        if INTERDIT.search(txt): E(i, q['id'], 'notion hors programme : ' + INTERDIT.search(txt).group(0))
        if txt.count('$') % 2: E(i, q['id'], '$ non appariés')
        if q['type'] == 'qcm':
            if len(set(q['choix'])) != len(q['choix']): E(i, q['id'], 'choix en double')
            if not (0 <= q['bonne'] < len(q['choix'])): E(i, q['id'], 'indice de bonne réponse invalide')
    # Q1 multiple
    q = Q['q1']; a = q['params']['a']; vals = [nb(c.strip('$')) for c in q['choix']]
    ok = [v for v in vals if v % a == 0]
    if len(ok) != 1: E(i, 'q1', f'{len(ok)} multiples de {a} parmi {vals}')
    elif vals[q['bonne']] != ok[0]: E(i, 'q1', 'bonne réponse mal placée')
    if f'multiple de ${a}$' not in q['enonce']: E(i, 'q1', 'a absent de l’énoncé')
    if min(vals) < 2 * a: E(i, 'q1', 'valeur trop petite')
    for v in vals:
        if v != ok[0] and f'{v} = {a} \\times {v // a} + {v % a}' not in q['expl'].replace('\\,', ''): E(i, 'q1', f'division euclidienne de {v} absente/fausse')
    # Q2 impair
    q = Q['q2']; n, k = q['params']['n'], q['params']['k']
    if n % 2 != 1 or n != 2 * k + 1 or q['rep'] != [str(k)] or k < 100: E(i, 'q2', 'impair incohérent')
    if num_in(q['enonce'])[0] != n: E(i, 'q2', 'énoncé ≠ n')
    # Q3 diviseurs
    q = Q['q3']; n = q['params']['n']; d = divisors(n)
    if q['rep'] != [str(len(d))] or not 6 <= len(d) <= 12: E(i, 'q3', f'nombre de diviseurs de {n}')
    lst = [int(x) for x in re.findall(r'\$(\d+)\$', q['expl'].split('sont donc')[1].split(':')[0])]
    if lst != list(d): E(i, 'q3', f'liste des diviseurs fausse {lst}')
    for x, y in re.findall(r'(\d+) \\times (\d+)', q['expl']):
        if int(x) * int(y) != n: E(i, 'q3', f'paire fausse {x}×{y}')
    stats['q3_' + str(len(d))] += 1
    # Q4 plus grand multiple de a inférieur ou égal à b
    q = Q['q4']; a, b, m = q['params']['a'], q['params']['b'], q['params']['m']
    if m != a * (b // a) or q['rep'] != [str(m)] or m % a or m > b or m + a <= b: E(i, 'q4', f'plus grand multiple de {a} ≤ {b} : {m}')
    if b % a == 0: E(i, 'q4', f'{b} multiple de {a} (cas dégénéré)')
    if f'{b} = {a} \\times {b // a} + {b % a}' not in q['expl'].replace('\\,', ''): E(i, 'q4', 'division de b par a absente/fausse')
    if f'{a} \\times {b // a + 1} = {m + a}' not in q['expl'].replace('\\,', ''): E(i, 'q4', 'multiple suivant faux')
    # Q5 démonstration : carré d'un impair
    q = Q['q5']; K, n5, k2 = q['params']['K'], q['params']['n'], q['params']['k2']
    if n5 != 2 * K + 1 or n5 * n5 != 2 * k2 + 1 or k2 != 2 * K * K + 2 * K: E(i, 'q5', 'application fausse')
    if q['trous'][3]['rep'] != [str(k2)] or q['trous'][0]['rep'] != ['4k'] or q['texte'].count('[[') != 4: E(i, 'q5', 'trous faux')
    if f'{n5 * n5} = 2 \\times {k2} + 1' not in q['expl'].replace('\\,', ''): E(i, 'q5', 'vérification absente/fausse')
    # Q6 fraction
    q = Q['q6']; A, B, p_, q_ = (q['params'][k] for k in 'ABpq')
    if Rational(A, B) != Rational(p_, q_) or gcd(p_, q_) != 1 or q['rep'] != [f'{p_}/{q_}']: E(i, 'q6', 'fraction irréductible fausse')
    if p_ < 2 or q_ < 3 or p_ == q_ or A >= 1000 or B >= 1000 or gcd(A, B) < 6: E(i, 'q6', f'{A}/{B} dégénéré')
    g = gcd(A, B)
    if f'${A} = {g} \\times {p_}$ et ${B} = {g} \\times {q_}$' not in q['expl']: E(i, 'q6', 'diviseur commun faux')
    if f'On simplifie par ${g}$' not in q['expl']: E(i, 'q6', 'simplification absente')
    # Q7 parité : force brute sur n = -20..20
    q = Q['q7']; b, c = q['params']['b'], q['params']['c']
    par = {(n * n + b * n + c) % 2 for n in range(-20, 21)}
    vrai = 'depend' if len(par) == 2 else ('pair' if par == {0} else 'impair')
    if vrai != q['params']['verdict']: E(i, 'q7', f'verdict {q["params"]["verdict"]} ≠ {vrai}')
    attendu = {'pair': '$A$ est pair pour tout entier $n$.', 'impair': '$A$ est impair pour tout entier $n$.', 'depend': "La parité de $A$ dépend de l'entier $n$."}[vrai]
    if q['choix'][q['bonne']] != attendu: E(i, 'q7', 'bonne réponse mal placée')
    if sum(1 for ch in q['choix'] if ch == attendu) != 1: E(i, 'q7', 'pas une seule bonne réponse')
    if vrai == 'depend' and not f'$A = {1 + b + c}$' in q['expl']: E(i, 'q7', 'contre-exemple faux')
    stats['q7_' + vrai] += 1
    # Q8 consécutifs
    q = Q['q8']; k, Ssum, g8 = q['params']['k'], q['params']['S'], q['params']['grand']
    if sum(range(g8 - k + 1, g8 + 1)) != Ssum or q['rep'] != [str(g8)] or g8 - k + 1 < 10: E(i, 'q8', 'consécutifs faux')
    if num_in(q['enonce'])[0] != Ssum: E(i, 'q8', 'énoncé ≠ S')
    stats['q8_' + str(k)] += 1
    # Q9 démonstration à trous
    q = Q['q9']; a, p_, q_ = q['params']['a'], q['params']['p'], q['params']['q']
    if p_ == q_ or q['trous'][3]['rep'] != [str(p_ + q_)] or q['trous'][0]['rep'] != [f'{a}m']: E(i, 'q9', 'trous faux')
    if (a * p_ + a * q_) % a or (a * p_ + a * q_) // a != p_ + q_: E(i, 'q9', 'application fausse')
    if q['texte'].count('[[') != 4: E(i, 'q9', 'nombre de trous')
    if f'= {a} \\times {p_ + q_} = ' not in q['expl']: E(i, 'q9', 'explication')
print(f"{len(data['sujets'])} sujets audités ; {len(sigs)} sujets distincts ; répartition : {dict(sorted(stats.items()))}")
print(f'{len(err)} anomalie(s)')
for e in err[:40]: print('  ', e)
sys.exit(1 if err else 0)
