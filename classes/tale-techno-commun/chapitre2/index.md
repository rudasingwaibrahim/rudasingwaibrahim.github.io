---
title: "Chapitre 2 — Fonction exponentielle"
permalink: /classes/tale-techno-commun/chapitre2/
hero_title: "Chapitre 2"
hero_subtitle: "Fonction exponentielle"
dossier_pdf: tale-techno
cours:
  - titre: "Cours — Version élève"
    pdf: tale-techno-commun-ch2-cours-eleve.pdf
    dossier: tale-techno
  - titre: "Cours — Version professeur"
    pdf: tale-techno-commun-ch2-cours-prof.pdf
    dossier: tale-techno
planches:
  - num: 1
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch2-planche-01.pdf
  - num: 2
    themes: "Sujet et corrigé inclus"
    pdf: tale-techno-commun-ch2-planche-02.pdf
ds_blancs:
  - num: 1
    pdf: tale-techno-commun-ch2-dsblanc-01-sujet.pdf
  - num: 2
    pdf: tale-techno-commun-ch2-dsblanc-02-sujet.pdf
ds_published: false
erreurs:
  - "Confondre exp(a+b) = exp(a) * exp(b) avec exp(a*b) : la propriété fondamentale concerne la somme, pas le produit"
  - "Écrire exp(0) = 0 au lieu de exp(0) = 1 : l'exponentielle ne s'annule jamais"
  - "Oublier que exp(x) est toujours strictement positive : ne jamais écrire exp(x) = 0 ou exp(x) inférieur à 0"
  - "Se tromper dans la dérivée : la dérivée de exp(u) est u' * exp(u), pas simplement exp(u)"
  - "Confondre croissance exponentielle et croissance linéaire dans les problèmes de modélisation"
  - "Résoudre exp(x) = a en écrivant x = ln(a) sans vérifier que a est strictement positif"
  - "Oublier la croissance comparée : exp(x) l'emporte sur toute puissance de x quand x tend vers l'infini"
liens:
  - nom: "Khan Academy — Fonction exponentielle"
    desc: "Cours vidéo sur la fonction exponentielle et ses propriétés"
    url: "https://fr.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:exp/x2ec2f6f830c9fb89:exp-graph/v/graphing-exponential-functions"
    ico: "📚"
    cat: cours
  - nom: "Mathsmentales — Exponentielle"
    desc: "Exercices de calcul mental sur la fonction exponentielle"
    url: "https://mathsmentales.net/"
    ico: "🧠"
    cat: exercice
  - nom: "GeoGebra — Exponentielle interactive"
    desc: "Visualiser la courbe exponentielle et ses transformations"
    url: "https://www.geogebra.org/m/sjcbepnd"
    ico: "📐"
    cat: calcul
  - nom: "Wolfram Alpha — Exponentielle"
    desc: "Calculer, dériver et intégrer des fonctions exponentielles"
    url: "https://www.wolframalpha.com/input?i=plot+exp(x)"
    ico: "🔢"
    cat: calcul
---
{% include cours-cards.html %}
