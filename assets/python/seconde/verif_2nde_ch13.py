"""Vérifications du carnet Python « Seconde · Chapitre 13 · Moyenne et écart type d'une série ».

Ce fichier accompagne le carnet ch13-moyenne-ecart-type.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch13 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_somme_notes(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_somme_notes', 'verifier_moyenne', 'verifier_ecart_type', 'verifier_nombre_au_moins', 'verifier_proportion_intervalle', 'note']

# ─────────────────────────────────────────────────────────────────────────────
# Mécanique commune des vérifications (elle ne concerne pas l'élève).
# Tout ce qui commence par _ reste invisible après « from ... import * ».
# ─────────────────────────────────────────────────────────────────────────────
import sys as _sys
import io as _io
import re as _re
import contextlib as _contextlib

# Encouragements (Sigma) : une phrase variée après chaque vérification.
import random as _random

_BRAVO = [
    "Bien raisonné !", "Tu vois, tu en es capable.", "Ta méthode est la bonne.",
    "Ton programme fonctionne : c'est toi qui l'as écrit.", "Bravo, tu as pris le temps de réfléchir.",
    "C'est juste : ton travail paie.", "Belle rigueur !", "Tu progresses, continue comme ça.",
    "Bien joué : étape par étape, tu y arrives.", "Excellent : le code et les maths vont ensemble.",
    "Juste ! Garde cette méthode, elle fonctionne.", "Tu as trouvé : la programmation, c'est aussi pour toi.",
    "Solide ! Ton raisonnement est clair.", "Bravo : la persévérance, ça marche.",
    "Réussi ! Et ce n'est pas de la chance.",
]
_COURAGE = [
    "Une erreur, c'est une étape : relis le conseil ci-dessus.", "Pas encore, mais tu cherches : c'est comme ça qu'on apprend.",
    "Ce n'est pas grave : corrige une ligne à la fois, puis relance.", "Tout le monde fait des erreurs en programmant. Continue.",
    "Chaque message d'erreur te rapproche du bon programme.", "Respire, relis ton code : la solution est à ta portée.",
    "Une erreur repérée aujourd'hui, c'est une erreur évitée demain.", "Garde confiance : le conseil te donne la piste.",
    "Courage : comprendre une erreur, c'est apprendre deux fois.", "Essaie ta fonction sur un petit exemple : ça aide souvent.",
    "Tu as le droit de te tromper : c'est comme ça qu'on progresse.", "Ne lâche rien : relance la vérification après ta correction.",
]


def _bravo():
    print("  ★ " + _random.choice(_BRAVO))


def _courage():
    print("  ➜ " + _random.choice(_COURAGE))

_LIMITE = 300000      # nombre de lignes exécutées avant de conclure à une boucle sans fin
_RETURN = ("Le return doit être aligné avec le mot for (ou while) : s'il est décalé à l'intérieur de la boucle, "
           "la fonction s'arrête dès le premier tour.")
_RETURN_OU = ("ou bien ton return est décalé à l'intérieur de la boucle : il doit être aligné avec le mot for, "
              "sinon la fonction s'arrête dès le premier tour.")


class _PasEncore(Exception):
    """Réponse fausse : le message explique pourquoi."""


class _TropLong(Exception):
    """Le code de l'élève tourne trop longtemps (boucle qui ne s'arrête pas)."""


def _faux(message):
    raise _PasEncore(message)


def _montre(r):
    """Écrit pour un élève la valeur obtenue."""
    if r is Ellipsis:
        return "... (il reste des ... à remplacer)"
    if r is None:
        return "None, c'est-à-dire rien (as-tu oublié le return, ou l'as-tu placé à l'intérieur de la boucle ?)"
    if isinstance(r, str):
        return '"' + r + '"'
    if callable(r):
        return "une fonction, et non un nombre (as-tu oublié les parenthèses ?)"
    return repr(r)


def _nombre(x):
    """Écrit un nombre attendu sans décimales inutiles."""
    x = float(x)
    if x == int(x):
        return str(int(x))
    return repr(round(x, 10))


def _est_nombre(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _proche(x, y, tol=1e-9):
    if not _est_nombre(x):
        return False
    try:
        return abs(x - y) <= tol * max(1, abs(y))
    except Exception:
        return False


def _contient_points(code):
    """True si le code d'une fonction contient encore ... (Ellipsis)."""
    for c in code.co_consts:
        if c is Ellipsis:
            return True
        if hasattr(c, "co_consts") and _contient_points(c):
            return True
    return False


