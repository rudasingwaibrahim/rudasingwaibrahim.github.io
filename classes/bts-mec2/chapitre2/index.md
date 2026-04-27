---
title: "Chapitre 2 — Loi normale & Théorème central limite"
permalink: /classes/bts-mec2/chapitre2/
hero_title: "Chapitre 2"
hero_subtitle: "Loi normale & TLC"
dossier_pdf: bts-mec2
cours:
  - titre: "Cours — Version élève"
    sub: "Espaces de réponse, tableaux à compléter"
    pdf: bts-mec2-ch2-cours-eleve.pdf
    dossier: bts-mec2
  - titre: "Cours — Version professeur"
    sub: "Corrections complètes incluses"
    pdf: bts-mec2-ch2-cours-prof.pdf
    dossier: bts-mec2
planches:
  - num: 1
    themes: "Loi normale · Standardisation · Calculs calculatrice"
    pdf: bts-mec2-ch2-planche-01.pdf
  - num: 2
    themes: "TLC · Somme & moyenne empirique · Approximation"
    pdf: bts-mec2-ch2-planche-02.pdf
dm: []
ds_blancs:
  - num: 1
    contenu: "CCF Blanc Situation 2 — Loi normale + TLC + tolérance"
    duree: "55 min"
    pdf: bts-mec2-ch2-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "CCF Blanc Situation 2 — Loi normale + variance & somme de VA"
    duree: "55 min"
    pdf: bts-mec2-ch2-dsblanc-02-sujet.pdf
ds_published: false
ds: []
erreurs:
  - "Oublier de standardiser : Z = (X−μ)/σ avant de lire la table normale"
  - "Confondre σ et σ² (variance) dans les énoncés"
  - "Pour la moyenne empirique X̄, oublier que σ_X̄ = σ/√n (et non σ)"
  - "Pour une somme S_n, oublier que σ_S = σ·√n (et non σ/√n)"
  - "Appliquer le TLC sans vérifier n ≥ 30"
  - "Mauvaise lecture des intervalles : 68 % à ±1σ, 95 % à ±2σ, 99,7 % à ±3σ"
  - "Confondre P(X ≤ a) et P(X ≥ a) — penser à la symétrie de la loi normale"
liens:
  - nom: "GeoGebra — Loi normale interactive"
    desc: "Visualiser la courbe en cloche et les aires sous la courbe"
    url: "https://www.geogebra.org/m/qmZDh2Bx"
    ico: "📐"
    cat: calcul
  - nom: "GeoGebra Calculatrice Probabilités"
    desc: "Loi normale, Φ(z), quantiles directement en ligne"
    url: "https://www.geogebra.org/classic#probability"
    ico: "⚙️"
    cat: calcul
  - nom: "GeoGebra — Théorème central limite (TLC)"
    desc: "Simulation : la moyenne empirique tend vers une loi normale"
    url: "https://www.geogebra.org/m/JNvXFnzM"
    ico: "📊"
    cat: calcul
  - nom: "Khan Academy — Loi normale"
    desc: "Cours sur la loi normale et ses propriétés"
    url: "https://fr.khanacademy.org/math/statistics-probability/modeling-distributions-of-data"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Théorème central limite"
    desc: "Comprendre le TLC : simulations + démonstrations"
    url: "https://fr.khanacademy.org/math/statistics-probability/sampling-distributions-library"
    ico: "📚"
    cat: cours
  - nom: "Bibm@th — Loi normale BTS"
    desc: "Cours BTS synthétique avec exercices corrigés"
    url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/loinormale.html"
    ico: "📝"
    cat: cours
---
{% include cours-cards.html %}
