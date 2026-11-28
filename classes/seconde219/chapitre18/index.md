---
title: Chapitre 18 — Échantillonnage
permalink: /classes/seconde219/chapitre18/
hero_title: Chapitre 18
hero_subtitle: Échantillonnage
cours:
- titre: Cours — Version élève
  pdf: seconde-ch18-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: seconde-ch18-cours-prof.pdf
- titre: Cours complet
  pdf: seconde-ch18-cours.pdf
planches:
- num: 1
  pdf: seconde-ch18-planche-01.pdf
- num: 2
  pdf: seconde-ch18-planche-02.pdf
dm:
- num: 1
  duree: "1 semaine"
  pdf: seconde-ch18-dm-01-sujet.pdf
- num: 2
  duree: "1 semaine"
  pdf: seconde-ch18-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: Échantillonnage · Fluctuation · Estimation
  duree: "55 min"
  pdf: seconde-ch18-dsblanc-01-sujet.pdf
- num: 2
  contenu: Intervalle de confiance · Décision
  duree: "55 min"
  pdf: seconde-ch18-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: seconde-ch18-activites.pdf
- titre: Activités — Version professeur
  pdf: seconde-ch18-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: seconde-ch18-ds-01-sujet.pdf
- num: 2
  pdf: seconde-ch18-ds-02-sujet.pdf
- num: 3
  pdf: seconde-ch18-ds-03-sujet.pdf
python:
- titre: "Simuler des échantillons, observer la loi des grands nombres"
  fichier: /assets/python/seconde/ch18-simulation-echantillons.ipynb
  module: /assets/python/seconde/verif_2nde_ch18.py
  duree: "40 min"
  contenu: "Simuler un dé · Expérience de Bernoulli · Fréquence dans un échantillon · Écart type des fréquences · Loi des grands nombres"
erreurs:
- "Confondre population, échantillon et individu"
- "Oublier que la fréquence observée sur un échantillon varie d'un échantillon à l'autre (fluctuation d'échantillonnage)"
- "Croire qu'une simulation démontre une probabilité : elle donne une fréquence, qui fluctue"
- "Oublier que, lorsque $n$ est grand, la fréquence observée est le plus souvent proche de la probabilité (loi des grands nombres)"
- "Croire qu'un échantillon plus grand donne toujours exactement la probabilité $p$ : la fréquence en est seulement, le plus souvent, plus proche"
- "Croire qu'après plusieurs PILE, FACE devient plus probable : les lancers sont indépendants"
liens:
- nom: Mathrix — Échantillonnage Seconde
  desc: "Cours vidéo sur l'échantillonnage et la fluctuation"
  url: "https://www.mathrix.fr/echantillonnage-seconde/"
  ico: 🎬
  cat: cours
- nom: Khan Academy — Statistiques inférentielles
  desc: "Exercices sur l'échantillonnage"
  url: "https://fr.khanacademy.org/math/statistics-probability/sampling-distributions-library"
  ico: 📚
  cat: cours
---
{% include cours-cards.html %}