def _sortie(f, *valeurs):
    """Appelle f(*valeurs) et renvoie (ce que f renvoie, ce que f affiche)."""
    tampon = _io.StringIO()
    with _contextlib.redirect_stdout(tampon):
        r = f(*valeurs)
    return r, tampon.getvalue()


def _executer(test, objets, g):
    """Lance le test en comptant les lignes exécutées dans le code de l'élève."""
    compte = [0]

    def locale(frame, evenement, arg):
        if evenement == "line":
            compte[0] += 1
            if compte[0] > _LIMITE:
                raise _TropLong()
        return locale

    def globale(frame, evenement, arg):
        if frame.f_globals is g:
            return locale
        return None

    ancien = _sys.gettrace()
    _sys.settrace(globale)
    try:
        return test(*objets)
    finally:
        _sys.settrace(ancien)


def _nom_inconnu(e):
    nom = getattr(e, "name", None)
    if not nom:
        m = _re.search(r"'([^']+)'", str(e))
        nom = m.group(1) if m else "?"
    return nom


def _verifier(test, noms, aide=None):
    """Cherche les noms de l'élève dans le carnet, lance le test, affiche le bilan."""
    aide = aide or {}
    try:
        g = _sys._getframe(2).f_globals
    except Exception:
        import __main__
        g = vars(__main__)
    objets = []
    for nom in noms:
        if nom not in g:
            print("✘ Pas encore : Python ne connaît pas encore « " + nom + " ».")
            print("  → Exécute d'abord la cellule où tu as écrit " + nom
                  + " (Maj + Entrée), puis relance cette vérification.")
            _courage()
            return
        obj = g[nom]
        if obj is Ellipsis:
            print("✘ Pas encore : « " + nom + " » vaut encore ... .")
            print("  → Remplace les ... par ta réponse, exécute la cellule, puis relance cette vérification.")
            _courage()
            return
        code = getattr(obj, "__code__", None)
        if code is not None and _contient_points(code):
            print("✘ Pas encore : il reste des ... à remplacer dans ta fonction " + nom + ".")
            print("  → Remplace chaque ... par ton code, exécute la cellule de ta fonction,"
                  " puis relance cette vérification.")
            _courage()
            return
        objets.append(obj)
    try:
        bilan = _executer(test, objets, g)
    except _PasEncore as e:
        print("✘ Pas encore : " + str(e))
        _courage()
        return
    except _TropLong:
        print("✘ Pas encore : ta fonction ne s'arrête pas (sa boucle a fait des centaines de milliers de tours).")
        print("  → " + aide.get("boucle", "Vérifie ta boucle while : la variable testée doit changer à chaque "
                                          "tour, pour que la condition finisse par devenir fausse."))
        _courage()
        return
    except NameError as e:
        nom = _nom_inconnu(e)
        print("✘ Pas encore : ta fonction utilise le nom « " + nom + " », que Python ne connaît pas.")
        print("  → Vérifie son orthographe (Python distingue majuscules et minuscules). "
              "Si c'est une fonction écrite plus haut dans le carnet, exécute d'abord sa cellule.")
        _courage()
        return
    except ZeroDivisionError:
        print("✘ Pas encore : ta fonction divise par 0, ce qui est impossible.")
        print("  → " + aide.get("division", "Repère la division (/, // ou %) dont le diviseur vaut 0."))
        _courage()
        return
    except IndexError:
        print("✘ Pas encore : ta fonction demande un élément de la liste qui n'existe pas (indice trop grand).")
        print("  → " + aide.get("indice", "Les indices d'une liste de longueur n vont de 0 à n - 1."))
        _courage()
        return
    except RecursionError:
        print("✘ Pas encore : ta fonction s'appelle elle-même sans jamais s'arrêter.")
        _courage()
        return
    except TypeError as e:
        texte = str(e)
        if "ellipsis" in texte.lower():
            print("✘ Pas encore : il reste des ... à remplacer (Python ne sait pas calculer avec ...).")
        elif "NoneType" in texte:
            print("✘ Pas encore : un calcul utilise une valeur vide (None).")
            print("  → Une de tes fonctions ne renvoie rien : vérifie qu'elle se termine par un return.")
        else:
            print("✘ Pas encore : ta fonction fait un calcul impossible "
                  "(par exemple avec un texte au lieu d'un nombre).")
            print("  → " + aide.get("calcul", "Relis chaque ligne de ta fonction : chaque calcul doit porter sur des nombres."))
        _courage()
        return
    except Exception:
        print("✘ Pas encore : ta fonction s'arrête sur une erreur.")
        print("  → Appelle ta fonction toute seule dans une nouvelle cellule (par exemple avec un petit nombre)"
              " pour voir le message de Python, puis relis ton code ligne par ligne.")
        _courage()
        return
    print("✔ Juste : " + bilan)
    _bravo()


