# Σ Sigma — Installer les devoirs en ligne (10 minutes)

Ce guide s'adresse au professeur. Aucune connaissance en informatique n'est nécessaire : il suffit de copier-coller un fichier et de cliquer aux bons endroits. Tout se passe dans **votre** compte Google : les noms et les notes des élèves ne quittent jamais votre espace.

**Ce dont vous avez besoin :** un ordinateur (pas un téléphone), votre compte Google (Gmail) et le fichier `tools/devoirs/Code.gs` de ce dépôt.

---

## Étape 1 — Créer la feuille Google (1 min)

1. Ouvrez <https://sheets.google.com> et cliquez sur la grande case **« + » (Vide)**.
2. En haut à gauche, cliquez sur « Feuille de calcul sans titre » et renommez-la **Devoirs Sigma**.
3. Menu **Fichier › Paramètres** : dans « Fuseau horaire », choisissez **(GMT+03:00) Mayotte** (ou Nairobi), puis **Enregistrer les paramètres**. Les dates limites seront ainsi à l'heure de Mayotte.

## Étape 2 — Coller le script (2 min)

1. Dans la feuille, menu **Extensions › Apps Script**. Un nouvel onglet s'ouvre : l'éditeur, avec un fichier `Code.gs` qui contient quelques lignes (`function myFunction() {…}`).
2. Sélectionnez tout ce texte (Ctrl + A) et effacez-le.
3. Ouvrez le fichier `tools/devoirs/Code.gs` du dépôt GitHub (bouton **Raw** pour afficher le texte brut), sélectionnez tout (Ctrl + A), copiez (Ctrl + C), puis collez-le (Ctrl + V) dans l'éditeur.
4. Cliquez sur l'icône **disquette** (Enregistrer) en haut. En haut à gauche, renommez le projet « Projet sans titre » en **Sigma devoirs**.
5. Icône **engrenage** (Paramètres du projet), à gauche : vérifiez que le **fuseau horaire** est aussi « (GMT+03:00) Mayotte ».

## Étape 3 — Lancer l'installation (2 min)

1. Revenez à l'éditeur (icône **< >** à gauche). Dans la barre du haut, à droite de « Exécuter », une liste déroulante indique une fonction : choisissez **installer**, puis cliquez sur **▷ Exécuter**.
2. Google demande une autorisation : **Examiner les autorisations** › choisissez votre compte.
3. Un écran « Google n'a pas validé cette application » apparaît (c'est normal : c'est **votre** script, pas une application publique). Cliquez sur **Paramètres avancés**, puis **Accéder à Sigma devoirs (non sécurisé)**, puis **Autoriser**.
   Le script demande : lire et modifier cette feuille, vous envoyer des courriels, s'exécuter toutes les heures. Il ne lit rien d'autre.
4. En bas, le « Journal d'exécution » affiche « Exécution terminée ». Revenez à la feuille : deux onglets sont apparus, **Réglages** et **Rendus**. Rechargez la page de la feuille (F5) : un menu **Sigma** apparaît à droite de « Aide ».

## Étape 4 — Vérifier les réglages (1 min)

Onglet **Réglages** :

| Ligne | À vérifier |
|---|---|
| Adresse du professeur | votre adresse : c'est là qu'arrivent les récapitulatifs |
| Note retenue dans le récapitulatif | `meilleure` (meilleure note des essais) ou `dernière` |
| Récapitulatif automatique à la date limite | `oui` ou `non` |

Puis, dans le tableau des devoirs (ligne `seconde-ch4-dm1`) :

