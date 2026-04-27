---
title: "Chapitre 1 — Probabilités conditionnelles & Loi binomiale"
permalink: /classes/bts-mec2/chapitre1/
hero_title: "Chapitre 1"
hero_subtitle: "Probabilités conditionnelles & Loi binomiale"
dossier_pdf: bts-mec2
cours:
  - titre: "Cours — Version élève"
    sub: "Espaces de réponse, tableaux à compléter"
    pdf: bts-mec2-ch1-cours-eleve.pdf
    dossier: bts-mec2
  - titre: "Cours — Version professeur"
    sub: "Corrections complètes incluses"
    pdf: bts-mec2-ch1-cours-prof.pdf
    dossier: bts-mec2
planches:
  - num: 1
    themes: "Arbres pondérés · Probabilités totales · Bayes"
    pdf: bts-mec2-ch1-planche-01.pdf
  - num: 2
    themes: "Loi binomiale · Espérance & variance · Calculs calculatrice"
    pdf: bts-mec2-ch1-planche-02.pdf
dm: []
ds_blancs:
  - num: 1
    contenu: "CCF Blanc Situation 2 — Probabilités + binomiale (page de garde + consignes E31)"
    duree: "55 min"
    pdf: bts-mec2-ch1-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "CCF Blanc Situation 2 — Variantes binomiale + arbre pondéré"
    duree: "55 min"
    pdf: bts-mec2-ch1-dsblanc-02-sujet.pdf
ds_published: false
ds: []
erreurs:
  - "Confondre P(A∩B) et P(A|B)"
  - "Oublier de vérifier les 4 conditions de la loi binomiale (n épreuves identiques, 2 issues, indépendance, X = nb succès)"
  - "Confondre P(X = k) et P(X ≤ k) à la calculatrice (binomFRep / binomPDF)"
  - "Mal utiliser la formule des probabilités totales (oublier un événement du système complet)"
  - "Inverser numérateur et dénominateur dans la formule de Bayes : P(A|B) = P(B|A)·P(A)/P(B)"
  - "Confondre événements indépendants et événements incompatibles"
  - "Oublier le coefficient binomial C(n,k) dans P(X = k)"
  - "Calculer V(X) = np au lieu de np(1−p)"
liens:
  - nom: "GeoGebra — Loi binomiale interactive"
    desc: "Visualiser P(X=k) et P(X≤k) en faisant varier n et p"
    url: "https://www.geogebra.org/m/W3UbgPup"
    ico: "📐"
    cat: calcul
  - nom: "GeoGebra Calculatrice Probabilités"
    desc: "Calculer binomiale, normale, Poisson directement en ligne"
    url: "https://www.geogebra.org/classic#probability"
    ico: "⚙️"
    cat: calcul
  - nom: "Khan Academy — Probabilités conditionnelles & Bayes"
    desc: "Cours complet : conditionnement, indépendance, théorème de Bayes"
    url: "https://fr.khanacademy.org/math/statistics-probability/probability-library"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Loi binomiale"
    desc: "Vidéos + exercices sur la loi binomiale (E, V, calculs)"
    url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library"
    ico: "📚"
    cat: cours
  - nom: "Bibm@th — Probabilités BTS"
    desc: "Cours synthétique BTS avec exercices corrigés"
    url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/probas.html"
    ico: "📝"
    cat: cours
---
{% include cours-cards.html %}
