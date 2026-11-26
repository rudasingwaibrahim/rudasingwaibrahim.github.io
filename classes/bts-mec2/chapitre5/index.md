---
title: Chapitre 5 — Calcul vectoriel
permalink: /classes/bts-mec2/chapitre5/
hero_title: Chapitre 5
hero_subtitle: Calcul vectoriel
dossier_pdf: bts-mec2
cours:
- titre: Cours — Version élève
  sub: "Espaces de réponse, tableaux à compléter"
  pdf: bts-mec2-ch5-cours-eleve.pdf
  dossier: bts-mec2
- titre: Cours — Version professeur
  sub: Corrections complètes incluses
  pdf: bts-mec2-ch5-cours-prof.pdf
  dossier: bts-mec2
planches:
- num: 1
  themes: Produit scalaire 2D/3D · Orthogonalité · Polarisation
  pdf: bts-mec2-ch5-planche-01.pdf
- num: 2
  themes: "Équations cartésiennes (droite, plan, cercle) · Distance"
  pdf: bts-mec2-ch5-planche-02.pdf
dm: []
ds_blancs:
- num: 1
  contenu: CCF Blanc Situation 1 — Produit scalaire + équations de droites
  duree: "55 min"
  pdf: bts-mec2-ch5-dsblanc-01-sujet.pdf
- num: 2
  contenu: CCF Blanc Situation 1 — Géométrie 3D + plans + distance
  duree: "55 min"
  pdf: bts-mec2-ch5-dsblanc-02-sujet.pdf
ds_published: false
ds: []
erreurs:
- Confondre produit scalaire (nombre) et produit vectoriel (vecteur)
- "Se tromper de signe dans $\\overrightarrow{AB}\\cdot\\overrightarrow{AC} = \\frac{1}{2}\\left(AB^2 + AC^2 - BC^2\\right)$"
- "Pour la droite $ax + by + c = 0$, confondre vecteur normal $(a\\,;b)$ et vecteur directeur $(-b\\,;a)$"
- Oublier la valeur absolue dans la formule de la distance point-droite/plan
- "Se tromper de signe sur le centre : le cercle $(x - a)^2 + (y - b)^2 = r^2$ a pour centre $(a\\,;b)$"
- "Oublier la troisième coordonnée dans l'espace : $\\vec u\\cdot\\vec v = xx' + yy' + zz'$"
- Conclure que deux vecteurs sont orthogonaux sans vérifier $\vec u\cdot\vec v = 0$
liens:
- nom: GeoGebra — Produit scalaire interactif
  desc: "Visualiser u·v selon l'angle entre vecteurs"
  url: "https://www.geogebra.org/m/yjfHNTKy"
  ico: 📐
  cat: calcul
- nom: GeoGebra — Géométrie 3D
  desc: "Vecteurs, plans, distances en 3D (vue interactive)"
  url: "https://www.geogebra.org/3d"
  ico: 📊
  cat: calcul
- nom: Khan Academy — Vecteurs
  desc: "Cours complet : produit scalaire, orthogonalité, applications"
  url: "https://fr.khanacademy.org/math/algebra-home/alg-vectors"
  ico: 📚
  cat: cours
- nom: "Bibm@th — Calcul vectoriel BTS"
  desc: Cours BTS synthétique avec exercices corrigés
  url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/algebre/vecteurs.html"
  ico: 📝
  cat: cours
---
{% include cours-cards.html %}
