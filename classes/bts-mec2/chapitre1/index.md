---
title: "Chapitre 1 — Probabilités conditionnelles & Loi binomiale"
permalink: /classes/bts-mec2/chapitre1/
hero_title: Chapitre 1
hero_subtitle: "Probabilités conditionnelles & Loi binomiale"
dossier_pdf: bts-mec2
cours:
- titre: Cours — Version élève
  sub: "Espaces de réponse, tableaux à compléter"
  pdf: bts-mec2-ch1-cours-eleve.pdf
  dossier: bts-mec2
- titre: Cours — Version professeur
  sub: Corrections complètes incluses
  pdf: bts-mec2-ch1-cours-prof.pdf
  dossier: bts-mec2
planches:
- num: 1
  themes: Arbres pondérés · Probabilités totales · Bayes
  pdf: bts-mec2-ch1-planche-01.pdf
- num: 2
  themes: "Loi binomiale · Espérance & variance · Calculs calculatrice"
  pdf: bts-mec2-ch1-planche-02.pdf
dm: []
ds_blancs:
- num: 1
  contenu: CCF Blanc Situation 2 — Probabilités + binomiale (page de garde + consignes E31)
  duree: "55 min"
  pdf: bts-mec2-ch1-dsblanc-01-sujet.pdf
- num: 2
  contenu: CCF Blanc Situation 2 — Variantes binomiale + arbre pondéré
  duree: "55 min"
  pdf: bts-mec2-ch1-dsblanc-02-sujet.pdf
ds_published: false
ds: []
erreurs:
- Confondre $P(A \cap B)$ et $P_B(A)$
- "Appliquer la loi binomiale sans vérifier ses conditions : $n$ épreuves identiques et indépendantes, deux issues, $X$ compte les succès"
- Confondre $P(X = k)$ et $P(X \leqslant k)$ à la calculatrice (binomFdp / binomFRép)
- "Mal utiliser la formule des probabilités totales : oublier un événement de la partition"
- "Se tromper dans la formule de Bayes : $P_B(A) = \\dfrac{P_A(B)\\,P(A)}{P(B)}$"
- Confondre événements indépendants et événements incompatibles
- "Oublier le coefficient binomial : $P(X = k) = \\binom{n}{k}\\,p^k(1-p)^{n-k}$"
- Écrire $V(X) = np$ au lieu de $V(X) = np(1 - p)$
liens:
- nom: GeoGebra — Loi binomiale interactive
  desc: Visualiser P(X=k) et P(X≤k) en faisant varier n et p
  url: "https://www.geogebra.org/m/W3UbgPup"
  ico: 📐
  cat: calcul
- nom: GeoGebra Calculatrice Probabilités
  desc: "Calculer binomiale, normale, Poisson directement en ligne"
  url: "https://www.geogebra.org/classic#probability"
  ico: ⚙️
  cat: calcul
- nom: "Khan Academy — Probabilités conditionnelles & Bayes"
  desc: "Cours complet : conditionnement, indépendance, théorème de Bayes"
  url: "https://fr.khanacademy.org/math/statistics-probability/probability-library"
  ico: 📚
  cat: cours
- nom: Khan Academy — Loi binomiale
  desc: "Vidéos + exercices sur la loi binomiale (E, V, calculs)"
  url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library"
  ico: 📚
  cat: cours
- nom: "Bibm@th — Probabilités BTS"
  desc: Cours synthétique BTS avec exercices corrigés
  url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/probas.html"
  ico: 📝
  cat: cours
---
{% include cours-cards.html %}