- **Classes** : `Seconde 219, Seconde 220` (séparées par des virgules) ;
- **Ouvert** : `oui` pour ouvrir le devoir, `non` pour le fermer immédiatement ;
- **Date limite** : par exemple `12/12/2026 23:59`. Une date sans heure vaut « jusqu'à 23 h 59 ce jour-là » ;
- **Essais maximum** : `2` conseillé (chaque nouvel essai donne un sujet avec d'autres nombres) ;
- **Jeton** : ne pas modifier (il doit rester identique à celui du site, fichier `_data/devoirs.yml`) ;
- **Récapitulatif envoyé le** : rempli automatiquement. Effacez-le pour que le récapitulatif reparte à la prochaine échéance (par exemple après avoir repoussé la date limite).

Menu **Sigma › Tester l'envoi d'un courriel** : vous devez recevoir un message « Σ Sigma — test d'envoi ».

## Étape 5 — Publier le script comme application Web (2 min)

1. Dans l'éditeur Apps Script, bouton bleu **Déployer › Nouveau déploiement**.
2. À gauche de « Sélectionner le type », cliquez sur l'**engrenage** › **Application Web**.
3. Remplissez :
   - Description : `Sigma devoirs` ;
   - **Exécuter en tant que : Moi** (votre adresse) ;
   - **Qui peut accéder : Tout le monde** (pas « Tout utilisateur disposant d'un compte Google » : les élèves n'ont pas besoin de compte).
4. **Déployer**. Copiez l'**URL de l'application Web** : elle ressemble à `https://script.google.com/macros/s/AKfy…/exec`.
5. Vérification : collez cette URL dans un nouvel onglet en ajoutant `?action=liste` à la fin. Vous devez voir un texte commençant par `{"ok":true,"devoirs":[…`.

## Étape 6 — Brancher le site (1 min)

Dans le dépôt GitHub du site, ouvrez `_config.yml`, cliquez sur le **crayon** (Modifier) et remplacez la ligne

```yaml
devoirs_url: ""
```

par (avec **votre** URL, entre guillemets) :

```yaml
devoirs_url: "https://script.google.com/macros/s/AKfy…/exec"
```

Puis **Commit changes**. Une à deux minutes plus tard, <https://ibrahim-rudasingwa.fr/devoirs/> affiche « Ouvert · à rendre avant le … » et le mode démo disparaît. Faites un essai complet avec un faux élève (par exemple « Test Professeur ») : une ligne apparaît dans l'onglet **Rendus**. Supprimez ensuite cette ligne (clic droit sur le numéro de ligne › Supprimer la ligne).

Donnez aux élèves le lien du devoir (par PRONOTE par exemple) : `https://ibrahim-rudasingwa.fr/devoirs/seconde-ch4-dm1/`.

---

## Au quotidien

- **Les notes** arrivent dans l'onglet **Rendus** : une ligne par rendu (date, classe, nom, prénom, note sur 20, points par question, durée de travail, numéro d'essai, réponses brutes).
- **Le récapitulatif** (tableau trié par classe puis par nom, moyennes, question la plus échouée) arrive par courriel automatiquement dans l'heure qui suit la date limite. À tout moment : menu **Sigma › Envoyer le récapitulatif maintenant**.
- **Fermer un devoir** : `Ouvert` = `non`. **Prolonger** : changez la date limite (et effacez « Récapitulatif envoyé le » si besoin).
- **Accorder un essai de plus à un élève** : supprimez l'une de ses lignes dans **Rendus**, ou augmentez « Essais maximum ».
- **Fin d'année scolaire** : supprimez les lignes de l'onglet **Rendus** (engagement pris dans les mentions légales du site).

## Si vous modifiez le script plus tard

Après avoir collé une nouvelle version de `Code.gs` : **Déployer › Gérer les déploiements** › icône **crayon** › Version : **Nouvelle version** › **Déployer**. L'URL ne change pas : rien à modifier sur le site. (Créer un « Nouveau déploiement » donnerait une autre URL.)

## En cas de problème

| Symptôme | Solution |
|---|---|
| Le site affiche « Impossible de joindre le serveur des devoirs » | Vérifiez l'URL dans `_config.yml` (elle finit par `/exec`) et l'accès « Tout le monde » du déploiement. |
| « Lien du devoir invalide » | Le jeton de l'onglet Réglages diffère de celui de `_data/devoirs.yml`. |
| Pas de courriel à l'échéance | Éditeur Apps Script › icône **réveil** (Déclencheurs) : une ligne `verifierEcheances` « Toutes les heures » doit exister. Sinon, relancez **Sigma › Installer / réparer**. |
| Un élève dit que son devoir « n'est pas encore envoyé » | Ses réponses sont gardées sur son téléphone : qu'il rouvre la page avec du réseau et touche « Réessayer l'envoi ». Un même envoi n'est jamais compté deux fois. |

---

## Pour la maintenance (développeur)

- `moteur.js` est la **source unique** des sujets et du corrigé. Après modification : `python3 tools/devoirs/sync.py` recopie le moteur dans `Code.gs` et dans `_includes/devoirs/moteur-demo.js` (mode démo, inclus dans la page seulement tant que `devoirs_url` est vide).
- Tests : `node tools/devoirs/tests/harness.js` (serveur avec bouchons Apps Script) et `python3 tools/devoirs/tests/audit.py 300` (audit mathématique sympy). Faux serveur local au même contrat JSON : `node tools/devoirs/tests/fake-server.js 8851`.
- Le dossier `tools/` est exclu de la publication du site (`exclude` dans `_config.yml`). Le dépôt étant public, le code du générateur est lisible sur GitHub ; un **sel secret** propre à votre installation (propriété du script) rend toutefois les sujets imprévisibles, et le corrigé n'est jamais envoyé au navigateur.
- Ajouter un devoir : une entrée dans `DEVOIRS` de `moteur.js`, une ligne dans `_data/devoirs.yml` (avec un nouveau jeton), une page `devoirs/<id>/index.html` (copie de celle du DM 1), puis une ligne dans l'onglet Réglages avec le même identifiant et le même jeton.
