---
title: Chapitre 19 — Concentration, loi des grands nombres
permalink: /classes/terminale-spe-maths/chapitre19/
hero_title: Chapitre 19
hero_subtitle: Inégalité de Bienaymé-Tchebychev — Inégalité de concentration — Loi des grands nombres
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch19-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch19-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch19-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch19-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Inégalité de Bienaymé-Tchebychev en situation
  duree: 1 semaine
  pdf: terminale-spe-ch19-dm-01-sujet.pdf
- num: 2
  contenu: Inégalité de concentration · Taille d'échantillon
  duree: 1 semaine
  pdf: terminale-spe-ch19-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Bienaymé-Tchebychev · Concentration · Loi des grands nombres
  duree: 2 h
  pdf: terminale-spe-ch19-dsblanc-01-sujet.pdf
- num: 2
  contenu: Concentration · Taille d'échantillon · Loi des grands nombres
  duree: 2 h
  pdf: terminale-spe-ch19-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch19-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch19-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch19-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch19-ds-02-sujet.pdf
erreurs:
- 'Inverser le sens : l''inégalité de Bienaymé-Tchebychev majore $P(|X - \mu| \geq \delta)$ par $\dfrac{V(X)}{\delta^2}$'
- 'Oublier le carré : on divise par $\delta^2$, et la variance $V$ (pas l''écart type $\sigma$) figure au numérateur'
- 'Oublier le facteur $n$ : l''inégalité de concentration donne $P(|M_n - \mu| \geq \delta) \leq \dfrac{V}{n\delta^2}$'
- 'Mal traduire un intervalle : $M_n \in\, ]\mu - \delta ; \mu + \delta[ \iff |M_n - \mu| < \delta$, événement contraire de $|M_n - \mu| \geq \delta$'
- 'Croire que la majoration donne la probabilité exacte : l''inégalité est universelle mais souvent très large (une borne supérieure à 1 ne renseigne pas)'
- Pour une taille d'échantillon, résoudre $\dfrac{V}{n\delta^2} \leq \alpha$ et prendre le plus petit entier $n \geq \dfrac{V}{\alpha\delta^2}$
---
{% include cours-cards.html %}
