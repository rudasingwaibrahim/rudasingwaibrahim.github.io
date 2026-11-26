#!/usr/bin/env python3
"""Vignettes des PDF du site Σ Sigma.

Pour chaque PDF de assets/pdf/, crée une vignette WebP de la première page
(300 px de large) dans assets/thumbs/ (même arborescence) et met à jour
_data/pdf_pages.yml (nombre de pages de chaque PDF), utilisé par les cartes.

Utilisation, depuis la racine du dépôt, après avoir ajouté des PDF :
    python3 tools/vignettes.py            # traite les PDF nouveaux ou modifiés
    python3 tools/vignettes.py --tout     # régénère toutes les vignettes

Prérequis : poppler-utils (pdftoppm, pdfinfo) et Pillow (pip install Pillow).
"""
import os, sys, subprocess, tempfile, re
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(RACINE, 'assets', 'pdf')
THUMBS = os.path.join(RACINE, 'assets', 'thumbs')
DATA = os.path.join(RACINE, '_data', 'pdf_pages.yml')
LARGEUR, QUALITE = 300, 62

def pages(chemin):
    try:
        out = subprocess.run(['pdfinfo', chemin], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r'^Pages:\s+(\d+)', out, re.M)
        return int(m.group(1)) if m else None
    except Exception:
        return None

def vignette(chemin, sortie):
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, 'p')
        subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-png', '-scale-to-x', str(LARGEUR * 2), '-scale-to-y', '-1', chemin, base],
                       check=True, capture_output=True, timeout=120)
        png = [f for f in os.listdir(tmp) if f.endswith('.png')][0]
        im = Image.open(os.path.join(tmp, png)).convert('RGB')
        h = round(im.height * LARGEUR / im.width)
        im = im.resize((LARGEUR, h), Image.LANCZOS)
        os.makedirs(os.path.dirname(sortie), exist_ok=True)
        im.save(sortie, 'WEBP', quality=QUALITE, method=6)

def main():
    tout = '--tout' in sys.argv
    nb, data = 0, {}
    for d, _, fichiers in os.walk(PDF):
        for f in sorted(fichiers):
            if not f.lower().endswith('.pdf'):
                continue
            chemin = os.path.join(d, f)
            rel = os.path.relpath(chemin, PDF)
            cle = '/assets/pdf/' + rel.replace(os.sep, '/')
            n = pages(chemin)
            if n:
                data[cle] = n
            sortie = os.path.join(THUMBS, os.path.splitext(rel)[0] + '.webp')
            if tout or not os.path.exists(sortie) or os.path.getmtime(sortie) < os.path.getmtime(chemin):
                try:
                    vignette(chemin, sortie); nb += 1
                except Exception as e:
                    print('échec :', rel, e)
    with open(DATA, 'w', encoding='utf-8') as fh:
        fh.write('# Nombre de pages de chaque PDF — généré par tools/vignettes.py, ne pas modifier à la main.\n')
        for k in sorted(data):
            fh.write('"%s": %d\n' % (k.replace('"', '\\"'), data[k]))
    print(f'{nb} vignette(s) créée(s), {len(data)} PDF recensés.')

if __name__ == '__main__':
    main()
