---
title: "Chapitre 15 — Variables aléatoires"
permalink: /classes/premiere-spe-maths/chapitre15/
dossier_pdf: premiere-spe-maths
hero_title: "Chapitre 15"
hero_subtitle: "Variables aléatoires — Loi, espérance et variance"
cours:
  - titre: "Cours — Version élève"
    pdf: premiere-spe-ch15-cours-eleve.pdf
  - titre: "Cours — Version professeur"
    pdf: premiere-spe-ch15-cours-prof.pdf
planches:
  - num: 1
    pdf: premiere-spe-ch15-planche-01.pdf
  - num: 2
    pdf: premiere-spe-ch15-planche-02.pdf
dm_published: false
dm:
  - num: 1
    contenu: "Variable aléatoire · Loi de probabilité"
    duree: "1 semaine"
    pdf: premiere-spe-ch15-dm-01-sujet.pdf
  - num: 2
    contenu: "Espérance · Variance · Écart-type"
    duree: "1 semaine"
    pdf: premiere-spe-ch15-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
  - num: 1
    contenu: "Loi de probabilité · Espérance"
    duree: "55 min"
    pdf: premiere-spe-ch15-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "Variance · Écart-type · Linéarité"
    duree: "55 min"
    pdf: premiere-spe-ch15-dsblanc-02-sujet.pdf
ds_published: false
ds:
  - num: 1
    pdf: premiere-spe-ch15-ds-01-sujet.pdf
  - num: 2
    pdf: premiere-spe-ch15-ds-02-sujet.pdf
  - num: 3
    pdf: premiere-spe-ch15-ds-03-sujet.pdf
erreurs:
  - "Confondre variable aléatoire X (fonction) et ses valeurs xᵢ"
  - "Oublier que la somme des probabilités d'une loi vaut 1"
  - "Mauvaise formule de l'espérance : E(X) = Σ xᵢ · P(X = xᵢ), pas la moyenne arithmétique des xᵢ"
  - "Confondre V(X) (variance) et σ(X) (écart-type) : σ(X) = √V(X)"
  - "Oublier la formule de König : V(X) = E(X²) − E(X)²"
  - "Croire que E(aX + b) = aE(X) + b·E(X) : NON, c'est aE(X) + b (linéarité)"
liens:
  - nom: "Jaicompris — Variables aléatoires"
    desc: "Méthode complète : loi, espérance, variance"
    url: "https://www.jaicompris.com/lycee/math/probabilite/variable-aleatoire.php"
    ico: "🎯"
    cat: methode
  - nom: "Khan Academy — Variables aléatoires discrètes"
    desc: "Loi, espérance, variance"
    url: "https://fr.khanacademy.org/math/statistics-probability/random-variables-stats-library"
    ico: "🎬"
    cat: cours
  - nom: "GeoGebra — Loi de probabilité"
    desc: "Construire un diagramme en bâtons d'une VA"
    url: "https://www.geogebra.org/m/RjNmKkPP"
    ico: "📐"
    cat: calcul
  - nom: "Lumni — Variables aléatoires"
    desc: "Vidéo : définition, espérance et variance"
    url: "https://www.lumni.fr/programme/variables-aleatoires"
    ico: "🎬"
    cat: cours
  - nom: "Maths-Cours — Variables aléatoires"
    desc: "Exercices progressifs avec corrigés détaillés"
    url: "https://www.maths-cours.fr/exercices/variable-aleatoire"
    ico: "📝"
    cat: entrainement
---
{% include cours-cards.html %}
