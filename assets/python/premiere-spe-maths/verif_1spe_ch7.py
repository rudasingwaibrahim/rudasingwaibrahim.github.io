"""Vérifications du carnet Python « Première spécialité · Chapitre 7 · Calculer les termes d'une suite ».

Ce fichier accompagne le carnet ch7-generalites-suites.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_1spe_ch7 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_u(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_u', 'verifier_v', 'verifier_liste_v', 'verifier_somme_v', 'verifier_seuil', 'verifier_seuil_carre', 'verifier_fibonacci', 'verifier_syracuse']

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
# Vérifications du carnet (une fonction par cellule « Vérification »).
# Les valeurs attendues sont calculées exactement, avec des fractions.
# ─────────────────────────────────────────────────────────────────────────────
from fractions import Fraction as _F


def _v_exact(n):
    t = _F(2)
    for i in range(n):
        t = _F(1, 2) * t + 3
    return t


def _est_liste(r, appel):
    if not isinstance(r, list):
        _faux(appel + " doit renvoyer une liste, écrite entre crochets [ ]. Ta fonction renvoie " + _montre(r) + ".")


def _test_u(u):
    r = u(0)
    if r == 7:
        _faux("u(0) renvoie 7 : tu as sans doute écrit n ^ 2. En Python, le carré s'écrit n ** 2 "
              "(le symbole ^ est un autre opérateur).")
    if r != 5:
        _faux("u_0 = 0² - 4 × 0 + 5 = 5. Ta fonction renvoie " + _montre(r) + ".")
    r = u(2)
    if r != 1:
        _faux("u_2 = 4 - 8 + 5 = 1. Ta fonction renvoie " + _montre(r) + ".")
    r = u(10)
    if r != 65:
        _faux("u_10 = 100 - 40 + 5 = 65. Ta fonction renvoie " + _montre(r) + ".")
    return "u(0) = 5, u(2) = 1 et u(10) = 65."


def verifier_u():
    """Vérifie la fonction u."""
    _verifier(_test_u, ["u"])


def _test_v(v):
    r = v(0)
    if _proche(r, _v_exact(1)):
        _faux("v(0) renvoie 4 = v_1 : ta boucle tourne une fois de trop. Pour v_n, elle doit tourner "
              "n fois : range(n).")
    if not _proche(r, 2):
        _faux("v(0) doit renvoyer v_0 = 2. Ta fonction renvoie " + _montre(r) + ".")
    r = v(1)
    if _proche(r, 2):
        _faux("v(1) renvoie 2 : ta boucle tourne n - 1 fois. Pour v_n, elle doit tourner n fois : range(n).")
    if not _proche(r, 4):
        _faux("v_1 = 0,5 × 2 + 3 = 4. Ta fonction renvoie " + _montre(r)
              + ". Dans la boucle, on écrit terme = 0.5 * terme + 3.")
    r = v(2)
    if _proche(r, 4):
        _faux("v(2) renvoie 4 = v_1 : ta boucle s'arrête après un seul tour. " + _RETURN)
    if not _proche(r, 5):
        _faux("v_2 = 0,5 × 4 + 3 = 5. Ta fonction renvoie " + _montre(r) + ".")
    for n in range(3, 31):
        r = v(n)
        if not _proche(r, _v_exact(n)):
            _faux("v(" + str(n) + ") devrait valoir " + _nombre(_v_exact(n)) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "v(0) = 2, v(1) = 4, v(2) = 5, et les termes suivants jusqu'à v(30) sont justes."


def verifier_v():
    """Vérifie la fonction v."""
    _verifier(_test_v, ["v"])


def _test_liste_v(liste_v):
    r = liste_v(5)
    _est_liste(r, "liste_v(5)")
    if len(r) == 2:
        _faux("liste_v(5) renvoie " + _montre(r) + " : la boucle s'arrête après un seul tour. " + _RETURN)
    if len(r) != 6:
        _faux("de v_0 à v_5, il y a 6 termes (et non 5). Ta liste en contient " + str(len(r)) + " : " + _montre(r) + ".")
    if not _proche(r[0], 2):
        _faux("le premier élément de la liste doit être v_0 = 2. Ta liste commence par " + _montre(r[0]) + ".")
    for n in range(6):
        if not _proche(r[n], _v_exact(n)):
            _faux("l'élément d'indice " + str(n) + " doit être v_" + str(n) + " = " + _nombre(_v_exact(n))
                  + ". Ta liste contient " + _montre(r[n]) + ". Ta liste complète : " + _montre(r) + ".")
    r5 = r
    r = liste_v(0)
    if not isinstance(r, list) or len(r) != 1:
        _faux("liste_v(0) doit renvoyer [2] : un seul terme, v_0. Ta fonction renvoie " + _montre(r) + ".")
    return "liste_v(5) renvoie " + _montre(r5) + " et liste_v(0) renvoie [2]."


def verifier_liste_v():
    """Vérifie la fonction liste_v."""
    _verifier(_test_liste_v, ["liste_v"])


def _test_somme_v(somme_v):
    r = somme_v(2)
    if _proche(r, 5):
        _faux("somme_v(2) renvoie 5 = v_2 : ta fonction garde seulement le dernier terme. "
              "Il faut ajouter chaque terme à S : S = S + terme.")
    if _proche(r, 2):
        _faux("somme_v(2) renvoie 2 = v_0 : la boucle s'arrête après un seul tour. " + _RETURN)
    if not _proche(r, 11):
        _faux("v_0 + v_1 + v_2 = 2 + 4 + 5 = 11. Ta fonction renvoie " + _montre(r) + ".")
    attendu = 0
    for k in range(11):
        attendu = attendu + _v_exact(k)
    r = somme_v(10)
    if not _proche(r, attendu):
        _faux("somme_v(10) devrait valoir " + _nombre(attendu) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "somme_v(2) = 11 et somme_v(10) ≈ " + _nombre(attendu) + "."


def verifier_somme_v():
    """Vérifie la fonction somme_v."""
    _verifier(_test_somme_v, ["somme_v"])


def _seuil_exact(e):
    n, t = 0, _F(2)
    while 6 - t >= _F(e):
        n, t = n + 1, _F(1, 2) * t + 3
    return n


def _test_seuil(seuil):
    r = seuil(1)
    if r == 0:
        _faux("seuil(1) renvoie 0 : la boucle ne tourne jamais. Vérifie la condition du while : "
              "on continue tant que 6 - terme >= e.")
    if r == 1:
        _faux("seuil(1) renvoie 1 : la boucle s'arrête après un seul tour (ou n ne fait que recevoir 1). "
              "Le return doit être aligné avec while, et n augmente de 1 à chaque tour : n = n + 1.")
    if r != 3:
        _faux("6 - v_2 = 1 n'est pas strictement inférieur à 1, mais 6 - v_3 = 0,5 l'est : seuil(1) doit renvoyer 3. "
              "Ta fonction renvoie " + _montre(r) + ". Vérifie que n augmente de 1 à chaque tour : n = n + 1.")
    for e in [0.5, 0.1, 0.01, 0.001, 0.0001]:
        r = seuil(e)
        if r != _seuil_exact(e):
            _faux("seuil(" + str(e) + ") doit renvoyer " + str(_seuil_exact(e)) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "seuil(1) = 3, et les seuils pour e = 0,5 ; 0,1 ; 0,01 ; 0,001 ; 0,0001 sont justes."


def verifier_seuil():
    """Vérifie la fonction seuil."""
    _verifier(_test_seuil, ["seuil"],
              aide={"boucle": "Dans la boucle, terme doit passer au terme suivant (terme = 0.5 * terme + 3) "
                              "et la condition du while doit utiliser e : 6 - terme >= e."})


def _test_seuil_carre(seuil_carre):
    r = seuil_carre(1000)
    if r == 1001:
        _faux("seuil_carre(1000) renvoie 1001 : ta condition compare n à A. Il faut comparer n² à A : n ** 2 <= A.")
    if r == 1:
        _faux("seuil_carre(1000) renvoie 1 : la boucle s'arrête après un seul tour. " + _RETURN)
    if r == 501:
        _faux("seuil_carre(1000) renvoie 501 : tu as écrit n * 2, qui est le double de n. Le carré s'écrit n ** 2.")
    if r != 32:
        _faux("31² = 961 ≤ 1000 et 32² = 1024 > 1000 : seuil_carre(1000) doit renvoyer 32. "
              "Ta fonction renvoie " + _montre(r) + ".")
    r = seuil_carre(10 ** 6)
    if r == 1000:
        _faux("1000² = 1 000 000 n'est pas strictement supérieur à 10⁶. On continue tant que n² ≤ A : "
              "la condition est n ** 2 <= A (et non n ** 2 < A).")
    if r != 1001:
        _faux("seuil_carre(10 ** 6) doit renvoyer 1001. Ta fonction renvoie " + _montre(r) + ".")
    if seuil_carre(0) != 1:
        _faux("0² = 0 n'est pas strictement supérieur à 0, mais 1² = 1 l'est : seuil_carre(0) doit renvoyer 1.")
    return "seuil_carre(1000) = 32, seuil_carre(10 ** 6) = 1001 et seuil_carre(0) = 1."


def verifier_seuil_carre():
    """Vérifie la fonction seuil_carre."""
    _verifier(_test_seuil_carre, ["seuil_carre"],
              aide={"boucle": "La condition du while doit porter sur n ** 2, et n augmente de 1 à chaque tour."})


_FIBO = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def _test_fibonacci(liste_fibonacci):
    r = liste_fibonacci(10)
    _est_liste(r, "liste_fibonacci(10)")
    if len(r) == 3:
        _faux("liste_fibonacci(10) renvoie " + _montre(r) + " : la boucle s'arrête après un seul tour. " + _RETURN)
    if len(r) != 11:
        _faux("de F_0 à F_10, il y a 11 termes. Ta liste en contient " + str(len(r)) + " : " + _montre(r) + ".")
    if r[0:3] != [0, 1, 1]:
        _faux("la liste doit commencer par 0, 1, 1 (F_2 = F_1 + F_0 = 1). Ta liste : " + _montre(r) + ".")
    if r != _FIBO:
        _faux("chaque terme est la somme des deux précédents : on attend " + _montre(_FIBO)
              + ". Ta liste : " + _montre(r) + ".")
    r = liste_fibonacci(30)
    if r[len(r) - 1] != 832040:
        _faux("F_30 doit valoir 832040. Le dernier terme de liste_fibonacci(30) vaut " + _montre(r[len(r) - 1]) + ".")
    return "liste_fibonacci(10) renvoie " + _montre(_FIBO) + " et F_30 = 832040."


def verifier_fibonacci():
    """Vérifie la fonction liste_fibonacci."""
    _verifier(_test_fibonacci, ["liste_fibonacci"],
              aide={"indice": "Tu demandes un élément qui n'existe pas encore. Au moment de calculer F_i, "
                              "les deux derniers éléments de la liste sont termes[i - 1] et termes[i - 2]."})


def _test_syracuse(syracuse):
    r = syracuse(6)
    _est_liste(r, "syracuse(6)")
    if r == [6, 3]:
        _faux("syracuse(6) renvoie [6, 3] : la boucle s'arrête après un seul tour. " + _RETURN)
    if r != [6, 3, 10, 5, 16, 8, 4, 2, 1]:
        _faux("pour c = 6, on attend [6, 3, 10, 5, 16, 8, 4, 2, 1]. Ta fonction renvoie " + _montre(r) + ".")
    for x in r:
        if isinstance(x, float):
            _faux("ta liste contient des nombres décimaux comme 3.0 : terme / 2 donne un décimal. "
                  "Utilise terme // 2 pour garder des entiers. Ta liste : " + _montre(r) + ".")
    if syracuse(1) != [1]:
        _faux("pour c = 1, la liste est [1] : on s'arrête tout de suite.")
    if len(syracuse(7)) != 17:
        _faux("pour c = 7, la liste contient 17 termes : 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1.")
    return "syracuse(6) renvoie [6, 3, 10, 5, 16, 8, 4, 2, 1] ; les cas c = 1 et c = 7 sont justes aussi."


def verifier_syracuse():
    """Vérifie la fonction syracuse."""
    _verifier(_test_syracuse, ["syracuse"],
              aide={"boucle": "Vérifie les deux calculs : un terme pair est divisé par 2 (terme // 2), "
                              "un terme impair devient 3 * terme + 1."})


print("Vérifications prêtes. Tu peux commencer.")
