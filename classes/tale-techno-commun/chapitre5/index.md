---
title: "Chapitre 5 — Probabilités conditionnelles"
permalink: /classes/tale-techno-commun/chapitre5/
hero_title: "Chapitre 5"
hero_subtitle: "Probabilités conditionnelles"
cours:
  - titre: "Cours — Version élève"
    pdf: tale-techno-commun-ch5-cours-eleve.pdf
  - titre: "Cours — Version professeur"
    pdf: tale-techno-commun-ch5-cours-prof.pdf
planches:
  - num: 1
    pdf: tale-techno-commun-ch5-planche-01.pdf
  - num: 2
    pdf: tale-techno-commun-ch5-planche-02.pdf
dm:
  - num: 1
    contenu: "Arbre pondéré · Probabilités totales · Problème médical"
    duree: "1 semaine"
    pdf: tale-techno-commun-ch5-dm-01-sujet.pdf
  - num: 2
    contenu: "Indépendance · Bayes · Problème appliqué"
    duree: "1 semaine"
    pdf: tale-techno-commun-ch5-dm-02-sujet.pdf
ds_blancs:
  - num: 1
    contenu: "Probabilité conditionnelle · Arbre pondéré · Indépendance"
    duree: "2 h"
    pdf: tale-techno-commun-ch5-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "Probabilités totales · Test médical · Synthèse type BAC"
    duree: "2 h"
    pdf: tale-techno-commun-ch5-dsblanc-02-sujet.pdf
ds_published: true
ds:
  - num: 1
    pdf: tale-techno-commun-ch5-ds-01-sujet.pdf
  - num: 2
    pdf: tale-techno-commun-ch5-ds-02-sujet.pdf
  - num: 3
    pdf: tale-techno-commun-ch5-ds-03-sujet.pdf
erreurs:
  - "Confondre P(A inter B) et P_A(B) : l'intersection est une probabilité absolue, la conditionnelle restreint l'univers"
  - "Oublier de vérifier que P(A) est non nul avant de calculer P_A(B) = P(A inter B) / P(A)"
  - "Inverser le conditionnement : P_A(B) n'est pas égal à P_B(A) en général"
  - "Confondre indépendance et incompatibilité : deux événements incompatibles ne sont presque jamais indépendants"
  - "Oublier la formule des probabilités totales : P(B) = P(A)*P_A(B) + P(Abar)*P_Abar(B)"
  - "Se tromper dans l'arbre pondéré : la somme des branches issues d'un même noeud doit toujours valoir 1"
  - "Multiplier les probabilités sur un chemin alors qu'il faut les additionner entre chemins menant au même événement"
liens:
  - nom: "Khan Academy — Probabilités conditionnelles"
    desc: "Cours vidéo complet sur les probabilités conditionnelles"
    url: "https://fr.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence/v/calculating-conditional-probability"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Théorème de Bayes"
    desc: "Comprendre le théorème de Bayes et ses applications"
    url: "https://fr.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence/v/bayes-theorem-visualized"
    ico: "📚"
    cat: cours
  - nom: "GeoGebra — Arbre pondéré interactif"
    desc: "Construire et visualiser des arbres de probabilités"
    url: "https://www.geogebra.org/m/mxhpfgnh"
    ico: "📐"
    cat: calcul
  - nom: "Wolfram Alpha — Probabilités"
    desc: "Calculer des probabilités conditionnelles et vérifier l'indépendance"
    url: "https://www.wolframalpha.com/input?i=conditional+probability"
    ico: "🔢"
    cat: calcul
---
{% include cours-cards.html %}
