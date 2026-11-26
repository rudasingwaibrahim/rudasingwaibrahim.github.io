#!/usr/bin/env python3
"""Recopie le moteur des devoirs (tools/devoirs/moteur.js, source unique) :
   - dans tools/devoirs/Code.gs, entre les marqueurs « DÉBUT / FIN MOTEUR SIGMA » (serveur) ;
   - dans _includes/devoirs/moteur-demo.js (mode démo du site, protégé de Liquid par raw).
Usage : python3 tools/devoirs/sync.py [--check]  (--check : échoue si une copie n'est pas à jour)."""
import os, re, sys
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
D, F = '/* ==== DÉBUT MOTEUR SIGMA ====', '/* ==== FIN MOTEUR SIGMA ==== */'
moteur = open(os.path.join(ICI, 'moteur.js'), encoding='utf-8').read().strip() + '\n'
assert moteur.startswith(D) and moteur.rstrip().endswith(F), 'marqueurs absents de moteur.js'
gs_p = os.path.join(ICI, 'Code.gs')
gs = open(gs_p, encoding='utf-8').read()
i, j = gs.index(D), gs.index(F) + len(F)
gs2 = gs[:i] + moteur.rstrip() + gs[j:]
demo_p = os.path.join(RACINE, '_includes', 'devoirs', 'moteur-demo.js')
demo = ('{%- comment -%} Copie générée par tools/devoirs/sync.py — ne pas modifier. Incluse seulement en mode démo. {%- endcomment -%}\n'
        '{% raw %}' + moteur + '{% endraw %}\n')
if '{% endraw' in moteur: sys.exit('moteur.js ne doit pas contenir « endraw »')
if '--check' in sys.argv:
    ok = gs2 == gs and os.path.exists(demo_p) and open(demo_p, encoding='utf-8').read() == demo
    print('copies à jour' if ok else 'COPIES PÉRIMÉES : lancer python3 tools/devoirs/sync.py'); sys.exit(0 if ok else 1)
open(gs_p, 'w', encoding='utf-8').write(gs2)
os.makedirs(os.path.dirname(demo_p), exist_ok=True)
open(demo_p, 'w', encoding='utf-8').write(demo)
print('Code.gs et _includes/devoirs/moteur-demo.js mis à jour')
