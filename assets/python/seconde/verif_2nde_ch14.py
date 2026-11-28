"""Vérifications du carnet Python « Seconde · Chapitre 14 · Approcher un maximum, mesurer une courbe ».

Ce fichier accompagne le carnet ch14-extremum-longueur-courbe.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch14 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_balayage_max(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_balayage_max', 'verifier_maximum', 'verifier_dichotomie_max', 'verifier_distance', 'verifier_longueur']

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
def _f(x):
    return -7 * x ** 2 + 3 * x + 1


def _bal(pas):
    x = -1
    while _f(x + pas) > _f(x):
        x = x + pas
    return x


def _test_balayage_max(balayage_max):
    r = balayage_max(0.1)
    _nombre_attendu(r, "balayage_max(0.1)")
    if _proche(r, -1):
        _faux("balayage_max(0.1) renvoie -1 : la boucle ne tourne pas. On avance tant que f augmente : "
              "la condition est f(x + pas) > f(x).")
    if _proche(r, _f(0.2), 1e-6):
        _faux("balayage_max(0.1) renvoie environ 1,32 : c'est une valeur de f. La fonction doit renvoyer l'abscisse x : return x.")
    if not _proche(r, 0.2, 1e-6):
        _faux("avec le pas 0,1, f augmente jusqu'à x = 0,2 puis diminue (f(0,3) = 1,27 < f(0,2) = 1,32) : balayage_max(0.1) "
              "doit renvoyer 0,2. Ta fonction renvoie " + _montre(r) + ".")
    r = balayage_max(0.001)
    if not _proche(r, _bal(0.001), 1e-6):
        _faux("balayage_max(0.001) doit renvoyer environ 0,214. Ta fonction renvoie " + _montre(r)
              + ". Dans la boucle, x avance du pas choisi : x = x + pas.")
    return "balayage_max(0.1) ≈ 0,2 et balayage_max(0.001) ≈ 0,214."


def verifier_balayage_max():
    """Vérifie la fonction balayage_max."""
    _verifier(_test_balayage_max, ["balayage_max"],
              aide={"boucle": "Dans la boucle, x doit avancer : x = x + pas, et la condition compare f(x + pas) à f(x)."})


def _test_maximum(maximum):
    r = maximum(0.001)
    _nombre_attendu(r, "maximum(0.001)")
    if _proche(r, _bal(0.001), 1e-6):
        _faux("maximum(0.001) renvoie environ 0,214 : c'est l'abscisse du maximum. Le maximum est l'image de cette abscisse : "
              "f(balayage_max(pas)).")
    if not _proche(r, _f(_bal(0.001)), 1e-9):
        _faux("maximum(0.001) doit renvoyer environ 1,32143. Ta fonction renvoie " + _montre(r) + ".")
    return "maximum(0.001) ≈ 1,32143 (la valeur exacte est 37/28 ≈ 1,321429)."


def verifier_maximum():
    """Vérifie la fonction maximum."""
    _verifier(_test_maximum, ["maximum"])


def _dic(a, b, e):
    while b - a > e:
        c = (a + b) / 2
        if _f(c) < _f(c + 0.000001):
            a = c
        else:
            b = c
    return a


def _test_dichotomie_max(dichotomie_max):
    r = dichotomie_max(-1, 2, 0.001)
    _nombre_attendu(r, "dichotomie_max(-1, 2, 0.001)")
    if _proche(r, -1):
        _faux("dichotomie_max(-1, 2, 0.001) renvoie -1 : la boucle ne tourne pas, ou a ne change jamais. On continue tant que "
              "l'intervalle est trop large : b - a > e ; si f augmente encore après c, on remplace a par c.")
    if r > 1.9 or r < -0.9:
        _faux("dichotomie_max(-1, 2, 0.001) renvoie " + _ecrire(r) + " : le maximum n'est pas là. Si f(c) < f(c + 0,000001), "
              "f est encore croissante, donc le maximum est à droite de c : a = c ; sinon b = c.")
    if r > 1.5:
        _faux("dichotomie_max(-1, 2, 0.001) renvoie " + _ecrire(r) + " : quand f n'augmente plus après c, il faut remplacer b par c (b = c).")
    if not _proche(r, _dic(-1, 2, 0.001), 1e-12):
        _faux("dichotomie_max(-1, 2, 0.001) doit renvoyer environ 0,2141. Ta fonction renvoie " + _montre(r) + ".")
    if not abs(dichotomie_max(-1, 2, 0.000001) - 3 / 14) < 0.000002:
        _faux("avec la précision 0,000001, le résultat doit être à moins de 0,000002 de 3/14 ≈ 0,2142857.")
    return "dichotomie_max(-1, 2, 0.001) ≈ 0,2141 en 12 étapes ; avec e = 0,000001, on trouve 0,214285… ≈ 3/14."


def verifier_dichotomie_max():
    """Vérifie la fonction dichotomie_max."""
    _verifier(_test_dichotomie_max, ["dichotomie_max"],
              aide={"boucle": "À chaque tour, l'une des deux bornes doit être remplacée par c : a = c dans un cas, b = c dans "
                              "l'autre ; sinon l'amplitude b - a ne diminue pas."})


def _test_distance(distance):
    r = distance(0, 0, 3, 4)
    _nombre_attendu(r, "distance(0, 0, 3, 4)")
    if _proche(r, 25):
        _faux("distance(0, 0, 3, 4) renvoie 25 = 3² + 4² : il manque la racine carrée, sqrt(...).")
    if not _proche(r, 5):
        _faux("la distance entre (0 ; 0) et (3 ; 4) vaut √(3² + 4²) = 5. Ta fonction renvoie " + _montre(r)
              + ". Vérifie les parenthèses : sqrt((xB - xA) ** 2 + (yB - yA) ** 2).")
    if not _proche(distance(1, 2, -2, -2), 5) or not _proche(distance(0, 1, 1, 0), _math.sqrt(2)):
        _faux("distance(1, 2, -2, -2) doit renvoyer 5 et distance(0, 1, 1, 0) doit renvoyer √2 ≈ 1,414. "
              "Vérifie les parenthèses : sqrt((xB - xA) ** 2 + (yB - yA) ** 2).")
    return "distance(0, 0, 3, 4) = 5, distance(1, 2, -2, -2) = 5 et distance(0, 1, 1, 0) = √2."


def verifier_distance():
    """Vérifie la fonction distance."""
    _verifier(_test_distance, ["distance"])


def _lg(n):
    L = 0
    for k in range(n):
        x1, x2 = k / n, (k + 1) / n
        L = L + _math.sqrt((x2 - x1) ** 2 + (_math.sqrt(1 - x2 ** 2) - _math.sqrt(1 - x1 ** 2)) ** 2)
    return L


def _test_longueur(longueur):
    try:
        r = longueur(1)
    except ValueError:
        _faux("Python doit calculer la racine carrée d'un nombre négatif : une abscisse dépasse 1. "
              "Le point d'arrivée du segment k a pour abscisse (k + 1) / n, avec des parenthèses.")
    _nombre_attendu(r, "longueur(1)")
    if not _proche(r, _math.sqrt(2)):
        _faux("avec un seul segment, de (0 ; 1) à (1 ; 0), la longueur vaut √2 ≈ 1,414. Ta fonction renvoie " + _montre(r)
              + ". Appelle distance avec, dans l'ordre : x1, g(x1), x2, g(x2).")
    try:
        r = longueur(10)
    except ValueError:
        _faux("Python doit calculer la racine carrée d'un nombre négatif : écris x2 = (k + 1) / n, avec des parenthèses.")
    if _proche(r, _lg(10) / 10, 1e-6) or r < 0.5:
        _faux("longueur(10) renvoie " + _ecrire(r) + " : c'est la longueur d'un seul segment. Il faut ajouter chaque longueur "
              "à L : L = L + distance(...).")
    if not _proche(r, _lg(10), 1e-9):
        _faux("longueur(10) doit renvoyer environ " + _ecrire(_lg(10)) + ". Ta fonction renvoie " + _montre(r)
              + ". Appelle distance avec les coordonnées dans l'ordre : x1, g(x1), x2, g(x2).")
    r = longueur(1000)
    if not _proche(r, _lg(1000), 1e-9):
        _faux("longueur(1000) doit renvoyer environ " + _ecrire(_lg(1000)) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "longueur(1) = √2 ≈ 1,414, longueur(10) ≈ " + _ecrire(_lg(10), 4) + " et longueur(1000) ≈ " + _ecrire(_lg(1000), 6) + "."


def verifier_longueur():
    """Vérifie la fonction longueur."""
    _verifier(_test_longueur, ["longueur"])


print("Vérifications prêtes. Tu peux commencer.")
