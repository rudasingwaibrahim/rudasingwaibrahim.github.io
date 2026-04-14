---
title: "Chapitre 3 — Calcul intégral"
permalink: /classes/bts-mec1/chapitre3/
hero_title: "Chapitre 3"
hero_subtitle: "Calcul intégral"

dossier_pdf: bts-mec1

cours:
  - titre: "Cours — Version élève"
    sub: "Espaces de réponse, tableaux à compléter"
    pdf: bts-calcul-integral-cours-eleve.pdf
    dossier: bts-mec1
  - titre: "Cours — Version professeur"
    sub: "Corrections complètes incluses"
    pdf: bts-calcul-integral-cours-prof.pdf
    dossier: bts-mec1

planches:
  - num: 1
    themes: "Primitives · IPP · Changement de variable"
    pdf: bts-calcul-integral-planche-01.pdf
  - num: 2
    themes: "Aires · Valeur moyenne · Applications BTP"
    pdf: bts-calcul-integral-planche-02.pdf

dm:
  - num: 1
    contenu: "Primitives · Déblai · Énergie solaire"
    duree: "1 semaine"
    pdf: bts-calcul-integral-dm-01-sujet.pdf
  - num: 2
    contenu: "Valeur moyenne · IPP double · Réservoir · Thermique"
    duree: "1 semaine"
    pdf: bts-calcul-integral-dm-02-sujet.pdf

ds_blancs:
  - num: 1
    contenu: "Vérifications · Intégrales · IPP · Flux thermique"
    duree: "55 min"
    pdf: bts-calcul-integral-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "Primitives · Intégrales · Toiture parabolique"
    duree: "55 min"
    pdf: bts-calcul-integral-dsblanc-02-sujet.pdf

ds_published: false

erreurs:
  - "Oublier la constante + C dans les primitives indéfinies"
  - "Confondre dérivée et primitive d'une fonction"
  - "Mal appliquer la linéarité de l'intégrale"
  - "Inverser les bornes sans changer le signe"
  - "Oublier la valeur absolue pour l'aire entre deux courbes"
  - "Confondre aire algébrique et aire géométrique"
  - "Erreurs dans les primitives usuelles : sin, cos, exp, puissances"

liens:
  - nom: "Wolfram Alpha"
    desc: "Calcule primitives et intégrales avec toutes les étapes détaillées"
    url: "https://www.wolframalpha.com/calculators/integral-calculator/"
    ico: "🔢"
    cat: calcul
  - nom: "GeoGebra — Visualiser l'intégrale"
    desc: "Modifier les bornes et voir l'aire colorée se mettre à jour en temps réel"
    url: "https://www.geogebra.org/m/ACVXrSjF"
    ico: "📐"
    cat: calcul
  - nom: "GeoGebra — Méthode des rectangles"
    desc: "Comprendre la définition de l'intégrale par approximation rectangulaire"
    url: "https://www.geogebra.org/m/hwdV4TyX"
    ico: "📊"
    cat: calcul
  - nom: "GeoGebra Calculatrice"
    desc: "Taper Integrale(f(x), a, b) pour calculer directement"
    url: "https://www.geogebra.org/calculator"
    ico: "⚙️"
    cat: calcul
  - nom: "Symbolab"
    desc: "Primitives et intégrales avec étapes détaillées en français"
    url: "https://www.symbolab.com/solver/integral-calculator"
    ico: "⚙️"
    cat: calcul
  - nom: "Bibm@th"
    desc: "Cours complet et exercices corrigés BTS Analyse — intégration"
    url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/integration.html"
    ico: "📚"
    cat: cours
  - nom: "Math'O karé"
    desc: "Cours illustré avec applets GeoGebra intégrés dans la page"
    url: "https://mathokare.re/2021/06/07/tc-calcul-integral/"
    ico: "📝"
    cat: cours
  - nom: "Mon lycée numérique"
    desc: "Cours avec outils Xcas et Python en ligne"
    url: "http://www.monlyceenumerique.fr/maths_en1/integrale/integrale.html"
    ico: "🎓"
    cat: cours
---

{% include cours-cards.html %}
