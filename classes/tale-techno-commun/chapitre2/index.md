---
title: Chapitre 2 — Fonctions exponentielles
permalink: /classes/tale-techno-commun/chapitre2/
hero_title: Chapitre 2
hero_subtitle: Fonctions exponentielles
cours:
- titre: Cours — Version élève
  pdf: tale-techno/tale-techno-commun-ch2-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: tale-techno/tale-techno-commun-ch2-cours-prof.pdf
- titre: Cours complet
  fichier: /assets/pdf/tale-techno/tale-techno-commun-ch2-cours.pdf
planches:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch2-planche-01.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch2-planche-02.pdf
dm:
- num: 1
  contenu: Propriétés algébriques · Équations et inéquations · Taux moyen
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch2-dm-01-sujet.pdf
- num: 2
  contenu: Sens de variation de k × aˣ · Modélisation
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch2-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: Calculs de puissances · Modélisation · Taux d'évolution · Étude de k × aˣ
  duree: "2 h"
  pdf: tale-techno/tale-techno-commun-ch2-dsblanc-01-sujet.pdf
- num: 2
  contenu: Étude de fonctions · Modélisation type BAC
  duree: "2 h"
  pdf: tale-techno/tale-techno-commun-ch2-dsblanc-02-sujet.pdf
ds_published: true
ds:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch2-ds-01-sujet.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch2-ds-02-sujet.pdf
- num: 3
  pdf: tale-techno/tale-techno-commun-ch2-ds-03-sujet.pdf
erreurs:
- "Confondre $a^{x+y} = a^x \\times a^y$ et $a^{xy}$ : pour un produit de puissances de même base, on additionne les exposants"
- "Écrire $a^0 = 0$ : pour tout $a > 0$, $a^0 = 1$"
- "Oublier que $a^x > 0$ pour tout réel $x$ (avec $a > 0$) : l'équation $2^x = 0$ n'a pas de solution"
- "Conclure que $x \\mapsto k\\,a^x$ est croissante dès que $a > 1$ : si $k < 0$, le sens de variation est inversé"
- Confondre croissance exponentielle (taux constant) et croissance linéaire (accroissement constant)
- "Calculer un taux moyen en divisant le taux global par $n$ : on résout $(1 + t_m)^n = C$, d'où $t_m = C^{1/n} - 1$"
liens:
- nom: Khan Academy — Fonction exponentielle
  desc: Cours vidéo sur la fonction exponentielle et ses propriétés
  url: "https://fr.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:exp/x2ec2f6f830c9fb89:exp-graph/v/graphing-exponential-functions"
  ico: 📚
  cat: cours
- nom: Mathsmentales — Exponentielle
  desc: Exercices de calcul mental sur la fonction exponentielle
  url: "https://mathsmentales.net/"
  ico: 🧠
  cat: exercice
- nom: GeoGebra — Exponentielle interactive
  desc: Visualiser la courbe exponentielle et ses transformations
  url: "https://www.geogebra.org/m/sjcbepnd"
  ico: 📐
  cat: calcul
- nom: Wolfram Alpha — Exponentielle
  desc: "Calculer, dériver et intégrer des fonctions exponentielles"
  url: "https://www.wolframalpha.com/input?i=plot+exp(x)"
  ico: 🔢
  cat: calcul
---
{% include cours-cards.html %}
