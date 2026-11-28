"""Vérifications du carnet Python « Terminale spécialité · Chapitre 15 · Équations différentielles : la méthode d'Euler ».

Ce fichier accompagne le carnet ch15-methode-euler.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch15 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_euler_primitive(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_euler_primitive', 'verifier_euler_affine', 'verifier_solution_exacte', 'verifier_ecart']

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
def _test_euler_primitive(euler_primitive):
    r = euler_primitive(0.1, 3)
    _est_liste(r, "euler_primitive(0.1, 3)")
    if len(r) != 4:
        _faux("euler_primitive(0.1, 3) doit renvoyer 4 valeurs, de y_0 à y_3. Ta liste en contient " + str(len(r)) + ".")
    if _listes_proches(r, [0, 0.02, 0.06, 0.12]):
        _faux("euler_primitive(0.1, 3) renvoie [0, 0.02, 0.06, 0.12] : tu calcules f en x_(k+1) au lieu de x_k. Respecte l'ordre : "
              "d'abord y = y + h * f(x), puis x = x + h.")
    if _listes_proches(r, [0, 0, 0.2, 0.6]):
        _faux("euler_primitive(0.1, 3) renvoie [0, 0, 0.2, 0.6] : on ajoute h × f(x_k), et non f(x_k) : y = y + h * f(x).")
    if not _listes_proches(r, [0, 0, 0.02, 0.06]):
        _faux("y_1 = 0 + 0,1 × f(0) = 0 ; y_2 = 0 + 0,1 × f(0,1) = 0,02 ; y_3 = 0,02 + 0,1 × 0,4 = 0,06. Ta fonction renvoie "
              + _montre(r) + ".")
    r = euler_primitive(0.01, 100)
    if not _proche(r[100], 0.99, 1e-9):
        _faux("le dernier terme de euler_primitive(0.01, 100) doit valoir 0,99.")
    return "euler_primitive(0.1, 3) = [0, 0, 0.02, 0.06] ; avec h = 0,01, y_100 = 0,99 ≈ 1² (valeur exacte 1)."


def verifier_euler_primitive():
    """Vérifie la fonction euler_primitive."""
    _verifier(_test_euler_primitive, ["euler_primitive"])


def _ea(y0, h, n):
    y, Y = y0, [y0]
    for k in range(n):
        y = y + h * (3 * y + 5)
        Y.append(y)
    return Y


def _test_euler_affine(euler_affine):
    r = euler_affine(1, 0.1, 3)
    _est_liste(r, "euler_affine(1, 0.1, 3)")
    if len(r) != 4:
        _faux("euler_affine(1, 0.1, 3) doit renvoyer 4 valeurs. Ta liste en contient " + str(len(r)) + ".")
    if _proche(r[1], 6.3):
        _faux("y_1 vaut 6,3 dans ta liste : sans parenthèses, Python calcule y + h × 3y + 5. Écris y + h * (3 * y + 5).")
    if _proche(r[1], 1.3):
        _faux("y_1 vaut 1,3 dans ta liste : la dérivée est 3y + 5, il manque + 5 : y + h * (3 * y + 5).")
    if not _listes_proches(r, [1, 1.8, 2.84, 4.192]):
        _faux("y_1 = 1 + 0,1 × 8 = 1,8 ; y_2 = 2,84 ; y_3 = 4,192. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(euler_affine(1, 0.1, 10)[10], _ea(1, 0.1, 10)[10], 1e-9):
        _faux("le dernier terme de euler_affine(1, 0.1, 10) doit valoir environ 35,10.")
    return "euler_affine(1, 0.1, 3) = [1, 1.8, 2.84, 4.192] et y_10 ≈ 35,10 avec h = 0,1."


def verifier_euler_affine():
    """Vérifie la fonction euler_affine."""
    _verifier(_test_euler_affine, ["euler_affine"])


def _ex(x):
    return 8 / 3 * _math.exp(3 * x) - 5 / 3


def _test_solution_exacte(solution_exacte):
    r = solution_exacte(0)
    _nombre_attendu(r, "solution_exacte(0)")
    if _proche(r, 13 / 3):
        _faux("solution_exacte(0) renvoie 13/3 au lieu de y(0) = 1 : la solution constante est -5/3, donc on soustrait 5/3.")
    if not _proche(r, 1):
        _faux("la condition initiale impose y(0) = 1. Ta fonction renvoie " + _montre(r) + ".")
    if _proche(solution_exacte(1), 8 / 3 * _math.e - 5 / 3):
        _faux("solution_exacte(1) renvoie 8/3 × e - 5/3 : les solutions de y' = 3y + 5 font intervenir exp(3x), écris exp(3 * x).")
    if not _proche(solution_exacte(1), _ex(1), 1e-9) or not _proche(solution_exacte(0.5), _ex(0.5), 1e-9):
        _faux("solution_exacte(1) doit valoir 8/3 × e³ - 5/3 ≈ 51,89.")
    return "y(0) = 1 et y(1) = 8/3 × e³ - 5/3 ≈ 51,89."


def verifier_solution_exacte():
    """Vérifie la fonction solution_exacte."""
    _verifier(_test_solution_exacte, ["solution_exacte"])


def _test_ecart(ecart):
    try:
        r = ecart(10)
    except OverflowError:
        _faux("les valeurs deviennent énormes : le pas doit être h = 1 / n (et non n).")
    _nombre_attendu(r, "ecart(10)")
    att = abs(_ex(1) - _ea(1, 0.1, 10)[10])
    if _proche(r, _ex(1) - 1):
        _faux("ecart(10) renvoie y(1) - 1 : tu compares avec y_0. Le dernier terme de la liste est Y[n].")
    if not _proche(r, att, 1e-9):
        _faux("ecart(10) doit renvoyer environ " + _ecrire(att, 4) + ". Ta fonction renvoie " + _montre(r)
              + ". Le pas est h = 1 / n et on compare y(1) à Y[n].")
    if not _proche(ecart(100), abs(_ex(1) - _ea(1, 0.01, 100)[100]), 1e-9):
        _faux("ecart(100) doit renvoyer environ " + _ecrire(abs(_ex(1) - _ea(1, 0.01, 100)[100]), 4) + ".")
    return "ecart(10) ≈ " + _ecrire(att, 3) + " et ecart(100) ≈ " + _ecrire(abs(_ex(1) - _ea(1, 0.01, 100)[100]), 3) + "."


def verifier_ecart():
    """Vérifie la fonction ecart."""
    _verifier(_test_ecart, ["ecart"],
              aide={"indice": "La liste Y contient n + 1 valeurs, d'indices 0 à n : le dernier terme est Y[n]."})


print("Vérifications prêtes. Tu peux commencer.")
