---
title: Chapitre 9 — Suites 2/2
permalink: /classes/terminale-spe-maths/chapitre9/
hero_title: Chapitre 9
hero_subtitle: Comparaison, gendarmes, convergence monotone et suites géométriques
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch9-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch9-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch9-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch9-planche-02.pdf
dm_published: true
dm:
- num: 1
  contenu: Suites bornées · Convergence monotone
  duree: 1 semaine
  pdf: terminale-spe-ch9-dm-01-sujet.pdf
- num: 2
  contenu: Suites géométriques · Arithmético-géométriques
  duree: 1 semaine
  pdf: terminale-spe-ch9-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Récurrence · Suite auxiliaire géométrique · Sommes
  duree: 2 h
  pdf: terminale-spe-ch9-dsblanc-01-sujet.pdf
- num: 2
  contenu: Convergence monotone · Algorithme de seuil
  duree: 2 h
  pdf: terminale-spe-ch9-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch9-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch9-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch9-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch9-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch9-ds-03-sujet.pdf
python:
- titre: "Seuils et valeurs approchées de √2, du nombre d'or et de e"
  fichier: /assets/python/terminale-spe-maths/ch9-seuils-valeurs-approchees.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch9.py
  duree: "40 min"
  contenu: "Seuil (suite uₙ₊₁ = 0,85uₙ + 45) · √2 par dichotomie · Nombre d'or · e = 1 + 1/1! + 1/2! + …"
erreurs:
- 'Croire qu''une suite croissante converge toujours : il faut aussi qu''elle soit majorée'
- 'Penser que le théorème de convergence monotone donne la limite : il donne seulement l''existence de la limite'
- Appliquer le théorème des gendarmes avec des suites encadrantes de limites différentes
- Oublier que $(q^n)$ n'a pas de limite lorsque $q\leqslant -1$
- Écrire $1+q+\cdots+q^n=\dfrac{1-q^n}{1-q}$ au lieu de $\dfrac{1-q^{n+1}}{1-q}$
- 'Confondre majorant et limite : une suite majorée par $5$ ne tend pas forcément vers $5$'
---
{% include cours-cards.html %}
