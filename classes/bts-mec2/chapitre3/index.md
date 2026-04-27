---
title: "Chapitre 3 — Statistiques inférentielles"
permalink: /classes/bts-mec2/chapitre3/
hero_title: "Chapitre 3"
hero_subtitle: "Statistiques inférentielles"
dossier_pdf: bts-mec2
cours:
  - titre: "Cours — Version élève"
    sub: "Espaces de réponse, tableaux à compléter"
    pdf: bts-mec2-ch3-cours-eleve.pdf
    dossier: bts-mec2
  - titre: "Cours — Version professeur"
    sub: "Corrections complètes incluses"
    pdf: bts-mec2-ch3-cours-prof.pdf
    dossier: bts-mec2
planches:
  - num: 1
    themes: "Loi normale · Échantillonnage · IC moyenne & proportion"
    pdf: bts-mec2-ch3-planche-01.pdf
  - num: 2
    themes: "Tests bilatéraux & unilatéraux · Comparaison d'échantillons"
    pdf: bts-mec2-ch3-planche-02.pdf
dm: []
ds_blancs:
  - num: 1
    contenu: "Pots de confiture (Gr.B 2010) · Étiquetage (Gr.B 2006) · Équipes"
    duree: "3 h"
    pdf: bts-mec2-ch3-dsblanc-01-sujet.pdf
  - num: 2
    contenu: "Nouveau produit (Gr.B 2002) · Volume flacon (Gr.B 2010) · Procédés A/B"
    duree: "3 h"
    pdf: bts-mec2-ch3-dsblanc-02-sujet.pdf
ds_published: false
ds: []
erreurs:
  - "Confondre intervalle de confiance et intervalle de fluctuation"
  - "Oublier les conditions de validité : n ≥ 30, nf ≥ 5, n(1−f) ≥ 5"
  - "Interpréter l'IC comme « la vraie valeur est dans l'intervalle » au lieu de « on a 95 % de confiance »"
  - "Utiliser la formule de l'IC proportion pour une moyenne (ou inversement)"
  - "Oublier de diviser par √n dans la formule de l'IC pour la moyenne"
  - "Confondre test bilatéral et test unilatéral — mal poser H₁"
  - "Conclure qu'une valeur est « impossible » alors qu'elle est simplement hors de l'IC à 95 %"
  - "Rejeter H₀ avec une p-valeur > α, ou ne pas rejeter avec p-valeur < α (inversion)"
liens:
  - nom: "GeoGebra — Intervalle de confiance et estimation"
    desc: "Applet interactif : tirer N échantillons et observer les IC calculés"
    url: "https://www.geogebra.org/m/PrVaHfQ8"
    ico: "📐"
    cat: calcul
  - nom: "GeoGebra — Estimer une proportion (IC 95 %)"
    desc: "Visualiser la construction d'un IC pour une proportion à partir d'un sondage"
    url: "https://www.geogebra.org/m/Cj7vCJW9"
    ico: "📊"
    cat: calcul
  - nom: "GeoGebra Calculatrice Probabilités"
    desc: "Loi normale, calcul de Φ(z) et quantiles directement en ligne"
    url: "https://www.geogebra.org/classic#probability"
    ico: "⚙️"
    cat: calcul
  - nom: "Khan Academy — Intervalles de confiance"
    desc: "Chapitre complet (vidéos + exercices) sur la construction et l'interprétation d'un IC"
    url: "https://fr.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample"
    ico: "📚"
    cat: cours
  - nom: "Khan Academy — Tests de comparaison de deux échantillons"
    desc: "Comparer deux moyennes ou deux proportions (cadre BTS MEC2)"
    url: "https://fr.khanacademy.org/math/statistics-probability/significance-tests-confidence-intervals-two-samples"
    ico: "📚"
    cat: cours
  - nom: "Bibm@th — Statistique inférentielle"
    desc: "Cours BTS synthétique avec exercices corrigés (estimation, tests, IC)"
    url: "https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/statinferentielle.html"
    ico: "📝"
    cat: cours
---
{% include cours-cards.html %}
