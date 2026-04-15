---
title: "Chapitre 7 — Statistiques à deux variables"
permalink: /classes/tale-techno-commun/chapitre7/
hero_title: "Chapitre 7"
hero_subtitle: "Statistiques à deux variables"
dossier_pdf: tale-techno
cours:
  - titre: "Cours — Version élève"
    pdf: tale-techno-commun-ch7-cours-eleve.pdf
    dossier: tale-techno
  - titre: "Cours — Version professeur"
    pdf: tale-techno-commun-ch7-cours-prof.pdf
    dossier: tale-techno
planches:
  - num: 1
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch7-planche-01.pdf
  - num: 2
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch7-planche-02.pdf
ds_blancs:
  - num: 1
    pdf: tale-techno-commun-ch7-dsblanc-01-sujet.pdf
  - num: 2
    pdf: tale-techno-commun-ch7-dsblanc-02-sujet.pdf
ds_published: false
erreurs:
  - "Confondre les coordonnées du point moyen G : x barre est la moyenne des x, y barre est la moyenne des y"
  - "Oublier de vérifier que la droite de régression passe par le point moyen G"
  - "Inverser interpolation et extrapolation : interpoler c'est estimer entre les données, extrapoler c'est estimer au-delà"
  - "Appliquer un ajustement affine à un nuage clairement non linéaire sans effectuer de changement de variable"
  - "Se tromper dans le changement de variable : poser z = log(y) puis oublier de revenir à y = 10^z"
  - "Confondre la méthode des moindres carrés et la méthode des points moyens : deux méthodes distinctes"
  - "Extrapoler trop loin du domaine observé et présenter le résultat comme fiable sans esprit critique"
liens:
  - nom: "Khan Academy — Régression linéaire"
    desc: "Cours vidéo complet sur la droite de régression et les moindres carrés"
    url: "https://fr.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/introduction-to-trend-lines/v/fitting-a-line-to-data"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Corrélation"
    desc: "Comprendre le coefficient de corrélation et son interprétation"
    url: "https://fr.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/scatterplots-and-correlation/v/correlation-and-causality"
    ico: "📚"
    cat: cours
  - nom: "GeoGebra — Régression interactive"
    desc: "Tracer un nuage de points et ajuster une droite de régression en temps réel"
    url: "https://www.geogebra.org/m/xc4whypc"
    ico: "📐"
    cat: calcul
  - nom: "Wolfram Alpha — Régression"
    desc: "Calculer la droite de régression et les coefficients à partir de données"
    url: "https://www.wolframalpha.com/input?i=linear+regression"
    ico: "🔢"
    cat: calcul
---
{% include cours-cards.html %}
