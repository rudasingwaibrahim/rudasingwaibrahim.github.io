---
title: "Chapitre 1 — Suites numériques"
permalink: /classes/tale-techno-commun/chapitre1/
hero_title: "Chapitre 1"
hero_subtitle: "Suites numériques"
cours:
  - titre: "Cours — Version élève"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-cours-eleve.pdf
  - titre: "Cours — Version professeur"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-cours-prof.pdf
planches:
  - num: 1
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-planche-01.pdf
  - num: 2
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-planche-02.pdf
dm:
  - num: 1
    contenu: "Suite arithmétique · Somme de termes · Modélisation"
    duree: "1 semaine"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-dm-01-sujet.pdf
  - num: 2
    contenu: "Suite géométrique · Convergence · Problème ouvert"
    duree: "1 semaine"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-dm-02-sujet.pdf
ds_blancs:
  - num: 1
    contenu: "Suites arithmétiques · Suites géométriques · Sens de variation"
    duree: "2 h"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "Sommes · Convergence · Modélisation type BAC"
    duree: "2 h"
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-dsblanc-02-sujet.pdf
ds_published: true
ds:
  - num: 1
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-ds-01-sujet.pdf
  - num: 2
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-ds-02-sujet.pdf
  - num: 3
    pdf: /assets/pdf/tale-techno/tale-techno-commun-ch1-ds-03-sujet.pdf
erreurs:
  - "Confondre suite arithmétique et suite géométrique : additionner au lieu de multiplier (ou inversement)"
  - "Oublier que la raison d'une suite géométrique doit être non nulle et que les termes doivent rester de même signe"
  - "Calculer u(n+1) - u(n) pour une suite géométrique au lieu de u(n+1) / u(n)"
  - "Se tromper dans la formule du terme général : u(n) = u(0) + n*r et non u(n) = u(1) + n*r"
  - "Confondre le rang n et le terme u(n) : le rang est l'indice, le terme est la valeur"
  - "Oublier de vérifier le sens de variation avant de conclure sur la convergence"
  - "Appliquer la somme des termes d'une suite arithmétique sans adapter les bornes : S = (nombre de termes) * (premier + dernier) / 2"
liens:
  - nom: "Khan Academy — Suites arithmétiques"
    desc: "Cours vidéo complet sur les suites arithmétiques avec exemples"
    url: "https://fr.khanacademy.org/math/algebra/x2f8bb11595b61c86:sequences/x2f8bb11595b61c86:introduction-to-arithmetic-sequences/v/arithmetic-sequences"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Suites géométriques"
    desc: "Comprendre les suites géométriques et leur convergence"
    url: "https://fr.khanacademy.org/math/algebra/x2f8bb11595b61c86:sequences/x2f8bb11595b61c86:introduction-to-geometric-sequences/v/geometric-sequences-introduction"
    ico: "📚"
    cat: cours
  - nom: "GeoGebra — Suites interactives"
    desc: "Visualiser les termes d'une suite et son comportement asymptotique"
    url: "https://www.geogebra.org/m/ksphynmp"
    ico: "📐"
    cat: calcul
  - nom: "Wolfram Alpha — Suites"
    desc: "Calculer les termes, la somme et la limite d'une suite"
    url: "https://www.wolframalpha.com/input?i=sequence"
    ico: "🔢"
    cat: calcul
---
{% include cours-cards.html %}