# ─────────────────────────────────────────────────────────────────────────────
# Outils communs des vérifications (cachés).
# ─────────────────────────────────────────────────────────────────────────────
import math as _math
import random as _hasard_mod


def _booleen(r, appel, conseil=""):
    if r is not True and r is not False:
        _faux(appel + " doit renvoyer True ou False. Ta fonction renvoie " + _montre(r) + ". " + conseil)


def _affichage(f, *valeurs):
    """Appelle f(*valeurs) et renvoie la liste des lignes affichées (sans les lignes vides)."""
    r, texte = _sortie(f, *valeurs)
    return [ligne.strip() for ligne in texte.split("\n") if ligne.strip() != ""]


def _nombre_attendu(r, appel):
    if r is Ellipsis or r is None or not _est_nombre(r):
        _faux(appel + " doit renvoyer un nombre. Ta fonction renvoie " + _montre(r) + ".")


def _est_liste(r, appel):
    if not isinstance(r, list):
        _faux(appel + " doit renvoyer une liste, écrite entre crochets [ ]. Ta fonction renvoie " + _montre(r) + ".")


def _listes_proches(r, attendu, tol=1e-9):
    if not isinstance(r, list) or len(r) != len(attendu):
        return False
    for i in range(len(r)):
        if not _proche(r[i], attendu[i], tol):
            return False
    return True


class _Graine:
    """Rend le hasard reproductible pendant un test, puis rend au module random son état."""
    def __init__(self, graine):
        self.graine = graine

    def __enter__(self):
        self.etat = _hasard_mod.getstate()
        _hasard_mod.seed(self.graine)

    def __exit__(self, *a):
        _hasard_mod.setstate(self.etat)
        return False


def _ecrire(x, chiffres=6):
    """Écrit un nombre arrondi pour un message."""
    if isinstance(x, int):
        return str(x)
    return repr(round(x, chiffres)).replace(".", ",")

# ─────────────────────────────────────────────────────────────────────────────
# Vérifications du carnet (une fonction par cellule « Vérification »).
# ─────────────────────────────────────────────────────────────────────────────
_NOTES = [12, 8, 15, 10, 14, 9, 11, 17, 6, 13, 10, 12, 16, 7, 11, 14, 9, 12, 18, 5, 13, 10, 15, 11, 12]


def note(i):
    """Renvoie la note de l'élève numéro i (i entier de 0 à 24)."""
    if not (isinstance(i, int) and 0 <= i <= 24):
        raise IndexError("note : le numéro d'élève va de 0 à 24")
    return _NOTES[i]


def _test_somme_notes(somme_notes):
    r = somme_notes()
    if r == 278:
        _faux("somme_notes() renvoie 278 : il manque la note de l'élève 24. Pour i allant de 0 à 24, écris range(25).")
    if r == 12:
        _faux("somme_notes() renvoie 12, la dernière note : il faut ajouter chaque note à s, avec s = s + note(i).")
    if r == 300:
        _faux("somme_notes() renvoie 300 = 0 + 1 + ... + 24 : tu ajoutes les numéros i au lieu des notes. Écris s = s + note(i).")
    if r != 290:
        _faux("la somme des 25 notes vaut 290. Ta fonction renvoie " + _montre(r) + ".")
    return "la somme des 25 notes vaut 290."


