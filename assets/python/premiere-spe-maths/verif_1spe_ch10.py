"""Vérifications du carnet Python « Première spécialité · Chapitre 10 · Sommes de termes et seuils ».

Ce fichier accompagne le carnet ch10-suites-arithmetiques-geometriques.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_1spe_ch10 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_somme_entiers(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_somme_entiers', 'verifier_somme_geo', 'verifier_somme', 'verifier_seuil_valeur', 'verifier_liste_arith']

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
def _test_somme_entiers(somme_entiers):
    r = somme_entiers(100)
    if r == 4950:
        _faux("somme_entiers(100) renvoie 4950 = 1 + ... + 99 : le dernier terme, 100, manque. Écris range(1, n + 1).")
    if r == 100:
        _faux("somme_entiers(100) renvoie 100 : tu ajoutes 1 à chaque tour. Il faut ajouter k : S = S + k.")
    if r != 5050:
        _faux("1 + 2 + ... + 100 = 100 × 101 / 2 = 5050. Ta fonction renvoie " + _montre(r) + ".")
    if somme_entiers(1) != 1 or somme_entiers(10) != 55:
        _faux("somme_entiers(1) doit renvoyer 1 et somme_entiers(10) doit renvoyer 55.")
    return "somme_entiers(100) = 5050 = 100 × 101 / 2 et somme_entiers(10) = 55."


def verifier_somme_entiers():
    """Vérifie la fonction somme_entiers."""
    _verifier(_test_somme_entiers, ["somme_entiers"])


def _test_somme_geo(somme_geo):
    r = somme_geo(2, 10)
    _nombre_attendu(r, "somme_geo(2, 10)")
    if r == 1023:
        _faux("somme_geo(2, 10) renvoie 1023 = 1 + 2 + ... + 2⁹ : il manque q¹⁰. De q⁰ à qⁿ, il y a n + 1 termes : range(n + 1).")
    if r == 4094:
        _faux("somme_geo(2, 10) renvoie 4094 = 2 + 4 + ... + 2¹¹ : tu multiplies t avant de l'ajouter. Ajoute d'abord t à S, "
              "puis passe au terme suivant.")
    if r == 1 + 3 + 5 + 7 + 9 + 11 + 13 + 15 + 17 + 19 + 21:
        _faux("somme_geo(2, 10) renvoie 121 : tu ajoutes q au lieu de multiplier. Le terme suivant est t = t * q.")
    if r != 2047:
        _faux("1 + 2 + ... + 2¹⁰ = (1 - 2¹¹) / (1 - 2) = 2047. Ta fonction renvoie " + _montre(r) + ".")
    for q, n in [(0.5, 3), (3, 5), (-1, 4), (1, 7)]:
        att = sum([q ** k for k in range(n + 1)])
        if not _proche(somme_geo(q, n), att):
            _faux("somme_geo(" + str(q) + ", " + str(n) + ") doit renvoyer " + _ecrire(att) + ". Ta fonction renvoie "
                  + _montre(somme_geo(q, n)) + ".")
    return "somme_geo(2, 10) = 2047, somme_geo(0.5, 3) = 1,875, somme_geo(3, 5) = 364 ; les cas q = -1 et q = 1 sont justes."


def verifier_somme_geo():
    """Vérifie la fonction somme_geo."""
    _verifier(_test_somme_geo, ["somme_geo"])


def _test_somme(somme):
    r = somme(19)
    if r == 3145722:
        _faux("somme(19) renvoie 3 145 722 : il manque u_0 = 3. S doit commencer à u_0 : S = u.")
    if r == 3 * 2 ** 19:
        _faux("somme(19) renvoie " + str(r) + " = u_19 : il faut ajouter chaque terme à S, S = S + u.")
    if r != 3145725:
        _faux("u_0 + ... + u_19 = 3 × (2²⁰ - 1) = 3 145 725. Ta fonction renvoie " + _montre(r) + ".")
    if somme(0) != 3 or somme(2) != 21:
        _faux("somme(0) doit renvoyer u_0 = 3 et somme(2) doit renvoyer 3 + 6 + 12 = 21.")
    return "somme(19) = 3 145 725, somme(2) = 3 + 6 + 12 = 21 et somme(0) = 3."


def verifier_somme():
    """Vérifie la fonction somme."""
    _verifier(_test_somme, ["somme"])


def _seuil(s):
    v, n = 20000, 0
    while v >= s:
        v, n = 0.85 * v, n + 1
    return n


def _test_seuil_valeur(seuil_valeur):
    r = seuil_valeur(5000)
    if r == 1:
        _faux("seuil_valeur(5000) renvoie 1 : perdre 15 %, c'est multiplier par 1 - 0,15 = 0,85 (et non par 0,15) : v = 0.85 * v.")
    if r == 0:
        _faux("seuil_valeur(5000) renvoie 0 : la boucle ne tourne pas. On continue tant que la valeur n'est pas passée sous s : "
              "while v >= s.")
    if r != 9:
        _faux("20000 × 0,85⁸ ≈ 5449,8 ≥ 5000 et 20000 × 0,85⁹ ≈ 4632,3 < 5000 : seuil_valeur(5000) doit renvoyer 9. "
              "Ta fonction renvoie " + _montre(r) + ".")
    for s in [10000, 1, 20000]:
        if seuil_valeur(s) != _seuil(s):
            _faux("seuil_valeur(" + str(s) + ") doit renvoyer " + str(_seuil(s)) + ". Ta fonction renvoie "
                  + _montre(seuil_valeur(s)) + ".")
    return "seuil_valeur(5000) = 9, seuil_valeur(10000) = 5 et seuil_valeur(1) = " + str(_seuil(1)) + "."


def verifier_seuil_valeur():
    """Vérifie la fonction seuil_valeur."""
    _verifier(_test_seuil_valeur, ["seuil_valeur"],
              aide={"boucle": "Vérifie que v diminue à chaque tour (v = 0.85 * v) et que la condition est v >= s."})


def _test_liste_arith(liste_arith):
    r = liste_arith(4)
    _est_liste(r, "liste_arith(4)")
    if r == [5, 8, 11, 14]:
        _faux("liste_arith(4) renvoie 4 termes : de u_0 à u_4, il y en a 5. Écris range(n + 1).")
    if r == [3, 8, 13, 18, 23]:
        _faux("liste_arith(4) renvoie " + _montre(r) + " : tu as échangé le premier terme et la raison. u_k = 5 + 3k.")
    if r != [5, 8, 11, 14, 17]:
        _faux("liste_arith(4) doit renvoyer [5, 8, 11, 14, 17]. Ta fonction renvoie " + _montre(r) + ".")
    if liste_arith(0) != [5]:
        _faux("liste_arith(0) doit renvoyer [5].")
    return "liste_arith(4) = [5, 8, 11, 14, 17] et liste_arith(0) = [5]."


def verifier_liste_arith():
    """Vérifie la fonction liste_arith."""
    _verifier(_test_liste_arith, ["liste_arith"])


print("Vérifications prêtes. Tu peux commencer.")
