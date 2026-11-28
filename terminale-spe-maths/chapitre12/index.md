---
title: Chapitre 12 — Fonction logarithme 1/2
permalink: /classes/terminale-spe-maths/chapitre12/
hero_title: Chapitre 12
hero_subtitle: Fonction logarithme népérien — Propriétés algébriques, équations et inéquations
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch12-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch12-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch12-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch12-planche-02.pdf
dm_published: true
dm:
- num: 1
  contenu: Domaines · Propriétés algébriques · Équations
  duree: 1 semaine
  pdf: terminale-spe-ch12-dm-01-sujet.pdf
- num: 2
  contenu: Encadrements · Changement de variable · Inéquations
  duree: 1 semaine
  pdf: terminale-spe-ch12-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Suites et logarithme · Somme télescopique
  duree: 4 h
  pdf: terminale-spe-ch12-dsblanc-01-sujet.pdf
- num: 2
  contenu: Équations · Signe d'une fonction avec ln
  duree: 4 h
  pdf: terminale-spe-ch12-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch12-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch12-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch12-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch12-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch12-ds-03-sujet.pdf
python:
- titre: "Calculer un logarithme : l'algorithme de Briggs"
  fichier: /assets/python/terminale-spe-maths/ch12-algorithme-briggs.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch12.py
  duree: "35 min"
  contenu: "Algorithme de Briggs · ln(x) pour x ≥ 1 par divisions par e · ln(x) pour 0 < x < 1 · Comparaison avec math.log"
erreurs:
- 'Écrire $\ln(a+b)=\ln a+\ln b$ : c''est faux, la propriété est $\ln(ab)=\ln a+\ln b$ pour $a,b>0$'
- 'Oublier le domaine de validité : $\ln(x-1)+\ln(x+1)=\ln 3$ impose $x>1$, donc seule $x=2$ convient'
- 'Écrire $\ln(x^2)=2\ln x$ pour tout $x\neq 0$ : c''est vrai seulement pour $x>0$ ; en général $\ln(x^2)=2\ln|x|$'
- Oublier de changer le sens de l'inégalité en divisant par $\ln q<0$ quand $0<q<1$
- 'Résoudre $\mathrm{e}^x=-3$ : cette équation n''a pas de solution car $\mathrm{e}^x>0$'
- Confondre $\ln(\mathrm{e}^x)=x$ (pour tout réel $x$) et $\mathrm{e}^{\ln x}=x$ (seulement pour $x>0$)
---
{% include cours-cards.html %}
