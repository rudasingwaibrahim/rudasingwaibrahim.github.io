---
title: Chapitre 16 — Probabilités
permalink: /classes/seconde219/chapitre16/
hero_title: Chapitre 16
hero_subtitle: Probabilités
cours:
- titre: Cours — Version élève
  pdf: seconde-ch16-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: seconde-ch16-cours-prof.pdf
- titre: Cours complet
  pdf: seconde-ch16-cours.pdf
planches:
- num: 1
  pdf: seconde-ch16-planche-01.pdf
- num: 2
  pdf: seconde-ch16-planche-02.pdf
dm:
- num: 1
  contenu: Probabilités simples · Événement contraire
  duree: "1 semaine"
  pdf: seconde-ch16-dm-01-sujet.pdf
- num: 2
  contenu: Arbre · Tableau · Union et intersection
  duree: "1 semaine"
  pdf: seconde-ch16-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: Probabilités · Événements · Formules
  duree: "55 min"
  pdf: seconde-ch16-dsblanc-01-sujet.pdf
- num: 2
  contenu: "Loi de probabilité · Réunion et intersection · Arbre"
  duree: "55 min"
  pdf: seconde-ch16-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: seconde-ch16-activites.pdf
- titre: Activités — Version professeur
  pdf: seconde-ch16-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: seconde-ch16-ds-01-sujet.pdf
- num: 2
  pdf: seconde-ch16-ds-02-sujet.pdf
- num: 3
  pdf: seconde-ch16-ds-03-sujet.pdf
python:
- titre: "Filtrer des données et dresser un tableau croisé"
  fichier: /assets/python/seconde/ch16-filtres-tableau-croise.ipynb
  module: /assets/python/seconde/verif_2nde_ch16.py
  duree: "35 min"
  contenu: "Filtre avec and, or, not · Tableau croisé d'effectifs · Fréquence conditionnelle et probabilité conditionnelle"
erreurs:
- "Confondre issue, événement et univers"
- "Oublier qu'en équiprobabilité toutes les issues ont la même probabilité"
- "Mal compter les issues favorables ou le nombre total d'issues"
- "Oublier l'événement contraire : $P(\\overline{A}) = 1 - P(A)$"
- Confondre intersection $A \cap B$ (« A et B ») et réunion $A \cup B$ (« A ou B »)
- "Confondre $P_A(B)$ et $P_B(A)$ : la proportion de $B$ parmi les $A$ n'est pas la proportion de $A$ parmi les $B$"
- Ne pas vérifier que la somme des probabilités vaut 1
- Oublier une branche dans un arbre des possibles
liens:
- nom: Mathrix — Probabilités Seconde
  desc: Cours vidéo complet sur les probabilités
  url: "https://www.mathrix.fr/probabilites-seconde/"
  ico: 🎬
  cat: cours
- nom: Khan Academy — Probabilités
  desc: Exercices interactifs progressifs sur les probabilités
  url: "https://fr.khanacademy.org/math/statistics-probability/probability-library"
  ico: 📚
  cat: cours
- nom: JeuxMaths — Probabilités
  desc: Exercices interactifs en ligne
  url: "https://www.jeuxmaths.fr/exercices-de-maths-probabilites.html"
  ico: 🎮
  cat: cours
---
{% include cours-cards.html %}