---
title: Chapitre 1 — Suites arithmétiques et géométriques
permalink: /classes/tale-techno-commun/chapitre1/
hero_title: Chapitre 1
hero_subtitle: Suites arithmétiques et géométriques
cours:
- titre: Cours — Version élève
  pdf: tale-techno/tale-techno-commun-ch1-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: tale-techno/tale-techno-commun-ch1-cours-prof.pdf
- titre: Cours complet
  fichier: /assets/pdf/tale-techno/tale-techno-commun-ch1-cours.pdf
planches:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch1-planche-01.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch1-planche-02.pdf
dm:
- num: 1
  contenu: Suite arithmétique · Somme de termes · Modélisation
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch1-dm-01-sujet.pdf
- num: 2
  contenu: Suite géométrique · Somme de termes · Problème ouvert
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch1-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: Suites arithmétiques · Suites géométriques · Sens de variation
  duree: "2 h"
  pdf: tale-techno/tale-techno-commun-ch1-dsblanc-01-sujet.pdf
- num: 2
  contenu: Suites arithmétiques et géométriques · Sommes · Python
  duree: "2 h"
  pdf: tale-techno/tale-techno-commun-ch1-dsblanc-02-sujet.pdf
ds_published: true
ds:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch1-ds-01-sujet.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch1-ds-02-sujet.pdf
- num: 3
  pdf: tale-techno/tale-techno-commun-ch1-ds-03-sujet.pdf
python:
- titre: "Sommes de termes et symbole Σ"
  fichier: /assets/python/tale-techno-commun/ch1-sommes-suites.ipynb
  duree: "35 min"
  contenu: "Sommes de carrés, de cubes et d'inverses · Versements réguliers"
erreurs:
- "Confondre suite arithmétique et suite géométrique : on ajoute $r$ dans un cas, on multiplie par $q$ dans l'autre"
- "Écrire $u_n = u_0 \\times q \\times n$ pour une suite géométrique : le terme général est $u_n = u_0 \\times q^n$ (une puissance)"
- "Calculer $u_{n+1} - u_n$ pour reconnaître une suite géométrique : on calcule $\\dfrac{u_{n+1}}{u_n}$"
- "Se tromper de formule : $u_n = u_0 + nr$, mais $u_n = u_1 + (n - 1)r$ si la suite commence à $u_1$"
- "Confondre le rang $n$ et le terme $u_n$ : le rang est l'indice, le terme est la valeur"
- "Croire qu'une suite géométrique de raison $0 < q < 1$ finit par s'annuler : ses termes se rapprochent de 0 sans l'atteindre"
- "Se tromper de nombre de termes dans $S = (\\text{nombre de termes}) \\times \\dfrac{\\text{premier} + \\text{dernier}}{2}$"
liens:
- nom: Khan Academy — Suites arithmétiques
  desc: Cours vidéo complet sur les suites arithmétiques avec exemples
  url: "https://fr.khanacademy.org/math/algebra/x2f8bb11595b61c86:sequences/x2f8bb11595b61c86:introduction-to-arithmetic-sequences/v/arithmetic-sequences"
  ico: 📚
  cat: cours
- nom: Khan Academy — Suites géométriques
  desc: Comprendre les suites géométriques et leur convergence
  url: "https://fr.khanacademy.org/math/algebra/x2f8bb11595b61c86:sequences/x2f8bb11595b61c86:introduction-to-geometric-sequences/v/geometric-sequences-introduction"
  ico: 📚
  cat: cours
- nom: GeoGebra — Suites interactives
  desc: "Visualiser les termes d'une suite et son comportement asymptotique"
  url: "https://www.geogebra.org/m/ksphynmp"
  ico: 📐
  cat: calcul
- nom: Wolfram Alpha — Suites
  desc: "Calculer les termes, la somme et la limite d'une suite"
  url: "https://www.wolframalpha.com/input?i=sequence"
  ico: 🔢
  cat: calcul
---
{% include cours-cards.html %}
