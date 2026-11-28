---
title: Chapitre 7 — Statistiques à deux variables
permalink: /classes/terminale-techno-commun/chapitre7/
hero_title: Chapitre 7
hero_subtitle: Statistiques à deux variables
cours:
- titre: Cours — Version élève
  pdf: tale-techno/tale-techno-commun-ch7-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: tale-techno/tale-techno-commun-ch7-cours-prof.pdf
- titre: Cours complet — Statistiques à deux variables
  fichier: /assets/pdf/tale-techno-commun-ch7-cours.pdf
ds_published: false
ds:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch7-ds-01-sujet.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch7-ds-02-sujet.pdf
- num: 3
  pdf: tale-techno/tale-techno-commun-ch7-ds-03-sujet.pdf
erreurs:
- "Se tromper sur le point moyen : $G(\\bar x\\,;\\bar y)$, moyennes des $x_i$ et des $y_i$"
- Oublier de vérifier que la droite de régression passe par le point moyen G
- "Inverser interpolation et extrapolation : interpoler c'est estimer entre les données, extrapoler c'est estimer au-delà"
- Appliquer un ajustement affine à un nuage clairement non linéaire sans effectuer de changement de variable
- "Oublier de revenir à $y$ après le changement de variable $z = \\log y$ : $y = 10^z$"
- "Croire qu'un ajustement « au jugé » est la droite des moindres carrés : celle-ci rend minimale la somme $\\sum (y_i - (ax_i + b))^2$"
- Extrapoler trop loin du domaine observé et présenter le résultat comme fiable sans esprit critique
liens:
- nom: Khan Academy — Régression linéaire
  desc: Cours vidéo complet sur la droite de régression et les moindres carrés
  url: "https://fr.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/introduction-to-trend-lines/v/fitting-a-line-to-data"
  ico: 📚
  cat: cours
- nom: GeoGebra — Régression interactive
  desc: Tracer un nuage de points et ajuster une droite de régression en temps réel
  url: "https://www.geogebra.org/m/xc4whypc"
  ico: 📐
  cat: calcul
- nom: Wolfram Alpha — Régression
  desc: Calculer la droite de régression et les coefficients à partir de données
  url: "https://www.wolframalpha.com/input?i=linear+regression"
  ico: 🔢
  cat: calcul
canonical_url: /classes/tale-techno-commun/chapitre7/
sitemap: false
---
{% include cours-cards.html %}