def verifier_somme_notes():
    """Vérifie la fonction somme_notes."""
    _verifier(_test_somme_notes, ["somme_notes"],
              aide={"indice": "Les élèves sont numérotés de 0 à 24 : range(25)."})


def _test_moyenne(moyenne):
    r = moyenne()
    if r == 290:
        _faux("moyenne() renvoie 290 : c'est la somme. La moyenne se calcule en divisant par 25 : somme_notes() / 25.")
    if not _proche(r, 11.6):
        _faux("la moyenne est 290 / 25 = 11,6 : on divise par 25, le nombre de notes. Ta fonction renvoie " + _montre(r) + ".")
    return "m = 290 / 25 = 11,6."


def verifier_moyenne():
    """Vérifie la fonction moyenne."""
    _verifier(_test_moyenne, ["moyenne"])


def _test_ecart_type(ecart_type):
    try:
        r = ecart_type()
    except ValueError:
        _faux("Python doit calculer la racine carrée d'un nombre négatif : s2 doit accumuler les carrés des notes, "
              "s2 = s2 + note(i) ** 2.")
    if _proche(r, 10.4):
        _faux("ecart_type() renvoie 10,4 : c'est la variance. L'écart type est sa racine carrée : sqrt(s2 / 25 - m ** 2).")
    if _proche(r, _math.sqrt(3624 / 25 - 11.6)):
        _faux("ecart_type() renvoie environ 11,55 : dans la formule, on soustrait le carré de la moyenne, m ** 2.")
    if not _proche(r, _math.sqrt(10.4), 1e-9):
        _faux("la somme des carrés des notes vaut 3624, donc s = √(3624 / 25 - 11,6²) = √10,4 ≈ 3,2249. Ta fonction renvoie "
              + _montre(r) + ".")
    return "s = √(3624 / 25 - 11,6²) = √10,4 ≈ 3,22."


def verifier_ecart_type():
    """Vérifie la fonction ecart_type."""
    _verifier(_test_ecart_type, ["ecart_type"])


def _test_nombre_au_moins(nombre_au_moins):
    r = nombre_au_moins(10)
    if r == 16:
        _faux("nombre_au_moins(10) renvoie 16 : les trois notes égales à 10 ne sont pas comptées. « Supérieure ou égale » s'écrit >=.")
    if r == sum([x for x in _NOTES if x >= 10]):
        _faux("nombre_au_moins(10) renvoie " + str(r) + " : tu ajoutes les notes au compteur. Un compteur augmente de 1 : compteur = compteur + 1.")
    if r != 19:
        _faux("19 notes sont supérieures ou égales à 10. Ta fonction renvoie " + _montre(r) + ".")
    for seuil, v in [(15, 5), (0, 25), (19, 0), (18, 1)]:
        if nombre_au_moins(seuil) != v:
            _faux("nombre_au_moins(" + str(seuil) + ") doit renvoyer " + str(v) + ". Ta fonction renvoie "
                  + _montre(nombre_au_moins(seuil)) + ".")
    return "19 notes sont au moins égales à 10, 5 au moins égales à 15 ; les cas 0, 18 et 19 sont justes."


def verifier_nombre_au_moins():
    """Vérifie la fonction nombre_au_moins."""
    _verifier(_test_nombre_au_moins, ["nombre_au_moins"])


def _test_proportion_intervalle(proportion_intervalle):
    r = proportion_intervalle()
    if r == 16:
        _faux("proportion_intervalle() renvoie 16 : c'est un effectif. Pour une proportion, divise par l'effectif total : compteur / 25.")
    if _proche(r, 21 / 25) or _proche(r, 21):
        _faux("ta fonction compte aussi les notes inférieures à m - s : la borne inférieure de l'intervalle est m - s.")
    if not _proche(r, 0.64):
        _faux("16 notes sur 25 sont comprises entre m - s ≈ 8,38 et m + s ≈ 14,82 : la proportion est 0,64. Ta fonction renvoie "
              + _montre(r) + ".")
    return "16 notes sur 25, soit 64 %, sont comprises entre m - s ≈ 8,38 et m + s ≈ 14,82."


def verifier_proportion_intervalle():
    """Vérifie la fonction proportion_intervalle."""
    _verifier(_test_proportion_intervalle, ["proportion_intervalle"])


print("Vérifications prêtes. Tu peux commencer.")
