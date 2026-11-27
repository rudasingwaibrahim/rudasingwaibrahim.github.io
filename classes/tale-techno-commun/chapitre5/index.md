---
title: Chapitre 5 — Probabilités conditionnelles
permalink: /classes/tale-techno-commun/chapitre5/
hero_title: Chapitre 5
hero_subtitle: Probabilités conditionnelles
cours:
- titre: Cours — Version élève
  pdf: tale-techno/tale-techno-commun-ch5-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: tale-techno/tale-techno-commun-ch5-cours-prof.pdf
- titre: Cours complet
  fichier: /assets/pdf/tale-techno/tale-techno-commun-ch5-cours.pdf
planches:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch5-planche-01.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch5-planche-02.pdf
dm:
- num: 1
  contenu: Arbre pondéré · Probabilités totales · Problème médical
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch5-dm-01-sujet.pdf
- num: 2
  contenu: Indépendance · Inverser le conditionnement · Problème appliqué
  duree: "1 semaine"
  pdf: tale-techno/tale-techno-commun-ch5-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: QCM · Tableau croisé et indépendance · Problème
  duree: "55 min"
  pdf: tale-techno/tale-techno-commun-ch5-dsblanc-01-sujet.pdf
- num: 2
  contenu: Vrai-faux · Arbres et probabilités totales
  duree: "55 min"
  pdf: tale-techno/tale-techno-commun-ch5-dsblanc-02-sujet.pdf
ds_published: false
ds:
- num: 1
  pdf: tale-techno/tale-techno-commun-ch5-ds-01-sujet.pdf
- num: 2
  pdf: tale-techno/tale-techno-commun-ch5-ds-02-sujet.pdf
- num: 3
  pdf: tale-techno/tale-techno-commun-ch5-ds-03-sujet.pdf
erreurs:
- "Confondre $P(A \\cap B)$ et $P_A(B)$ : la probabilité conditionnelle restreint l'univers à $A$"
- "Oublier que $P_A(B) = \\dfrac{P(A \\cap B)}{P(A)}$ exige $P(A) \\neq 0$"
- "Inverser le conditionnement : $P_A(B)$ n'est pas égal à $P_B(A)$ en général"
- "Croire que deux événements sans issue commune sont indépendants : si $A \\cap B = \\varnothing$, avec $P(A) \\neq 0$ et $P(B) \\neq 0$, alors $P(A \\cap B) = 0 \\neq P(A) \\times P(B)$"
- "Oublier la formule des probabilités totales : $P(B) = P(A)\\,P_A(B) + P(\\overline{A})\\,P_{\\overline{A}}(B)$"
- "Se tromper dans l'arbre pondéré : la somme des probabilités issues d'un même nœud vaut 1"
- "Confondre les règles de l'arbre : on multiplie le long d'un chemin, on additionne les chemins qui mènent au même événement"
liens:
- nom: Khan Academy — Probabilités conditionnelles
  desc: Cours vidéo complet sur les probabilités conditionnelles
  url: "https://fr.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence/v/calculating-conditional-probability"
  ico: 📚
  cat: cours
- nom: GeoGebra — Arbre pondéré interactif
  desc: Construire et visualiser des arbres de probabilités
  url: "https://www.geogebra.org/m/mxhpfgnh"
  ico: 📐
  cat: calcul
- nom: Wolfram Alpha — Probabilités
  desc: "Calculer des probabilités conditionnelles et vérifier l'indépendance"
  url: "https://www.wolframalpha.com/input?i=conditional+probability"
  ico: 🔢
  cat: calcul
---
{% include cours-cards.html %}
