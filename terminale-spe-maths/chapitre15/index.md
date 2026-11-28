---
title: Chapitre 15 — Primitives et équations différentielles
permalink: /classes/terminale-spe-maths/chapitre15/
hero_title: Chapitre 15
hero_subtitle: Primitives — Équations y' = ay et y' = ay + b
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch15-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch15-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch15-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch15-planche-02.pdf
dm_published: true
dm:
- num: 1
  contenu: Primitives composées · Équations différentielles
  duree: 1 semaine
  pdf: terminale-spe-ch15-dm-01.pdf
- num: 2
  contenu: Équations différentielles · Modélisation
  duree: 1 semaine
  pdf: terminale-spe-ch15-dm-02.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Primitives · Équations y' = ay + b
  duree: 4 h
  pdf: terminale-spe-ch15-dsblanc-01.pdf
- num: 2
  contenu: Primitives · Équations différentielles
  duree: 4 h
  pdf: terminale-spe-ch15-dsblanc-02.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch15-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch15-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch15-ds-01.pdf
- num: 2
  pdf: terminale-spe-ch15-ds-02.pdf
- num: 3
  pdf: terminale-spe-ch15-ds-03.pdf
python:
- titre: "Équations différentielles : la méthode d'Euler"
  fichier: /assets/python/terminale-spe-maths/ch15-methode-euler.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch15.py
  duree: "40 min"
  contenu: "Euler pour y′ = f · Euler pour y′ = 3y + 5 · Solution exacte · Erreur selon le pas"
erreurs:
- 'Oublier la constante : si $F$ est une primitive de $f$ sur $I$, toutes les primitives sont $F + k$ avec $k \in \mathbb{R}$'
- 'Croire qu''une primitive de $(5x^3-3)^2$ est $\dfrac{(5x^3-3)^3}{3}$ : la forme $u''u^n$ exige le facteur $u''$ (ici $15x^2$)'
- 'Écrire qu''une primitive de $\dfrac{1}{x}$ est $\ln(x)$ sur $\mathbb{R}^*$ : une primitive se cherche sur un intervalle, ici $]0;+\infty[$'
- 'Se tromper de signe : les solutions de $y'' = ay$ sont $x \mapsto C\mathrm{e}^{ax}$, celles de $y'' + ay = 0$ sont $x \mapsto C\mathrm{e}^{-ax}$'
- Pour $y' = ay + b$ ($a \neq 0$), la solution constante est $-\dfrac{b}{a}$ (et non $\dfrac{b}{a}$)
- 'Déterminer la constante $C$ avant d''avoir écrit la solution générale : la condition initiale s''applique à $y(x) = C\mathrm{e}^{ax} - \dfrac{b}{a}$'
---
{% include cours-cards.html %}
