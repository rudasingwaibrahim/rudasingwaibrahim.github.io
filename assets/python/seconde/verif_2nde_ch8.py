"""Vérifications du carnet Python « Seconde · Chapitre 8 · Valeur absolue, distance et intervalles ».

Ce fichier accompagne le carnet ch8-valeur-absolue-intervalles.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch8 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_valeur_absolue(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_valeur_absolue', 'verifier_distance', 'verifier_appartient_intervalle', 'verifier_proche']

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
def _test_valeur_absolue(valeur_absolue):
    r = valeur_absolue(-5)
    if valeur_absolue(5) == -5:
        _faux("valeur_absolue(5) renvoie -5 : tu as échangé les deux cas. Une valeur absolue est toujours positive ou nulle : "
              "si x >= 0, on renvoie x ; sinon, -x.")
    if r == -5:
        _faux("valeur_absolue(-5) renvoie -5 : pour x < 0, la valeur absolue est -x (ici 5). Dans le else : return -x.")
    if r != 5:
        _faux("|-5| = 5. Ta fonction renvoie " + _montre(r) + ".")
    for x, v in [(5, 5), (0, 0), (-3.4, 3.4), (13, 13), (-0.001, 0.001)]:
        if not _proche(valeur_absolue(x), v):
            _faux("|" + str(x) + "| = " + str(v) + ". Ta fonction renvoie " + _montre(valeur_absolue(x)) + ".")
    return "|-5| = 5, |5| = 5, |0| = 0, |-3,4| = 3,4."


def verifier_valeur_absolue():
    """Vérifie la fonction valeur_absolue."""
    _verifier(_test_valeur_absolue, ["valeur_absolue"])


def _test_distance(distance):
    r = distance(3, 7)
    if r == -4:
        _faux("distance(3, 7) renvoie -4 : une distance n'est jamais négative. Si a < b, la distance est b - a.")
    if r == 10:
        _faux("distance(3, 7) renvoie 10 : la distance est une différence (7 - 3 = 4), pas une somme.")
    if r != 4:
        _faux("la distance entre 3 et 7 est 7 - 3 = 4. Ta fonction renvoie " + _montre(r) + ".")
    r = distance(12, 5)
    if r == -7:
        _faux("distance(12, 5) renvoie -7 : une distance n'est jamais négative. Si a >= b, la distance est a - b.")
    if r != 7:
        _faux("la distance entre 12 et 5 est 12 - 5 = 7. Ta fonction renvoie " + _montre(r) + ".")
    for a, b, v in [(-2, 5, 7), (-6, -2, 4), (4, 4, 0), (-1.5, 2, 3.5)]:
        if not _proche(distance(a, b), v):
            _faux("la distance entre " + str(a) + " et " + str(b) + " vaut " + str(v) + ". Ta fonction renvoie "
                  + _montre(distance(a, b)) + ".")
    return "distance(3, 7) = 4, distance(12, 5) = 7, distance(-2, 5) = 7, distance(-6, -2) = 4."


def verifier_distance():
    """Vérifie la fonction distance."""
    _verifier(_test_distance, ["distance"])


def _test_appartient_intervalle(appartient_intervalle):
    r = appartient_intervalle(3, 1, 5)
    _booleen(r, "appartient_intervalle(3, 1, 5)", "Écris une comparaison : a <= x <= b.")
    if r is not True:
        _faux("1 ≤ 3 ≤ 5 : appartient_intervalle(3, 1, 5) doit renvoyer True. Ta fonction renvoie " + _montre(r)
              + ". Le test est a <= x <= b.")
    if appartient_intervalle(1, 1, 5) is not True or appartient_intervalle(5, 1, 5) is not True:
        _faux("l'intervalle [1 ; 5] est fermé : les bornes 1 et 5 lui appartiennent. Utilise <= et non < .")
    if appartient_intervalle(7, 1, 5) is not False or appartient_intervalle(-2, 1, 5) is not False:
        _faux("7 et -2 n'appartiennent pas à [1 ; 5], mais ta fonction répond True pour l'un d'eux. "
              "Les deux conditions doivent être vraies en même temps (and) : a <= x <= b.")
    if appartient_intervalle(-0.5, -1, 0) is not True or appartient_intervalle(0.01, -1, 0) is not False:
        _faux("-0,5 appartient à [-1 ; 0], mais pas 0,01 : ta fonction répond autrement.")
    return "3, 1 et 5 appartiennent à [1 ; 5], 7 et -2 non ; les cas avec [-1 ; 0] sont justes."


def verifier_appartient_intervalle():
    """Vérifie la fonction appartient_intervalle."""
    _verifier(_test_appartient_intervalle, ["appartient_intervalle"])


def _test_proche(proche):
    r = proche(4, 3, 2)
    _booleen(r, "proche(4, 3, 2)", "Compare la distance à r : distance(x, a) <= r.")
    if r is not True:
        _faux("la distance entre 4 et 3 est 1 ≤ 2 : proche(4, 3, 2) doit renvoyer True.")
    if proche(5, 3, 2) is not True or proche(1, 3, 2) is not True:
        _faux("la distance entre 5 et 3 vaut 2 : |5 - 3| ≤ 2 est vrai, proche(5, 3, 2) doit renvoyer True (de même pour 1). "
              "Utilise <= et non <.")
    if proche(0, 3, 2) is not False:
        _faux("|0 - 3| = 3 > 2 : proche(0, 3, 2) doit renvoyer False. Ta fonction répond True : utilise la distance "
              "(toujours positive), et non la différence x - a.")
    if proche(-1, 3, 2) is not False or proche(5.5, 3, 2) is not False:
        _faux("|-1 - 3| = 4 et |5,5 - 3| = 2,5 sont supérieurs à 2 : proche doit renvoyer False.")
    return "proche(4, 3, 2), proche(5, 3, 2) et proche(1, 3, 2) renvoient True ; proche(0, 3, 2) et proche(-1, 3, 2) renvoient False."


def verifier_proche():
    """Vérifie la fonction proche."""
    _verifier(_test_proche, ["proche"])


print("Vérifications prêtes. Tu peux commencer.")
