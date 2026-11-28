"""Vérifications du carnet Python « Seconde · Chapitre 6 · Encadrer √2 par balayage ».

Ce fichier accompagne le carnet ch6-balayage-racine-2.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch6 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_balayage(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_balayage', 'verifier_nombre_etapes', 'verifier_balayage_fin', 'verifier_encadrement']

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
def _bal(pas, c=2, a=1):
    while (a + pas) ** 2 <= c:
        a = a + pas
    return a


def _test_balayage(balayage):
    r = balayage(0.1)
    _nombre_attendu(r, "balayage(0.1)")
    if _proche(r, 1.5, 1e-6):
        _faux("balayage(0.1) renvoie 1,5, mais 1,5² = 2,25 > 2. Ta condition teste a lui-même : il faut tester le nombre suivant "
              "a + pas, avec (a + pas) ** 2 <= 2, pour s'arrêter avant de dépasser √2.")
    if r >= 1.9:
        _faux("balayage(0.1) renvoie " + _ecrire(r) + " : la boucle va trop loin. Mets des parenthèses : (a + pas) ** 2. "
              "Sans elles, Python calcule a + (pas ** 2).")
    if _proche(r, 0.1, 1e-6):
        _faux("balayage(0.1) renvoie 0,1 : a doit avancer d'un pas à chaque tour, avec a = a + pas.")
    if not _proche(r, 1.4, 1e-6):
        _faux("1,4² = 1,96 ≤ 2 et 1,5² = 2,25 > 2 : balayage(0.1) doit renvoyer 1,4. Ta fonction renvoie " + _montre(r) + ".")
    r = balayage(0.01)
    if not _proche(r, 1.41, 1e-6):
        _faux("balayage(0.01) doit renvoyer 1,41 (1,41² = 1,9881 et 1,42² = 2,0164). Ta fonction renvoie " + _montre(r)
              + ". Dans la boucle, a avance du pas choisi : a = a + pas.")
    r = balayage(0.001)
    if not _proche(r, 1.414, 1e-6):
        _faux("balayage(0.001) doit renvoyer 1,414. Ta fonction renvoie " + _montre(r) + ".")
    return "balayage(0.1) ≈ 1,4, balayage(0.01) ≈ 1,41 et balayage(0.001) ≈ 1,414."


def verifier_balayage():
    """Vérifie la fonction balayage."""
    _verifier(_test_balayage, ["balayage"],
              aide={"boucle": "Dans la boucle, a doit avancer d'un pas : a = a + pas, et la condition doit porter sur (a + pas) ** 2."})


def _etapes(pas):
    a, c = 1, 0
    while (a + pas) ** 2 <= 2:
        a, c = a + pas, c + 1
    return c


def _test_nombre_etapes(nombre_etapes):
    r = nombre_etapes(0.1)
    if _est_nombre(r) and _proche(r, 1.4, 1e-6):
        _faux("nombre_etapes(0.1) renvoie 1,4 : c'est la valeur de a. La fonction doit renvoyer le compteur : return compteur.")
    if r == 1:
        _faux("nombre_etapes(0.1) renvoie 1 : compteur doit augmenter de 1 à chaque tour : compteur = compteur + 1.")
    if r != 4:
        _faux("de 1 à 1,4, on avance 4 fois du pas 0,1 : nombre_etapes(0.1) doit renvoyer 4. Ta fonction renvoie " + _montre(r) + ".")
    for p in [0.01, 0.001]:
        if nombre_etapes(p) != _etapes(p):
            _faux("nombre_etapes(" + str(p) + ") doit renvoyer " + str(_etapes(p)) + ". Ta fonction renvoie "
                  + _montre(nombre_etapes(p)) + ".")
    return "4 étapes pour le pas 0,1, 41 pour 0,01 et 414 pour 0,001."


def verifier_nombre_etapes():
    """Vérifie la fonction nombre_etapes."""
    _verifier(_test_nombre_etapes, ["nombre_etapes"])


def _fin(c, n, k0):
    a = 0 if k0 == 0 else 1
    for k in range(k0, n + 1):
        a = _bal(10 ** (-k), c, a)
    return a


def _test_balayage_fin(balayage_fin):
    r = balayage_fin(3)
    _nombre_attendu(r, "balayage_fin(3)")
    if _proche(r, 1.41, 1e-6):
        _faux("balayage_fin(3) renvoie 1,41 : il manque la dernière décimale. Pour k allant de 1 à n, écris range(1, n + 1).")
    if r == 1:
        _faux("balayage_fin(3) renvoie 1 : le pas doit être 10 ** (-k) (0,1 puis 0,01 puis 0,001), et non 10 ** k.")
    if not _proche(r, 1.414, 1e-6):
        _faux("balayage_fin(3) doit renvoyer 1,414. Ta fonction renvoie " + _montre(r) + ". Le pas est 10 ** (-k).")
    r = balayage_fin(7)
    if not _proche(r, 1.4142135, 1e-7):
        _faux("balayage_fin(7) doit renvoyer 1,4142135. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(balayage_fin(1), 1.4, 1e-6):
        _faux("balayage_fin(1) doit renvoyer 1,4.")
    return "balayage_fin(3) ≈ 1,414 et balayage_fin(7) ≈ 1,4142135."


def verifier_balayage_fin():
    """Vérifie la fonction balayage_fin."""
    _verifier(_test_balayage_fin, ["balayage_fin"],
              aide={"boucle": "Ton balayage est beaucoup trop long. Écris a = 1 une seule fois, avant la boucle for : "
                              "chaque nouveau pas repart du nombre a déjà trouvé. Vérifie aussi le pas : 10 ** (-k)."})


def _test_encadrement(encadrement):
    r = encadrement(9, 2)
    _nombre_attendu(r, "encadrement(9, 2)")
    if _proche(r, 1.41, 1e-6):
        _faux("encadrement(9, 2) renvoie 1,41 : c'est une valeur approchée de √2. La condition du while doit comparer à c : "
              "(a + pas) ** 2 <= c.")
    if not _proche(r, 3, 1e-6):
        _faux("√9 = 3 : encadrement(9, 2) doit renvoyer 3. Ta fonction renvoie " + _montre(r) + ".")
    if _proche(encadrement(0.5, 3), 1, 1e-9):
        _faux("encadrement(0.5, 3) renvoie 1, alors que 1² = 1 > 0,5 : pour c < 1, on a √c < 1. "
              "Il faut partir de a = 0.")
    for c, n in [(2, 5), (3, 4), (0.5, 3), (150, 2)]:
        r = encadrement(c, n)
        if not _proche(r, _fin(c, n, 0), 1e-7):
            _faux("encadrement(" + str(c) + ", " + str(n) + ") doit renvoyer " + _ecrire(_fin(c, n, 0), n)
                  + ". Ta fonction renvoie " + _montre(r) + ".")
    return "encadrement(9, 2) ≈ 3, encadrement(3, 4) ≈ 1,7320, encadrement(0.5, 3) ≈ 0,707 et encadrement(150, 2) ≈ 12,24."


def verifier_encadrement():
    """Vérifie la fonction encadrement."""
    _verifier(_test_encadrement, ["encadrement"],
              aide={"boucle": "Utilise une boucle for sur k (range(0, n + 1)), le pas 10 ** (-k) et, dedans, "
                              "le while du balayage avec (a + pas) ** 2 <= c."})


print("Vérifications prêtes. Tu peux commencer.")
