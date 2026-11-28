---
title: Chapitre 13 — Statistiques descriptives
permalink: /classes/seconde220/chapitre13/
hero_title: Chapitre 13
hero_subtitle: Statistiques descriptives
cours:
- titre: Cours — Version élève
  pdf: seconde-ch13-cours.pdf
- titre: Cours — Version professeur
  pdf: seconde-ch13-cours-prof.pdf
planches:
- num: 1
  pdf: seconde-ch13-planche-01.pdf
- num: 2
  pdf: seconde-ch13-planche-02.pdf
dm:
- num: 1
  contenu: Moyennes pondérées
  duree: "1 semaine"
  pdf: seconde-ch13-dm-01-sujet.pdf
- num: 2
  contenu: "Quartiles · Boîtes à moustaches · Valeur extrême"
  duree: "1 semaine"
  pdf: seconde-ch13-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: Moyennes · Linéarité
  duree: "55 min"
  pdf: seconde-ch13-dsblanc-01-sujet.pdf
- num: 2
  contenu: Médiane · Quartiles · Écart type
  duree: "55 min"
  pdf: seconde-ch13-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: seconde-ch13-activites.pdf
- titre: Activités — Version professeur
  pdf: seconde-ch13-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: seconde-ch13-ds-01-sujet.pdf
- num: 2
  pdf: seconde-ch13-ds-02-sujet.pdf
- num: 3
  pdf: seconde-ch13-ds-03-sujet.pdf
python:
- titre: "Moyenne et écart type d'une série"
  fichier: /assets/python/seconde/ch13-moyenne-ecart-type.ipynb
  module: /assets/python/seconde/verif_2nde_ch13.py
  duree: "35 min"
  contenu: "Accumulateur de somme · Moyenne · Écart type · Compteur · Proportion dans [m − s ; m + s]"
erreurs:
- "Confondre moyenne et médiane : la médiane partage la série ordonnée en deux groupes de même effectif"
- Oublier de pondérer chaque valeur par son effectif dans le calcul de la moyenne
- "Mal déterminer la médiane quand l'effectif total est pair : c'est la moyenne des deux valeurs centrales"
- "Confondre les quartiles $Q_1$, $Q_3$ et la médiane"
- "Oublier que l'écart interquartile vaut $Q_3 - Q_1$"
- "Mal lire un histogramme : l'aire représente l'effectif, pas la hauteur seule"
liens:
- nom: Lumni — Moyenne et médiane
  desc: Calculer et interpréter les indicateurs statistiques
  url: "https://www.lumni.fr/video/la-moyenne-et-la-mediane"
  ico: 🎬
  cat: cours
- nom: Khan Academy — Statistiques descriptives
  desc: "Exercices sur moyenne, médiane, quartiles, écart-type"
  url: "https://fr.khanacademy.org/math/statistics-probability"
  ico: 📚
  cat: cours
- nom: GeoGebra — Diagrammes statistiques
  desc: Créer histogrammes et boîtes à moustaches
  url: "https://www.geogebra.org/classic"
  ico: 📐
  cat: calcul
---
{% include cours-cards.html %}
