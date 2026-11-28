"""Vérifications du carnet Python « Terminale spécialité · Chapitre 20 · Calculer ln 2 : l'algorithme de Brouncker ».

Ce fichier accompagne le carnet ch20-brouncker-ln2.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch20 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_brouncker(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_brouncker', 'verifier_rectangles_inverse', 'verifier_rang_ln2']

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
def _B(n):
    B = 0
    for k in range(1, n + 1):
        B = B + 1 / ((2 * k - 1) * (2 * k))
    return B


def _test_brouncker(brouncker):
    r = brouncker(1)
    _nombre_attendu(r, "brouncker(1)")
    if _proche(r, 2):
        _faux("brouncker(1) renvoie 2 au lieu de 1/2 : sans parenthèses, Python calcule (1 / (2k - 1)) × 2k. Écris "
              "1 / ((2 * k - 1) * (2 * k)).")
    if _proche(r, 0):
        _faux("brouncker(1) renvoie 0 : le terme k = 1 manque. Pour k allant de 1 à n, écris range(1, n + 1).")
    if not _proche(r, 0.5):
        _faux("B_1 = 1/(1 × 2) = 0,5. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(brouncker(2), 7 / 12):
        _faux("B_2 = 1/2 + 1/12 = 7/12 ≈ 0,5833. Ta fonction renvoie " + _montre(brouncker(2)) + ".")
    if not _proche(brouncker(100), _B(100), 1e-12):
        _faux("brouncker(100) doit renvoyer environ 0,690653.")
    return "B_1 = 0,5, B_2 = 7/12 ≈ 0,5833, B_10 ≈ 0,66877 et B_100 ≈ 0,69065 (ln 2 ≈ 0,69315)."


def verifier_brouncker():
    """Vérifie la fonction brouncker."""
    _verifier(_test_brouncker, ["brouncker"],
              aide={"division": "Pour k = 0, le dénominateur (2k - 1)(2k) est nul : la somme commence à k = 1, range(1, n + 1)."})


def _test_rectangles_inverse(rectangles_inverse):
    r = rectangles_inverse(2)
    _nombre_attendu(r, "rectangles_inverse(2)")
    if _proche(r, 7 / 6):
        _faux("rectangles_inverse(2) renvoie 7/6 : tu additionnes les hauteurs sans les multiplier par la largeur h des rectangles.")
    if _proche(r, 1.5):
        _faux("rectangles_inverse(2) renvoie 1,5 : les rectangles sont sur [1 ; 2], l'abscisse est x_k = 1 + k * h.")
    if not _proche(r, 7 / 12):
        _faux("pour n = 2 : 1/2 × 1/(1,5) + 1/2 × 1/2 = 7/12. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(rectangles_inverse(100), _B(100), 1e-12):
        _faux("rectangles_inverse(100) doit être égal à B_100 ≈ 0,690653.")
    return "rectangles_inverse(2) = 7/12 = B_2 et rectangles_inverse(100) = B_100 ≈ 0,690653."


def verifier_rectangles_inverse():
    """Vérifie la fonction rectangles_inverse."""
    _verifier(_test_rectangles_inverse, ["rectangles_inverse"])


def _rang(e):
    n, B = 0, 0
    while _math.log(2) - B >= e:
        n = n + 1
        B = B + 1 / ((2 * n - 1) * (2 * n))
    return n


def _test_rang_ln2(rang_ln2):
    r = rang_ln2(0.01)
    if r == 0:
        _faux("rang_ln2(0.01) renvoie 0 : la boucle ne tourne pas. L'écart positif est log(2) - B (B_n est inférieur à ln 2).")
    if r != 25:
        _faux("rang_ln2(0.01) doit renvoyer 25. Ta fonction renvoie " + _montre(r) + ". B doit accumuler les termes : "
              "B = B + 1 / ((2 * n - 1) * (2 * n)).")
    if rang_ln2(0.001) != _rang(0.001):
        _faux("rang_ln2(0.001) doit renvoyer " + str(_rang(0.001)) + ".")
    return "rang_ln2(0.01) = 25 et rang_ln2(0.001) = 250 : l'écart est voisin de 1/(4n)."


def verifier_rang_ln2():
    """Vérifie la fonction rang_ln2."""
    _verifier(_test_rang_ln2, ["rang_ln2"],
              aide={"boucle": "Ta boucle ne s'arrête pas : B doit augmenter à chaque tour, B = B + 1 / ((2 * n - 1) * (2 * n))."})


print("Vérifications prêtes. Tu peux commencer.")
