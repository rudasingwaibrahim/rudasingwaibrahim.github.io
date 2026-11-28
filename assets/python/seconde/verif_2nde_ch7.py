"""Vérifications du carnet Python « Seconde · Chapitre 7 · Fonctions, images et appartenance à une courbe ».

Ce fichier accompagne le carnet ch7-fonctions-courbes.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch7 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_f(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_f', 'verifier_appartient', 'verifier_sur_droite', 'verifier_afficher_antecedents']

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
def _test_f(f):
    r = f(2)
    if r is None:
        _faux("f(2) ne renvoie rien (None) : ta fonction affiche peut-être le résultat avec print. Elle doit le renvoyer avec return.")
    if f(0) == -1 and f(3) == 1:
        _faux("f(0) renvoie -1 et f(3) renvoie 1 : tu as sans doute écrit x ^ 2. En Python, le carré s'écrit x ** 2 "
              "(le symbole ^ est un autre opérateur).")
    if r == 2 and f(3) == 1:
        _faux("f(2) renvoie 2 : tu as sans doute écrit x ^ 2. En Python, le carré s'écrit x ** 2 (le symbole ^ est un autre opérateur).")
    if r == 3 and f(3) == 6:
        _faux("f(3) renvoie 6 : ta fonction calcule 2x au lieu du carré. Le carré de x s'écrit x ** 2.")
    if r != 3:
        _faux("f(2) = 2² + 2 - 3 = 3. Ta fonction renvoie " + _montre(r) + ".")
    for x, v in [(0, -3), (-4, 9), (10, 107), (0.5, -2.25)]:
        if not _proche(f(x), v):
            _faux("f(" + str(x) + ") = " + _ecrire(v) + ". Ta fonction renvoie " + _montre(f(x)) + ".")
    return "f(2) = 3, f(0) = -3, f(-4) = 9, f(10) = 107 et f(0,5) = -2,25."


def verifier_f():
    """Vérifie la fonction f."""
    _verifier(_test_f, ["f"])


def _test_appartient(appartient):
    r = appartient(2, 3)
    if r is not True and r is not False:
        _faux("appartient(2, 3) doit renvoyer True ou False. Ta fonction renvoie " + _montre(r)
              + ". Compare y à f(x) avec == : y == f(x).")
    if r is False and appartient(0, 0) is True:
        _faux("ta fonction répond l'inverse : appartient(2, 3) renvoie False alors que f(2) = 3. Utilise == (et non !=).")
    if r is not True:
        _faux("f(2) = 3 : le point (2 ; 3) est sur la courbe, appartient(2, 3) doit renvoyer True. Ta fonction renvoie "
              + _montre(r) + ". Le test est y == f(x).")
    if appartient(3, 2) is not False:
        _faux("f(3) = 9 ≠ 2 : appartient(3, 2) doit renvoyer False. As-tu échangé x et y ? Le test est y == f(x).")
    if appartient(15, 237) is not True or appartient(15, 225) is not False:
        _faux("f(15) = 237 : appartient(15, 237) doit renvoyer True et appartient(15, 225) doit renvoyer False.")
    if appartient(-1.5, -2.25) is not True:
        _faux("f(-1,5) = 2,25 - 1,5 - 3 = -2,25 : appartient(-1.5, -2.25) doit renvoyer True.")
    return "(2 ; 3) et (15 ; 237) sont sur la courbe, (3 ; 2) et (15 ; 225) n'y sont pas."


def verifier_appartient():
    """Vérifie la fonction appartient."""
    _verifier(_test_appartient, ["appartient"])


def _test_sur_droite(sur_droite):
    r = sur_droite(2, 1, 3, 7)
    _booleen(r, "sur_droite(2, 1, 3, 7)", "Compare y à m * x + p avec ==.")
    if r is False and sur_droite(2, 1, 3, 5) is True:
        _faux("sur_droite(2, 1, 3, 7) renvoie False, alors que 2 × 3 + 1 = 7 : as-tu échangé m et p ? Le test est y == m * x + p.")
    if r is False and sur_droite(2, 1, 7, 3) is True:
        _faux("sur_droite(2, 1, 3, 7) renvoie False, alors que 2 × 3 + 1 = 7 : as-tu échangé x et y ? Le test est y == m * x + p.")
    if r is not True:
        _faux("2 × 3 + 1 = 7 : le point (3 ; 7) est sur la droite y = 2x + 1. sur_droite(2, 1, 3, 7) doit renvoyer True. "
              "Le test est y == m * x + p.")
    if sur_droite(2, 0, 250, 501) is not False or sur_droite(2, 0, 250, 500) is not True:
        _faux("2 × 250 = 500 : sur_droite(2, 0, 250, 500) doit renvoyer True et sur_droite(2, 0, 250, 501) doit renvoyer False.")
    if sur_droite(-3, 4, -2, 10) is not True or sur_droite(0, 5, 100, 5) is not True:
        _faux("(-2 ; 10) est sur la droite y = -3x + 4, et (100 ; 5) sur la droite y = 5 : ta fonction répond autrement.")
    return "(3 ; 7) est sur y = 2x + 1, (250 ; 500) sur y = 2x mais pas (250 ; 501), et les autres cas sont justes."


def verifier_sur_droite():
    """Vérifie la fonction sur_droite."""
    _verifier(_test_sur_droite, ["sur_droite"])


def _test_afficher_antecedents(afficher_antecedents):
    obtenus = _affichage(afficher_antecedents, 3)
    if obtenus == ["3"]:
        _faux("afficher_antecedents(3) affiche seulement 3 : ton test compare x à k. Il faut comparer l'image de x à k : f(x) == k.")
    if obtenus == ["3", "3"]:
        _faux("afficher_antecedents(3) affiche 3 deux fois : tu affiches l'image f(x). Il faut afficher l'antécédent : print(x).")
    if obtenus != ["-3", "2"]:
        _faux("f(-3) = 3 et f(2) = 3 : afficher_antecedents(3) doit afficher -3 puis 2. Ta fonction affiche "
              + (", ".join(obtenus) if obtenus else "rien") + ".")
    obtenus = _affichage(afficher_antecedents, 107)
    if obtenus == []:
        _faux("f(10) = 107, mais afficher_antecedents(107) n'affiche rien : 10 doit être testé. Pour aller de -10 à 10 inclus, "
              "écris range(-10, 11).")
    if obtenus != ["10"]:
        _faux("afficher_antecedents(107) doit afficher 10 (f(-11) = 107 aussi, mais -11 est hors de l'intervalle). "
              "Ta fonction affiche " + ", ".join(obtenus) + ".")
    obtenus = _affichage(afficher_antecedents, 87)
    if obtenus != ["-10", "9"]:
        _faux("f(-10) = 87 et f(9) = 87 : afficher_antecedents(87) doit afficher -10 puis 9. Ta fonction affiche "
              + (", ".join(obtenus) if obtenus else "rien") + ". Commence à -10 : range(-10, 11).")
    if _affichage(afficher_antecedents, 0) != []:
        _faux("aucun entier n'a pour image 0 : afficher_antecedents(0) ne doit rien afficher.")
    return "afficher_antecedents(3) affiche -3 et 2 ; les cas k = 107 (10), 87 (-10 et 9) et 0 (aucun) sont justes aussi."


def verifier_afficher_antecedents():
    """Vérifie la fonction afficher_antecedents."""
    _verifier(_test_afficher_antecedents, ["afficher_antecedents"])


print("Vérifications prêtes. Tu peux commencer.")
