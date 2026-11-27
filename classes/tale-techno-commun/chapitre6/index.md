---
title: Chapitre 6 — Variables aléatoires et loi binomiale
permalink: /classes/tale-techno-commun/chapitre6/
hero_title: Chapitre 6
hero_subtitle: Variables aléatoires et loi binomiale
cours:
- titre: Cours — Version élève
  pdf: tale-techno/tale-techno-commun-ch6-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: tale-techno/tale-techno-commun-ch6-cours-prof.pdf
- titre: Cours complet
  fichier: /assets/pdf/tale-techno/tale-techno-commun-ch6-cours.pdf
planches:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch6-planche-01.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch6-planche-02.pdf
dm:
- num: 1
  contenu: Loi de probabilité · Espérance · Simulation
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch6-dm-01-sujet.pdf
ds_blancs:
- num: 1
  contenu: Automatismes · Loi et espérance · Tirages avec remise
  duree: "55 min"
  pdf: tale-techno/tale-techno-commun-ch6-dsblanc-01-sujet.pdf
- num: 2
  contenu: Loi de probabilité · Espérance · Comparer des jeux
  duree: "55 min"
  pdf: tale-techno/tale-techno-commun-ch6-dsblanc-02-sujet.pdf
ds_published: false
ds:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch6-ds-01-sujet.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch6-ds-02-sujet.pdf
- num: 3
  pdf: tale-techno/tale-techno-commun-ch6-ds-03-sujet.pdf
erreurs:
- "Confondre espérance et probabilité : $E(X) = np$ est une valeur moyenne, pas une probabilité"
- Oublier de vérifier que la somme des probabilités vaut 1 avant de calculer E(X)
- "Utiliser la loi binomiale pour des tirages sans remise : elle suppose des épreuves identiques et indépendantes"
- "Calculer $P(X \\geqslant k)$ terme à terme au lieu d'utiliser $1 - P(X \\leqslant k - 1)$"
- Confondre $P(X = k)$ et $P(X \leqslant k)$ à la calculatrice (binompdf / binomcdf, BinomialPD / BinomialCD)
- "Écrire $E(X) = np$ sans avoir justifié que $X$ suit la loi $\\mathcal{B}(n, p)$"
liens:
- nom: Khan Academy — Loi binomiale
  desc: Cours vidéo complet sur la loi binomiale avec exemples
  url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library/binomial-random-variables/v/binomial-distribution"
  ico: 📚
  cat: cours
- nom: Khan Academy — Espérance
  desc: "Comprendre l'espérance d'une variable aléatoire discrète"
  url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library/expected-value-lib/v/expected-value-of-a-discrete-random-variable"
  ico: 📚
  cat: cours
- nom: GeoGebra — Loi binomiale interactive
  desc: Visualiser la distribution binomiale en faisant varier n et p
  url: "https://www.geogebra.org/m/nvzawmvd"
  ico: 📐
  cat: calcul
- nom: Wolfram Alpha — Loi binomiale
  desc: "Calculer P(X = k), P(X <= k) et E(X) directement"
  url: "https://www.wolframalpha.com/input?i=binomial+distribution"
  ico: 🔢
  cat: calcul
---
{% include cours-cards.html %}
