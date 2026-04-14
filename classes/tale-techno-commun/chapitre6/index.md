---
title: "Chapitre 6 — Loi binomiale et espérance"
permalink: /classes/tale-techno-commun/chapitre6/
hero_title: "Chapitre 6"
hero_subtitle: "Loi binomiale et espérance"

dossier_pdf: tale-techno

cours:
  - titre: "Cours — Version élève"
    pdf: tale-techno-commun-ch6-cours-eleve.pdf
    dossier: tale-techno
  - titre: "Cours — Version professeur"
    pdf: tale-techno-commun-ch6-cours-prof.pdf
    dossier: tale-techno

planches:
  - num: 1
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch6-planche-01.pdf
  - num: 2
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch6-planche-02.pdf

ds_blancs:
  - num: 1
    pdf: tale-techno-commun-ch6-dsblanc-01-sujet.pdf
  - num: 2
    pdf: tale-techno-commun-ch6-dsblanc-02-sujet.pdf

ds_published: false

erreurs:
  - "Confondre espérance et probabilité : E(X) = np est une moyenne, pas une probabilité"
  - "Oublier de vérifier que la somme des probabilités vaut 1 avant de calculer E(X)"
  - "Appliquer la loi binomiale sans tirage avec remise : B(n,p) exige des épreuves indépendantes"
  - "Calculer P(X supérieur ou égal à k) directement au lieu d'utiliser le complément : 1 - P(X inférieur ou égal à k-1)"
  - "Confondre P(X = k) exact et P(X inférieur ou égal à k) cumulé : binompdf vs binomcdf"
  - "Oublier la symétrie des coefficients binomiaux : C(n,k) = C(n,n-k)"
  - "Écrire E(X) = np sans avoir identifié la loi B(n,p) au préalable"

liens:
  - nom: "Khan Academy — Loi binomiale"
    desc: "Cours vidéo complet sur la loi binomiale avec exemples"
    url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library/binomial-random-variables/v/binomial-distribution"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Espérance"
    desc: "Comprendre l'espérance d'une variable aléatoire discrète"
    url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library/expected-value-lib/v/expected-value-of-a-discrete-random-variable"
    ico: "📚"
    cat: cours
  - nom: "GeoGebra — Loi binomiale interactive"
    desc: "Visualiser la distribution binomiale en faisant varier n et p"
    url: "https://www.geogebra.org/m/nvzawmvd"
    ico: "📐"
    cat: calcul
  - nom: "Wolfram Alpha — Loi binomiale"
    desc: "Calculer P(X = k), P(X inférieur ou égal à k) et E(X) directement"
    url: "https://www.wolframalpha.com/input?i=binomial+distribution"
    ico: "🔢"
    cat: calcul
---

{% include cours-cards.html %}
