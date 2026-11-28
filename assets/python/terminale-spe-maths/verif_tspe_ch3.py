"""Vérifications du carnet Python « Terminale spécialité · Chapitre 3 · Triangle de Pascal, parties et permutations ».

Ce fichier accompagne le carnet ch3-pascal-parties-permutations.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch3 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_factorielle(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_factorielle', 'verifier_triangle_pascal', 'verifier_parties2', 'verifier_triplets_distincts', 'verifier_permutation_aleatoire']

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
def _test_factorielle(factorielle):
    r = factorielle(5)
    if r == 0:
        _faux("factorielle(5) renvoie 0 : ta boucle commence à k = 0, et un produit qui contient 0 est nul. Écris range(1, n + 1).")
    if r == 24:
        _faux("factorielle(5) renvoie 24 = 4! : le facteur 5 manque. Écris range(1, n + 1).")
    if r != 120:
        _faux("5! = 1 × 2 × 3 × 4 × 5 = 120. Ta fonction renvoie " + _montre(r) + ".")
    if factorielle(0) != 1 or factorielle(1) != 1 or factorielle(10) != 3628800:
        _faux("0! = 1, 1! = 1 et 10! = 3 628 800 : ta fonction répond autrement.")
    return "5! = 120, 10! = 3 628 800, 0! = 1 et 1! = 1."


def verifier_factorielle():
    """Vérifie la fonction factorielle."""
    _verifier(_test_factorielle, ["factorielle"])


def _pascal(N):
    L = [[1]]
    for n in range(1, N + 1):
        ligne = [1]
        for k in range(1, n):
            ligne.append(L[n - 1][k - 1] + L[n - 1][k])
        ligne.append(1)
        L.append(ligne)
    return L


def _test_triangle_pascal(triangle_pascal):
    r = triangle_pascal(4)
    _est_liste(r, "triangle_pascal(4)")
    if len(r) != 5:
        _faux("triangle_pascal(4) doit renvoyer 5 lignes (de la ligne 0 à la ligne 4). Ta fonction en renvoie " + str(len(r)) + ".")
    if r[1] == [1]:
        _faux("la ligne 1 de ton triangle est [1] : il manque le dernier coefficient. Après la boucle sur k, ajoute 1 : "
              "ligne.append(1).")
    if r[2] == [1, 1, 1]:
        _faux("la ligne 2 de ton triangle est [1, 1, 1] : chaque coefficient intérieur est la somme des deux coefficients "
              "au-dessus : L[n - 1][k - 1] + L[n - 1][k].")
    if r != _pascal(4):
        _faux("triangle_pascal(4) doit renvoyer " + _montre(_pascal(4)) + ". Ta fonction renvoie " + _montre(r) + ".")
    r = triangle_pascal(10)
    if r != _pascal(10):
        _faux("la ligne 10 doit être " + _montre(_pascal(10)[10]) + ".")
    return "triangle_pascal(4) = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]] ; la ligne 10 est juste aussi (C(10, 5) = 252)."


def verifier_triangle_pascal():
    """Vérifie la fonction triangle_pascal."""
    _verifier(_test_triangle_pascal, ["triangle_pascal"],
              aide={"indice": "La ligne n - 1 doit contenir n coefficients, d'indices 0 à n - 1 : n'oublie pas le dernier "
                              "coefficient 1 de chaque ligne (ligne.append(1)), et utilise L[n - 1][k - 1] + L[n - 1][k]."})


_E = ["a", "b", "c", "d", "e"]


def _paires(E):
    return [[E[i], E[j]] for i in range(len(E)) for j in range(i + 1, len(E))]


def _test_parties2(parties2):
    r = parties2(_E)
    _est_liste(r, "parties2(E)")
    if len(r) == 25:
        _faux("parties2 renvoie 25 éléments pour un ensemble à 5 éléments : tu comptes aussi [a, a] et chaque partie deux fois "
              "([a, b] et [b, a]). Impose i < j : range(i + 1, n).")
    if len(r) == 15:
        _faux("parties2 renvoie 15 éléments : tu comptes aussi les « parties » [a, a], qui n'ont qu'un élément. "
              "Impose i < j : range(i + 1, n).")
    if len(r) != 10:
        _faux("un ensemble à 5 éléments a C(5, 2) = 10 parties à 2 éléments. Ta fonction en renvoie " + str(len(r)) + ".")
    if r != _paires(_E):
        _faux("parties2(E) doit renvoyer " + _montre(_paires(_E)) + ". Ta fonction renvoie " + _montre(r) + ".")
    if parties2([1, 2]) != [[1, 2]] or parties2([7]) != []:
        _faux("parties2([1, 2]) doit renvoyer [[1, 2]] et parties2([7]) doit renvoyer [].")
    return "parties2 renvoie les 10 parties à 2 éléments de {a, b, c, d, e} : C(5, 2) = 10."


def verifier_parties2():
    """Vérifie la fonction parties2."""
    _verifier(_test_parties2, ["parties2"])


def _test_triplets_distincts(triplets_distincts):
    r = triplets_distincts(["a", "b", "c", "d"])
    _est_liste(r, "triplets_distincts")
    if len(r) == 36:
        _faux("pour 4 éléments, ta fonction renvoie 36 triplets : elle accepte des triplets comme [a, b, a]. "
              "Les trois éléments doivent être deux à deux distincts : a != b and a != c and b != c.")
    if len(r) > 36:
        _faux("pour 4 éléments, ta fonction renvoie " + str(len(r)) + " triplets : avec or, il suffit que deux éléments diffèrent. "
              "Il faut que les trois conditions soient vraies : and.")
    if len(r) != 24:
        _faux("pour 4 éléments, il y a 4 × 3 × 2 = 24 triplets d'éléments distincts. Ta fonction en renvoie " + str(len(r)) + ".")
    for t in r:
        if not isinstance(t, list) or len(t) != 3 or t[0] == t[1] or t[0] == t[2] or t[1] == t[2]:
            _faux("chaque triplet doit être une liste de trois éléments distincts. Ta fonction renvoie " + _montre(t) + ".")
    if len(triplets_distincts([1, 2, 3])) != 6:
        _faux("pour 3 éléments, on doit obtenir les 3! = 6 permutations.")
    return "24 triplets d'éléments distincts pour 4 éléments (4 × 3 × 2) et 3! = 6 permutations de [1, 2, 3]."


def verifier_triplets_distincts():
    """Vérifie la fonction triplets_distincts."""
    _verifier(_test_triplets_distincts, ["triplets_distincts"])


def _test_permutation_aleatoire(permutation_aleatoire):
    L = [1, 2, 3]
    with _Graine(3):
        r = permutation_aleatoire(L)
    if L != [1, 2, 3]:
        _faux("après l'appel, la liste de départ est devenue " + _montre(L) + " : ta fonction l'a vidée. Travaille sur une copie : "
              "crée reste = [] puis ajoute-lui chaque élément de L.")
    _est_liste(r, "permutation_aleatoire([1, 2, 3])")
    if len(r) != 3 or sorted(r) != [1, 2, 3]:
        _faux("permutation_aleatoire([1, 2, 3]) doit renvoyer les trois éléments 1, 2, 3, chacun une fois. Ta fonction renvoie "
              + _montre(r) + ".")
    vus = {}
    with _Graine(33):
        for k in range(1200):
            p = permutation_aleatoire([1, 2, 3])
            if sorted(p) != [1, 2, 3]:
                _faux("ta fonction renvoie " + _montre(p) + ", qui n'est pas une permutation de [1, 2, 3].")
            vus[str(p)] = vus.get(str(p), 0) + 1
    if len(vus) != 6:
        _faux("sur 1200 tirages, ta fonction ne donne que " + str(len(vus)) + " permutations différentes sur les 6 possibles.")
    for cle in vus:
        if abs(vus[cle] / 1200 - 1 / 6) > 0.05:
            _faux("sur 1200 tirages, la permutation " + cle + " sort avec la fréquence " + _ecrire(vus[cle] / 1200, 3)
                  + ", trop loin de 1/6 : chaque élément restant doit avoir la même chance d'être tiré.")
    return "sur 1200 tirages, les 6 permutations de [1, 2, 3] sortent chacune avec une fréquence proche de 1/6 ; la liste de départ n'est pas modifiée."


def verifier_permutation_aleatoire():
    """Vérifie la fonction permutation_aleatoire."""
    _verifier(_test_permutation_aleatoire, ["permutation_aleatoire"],
              aide={"indice": "Les indices de reste vont de 0 à len(reste) - 1 : randint(0, len(reste) - 1).",
                    "boucle": "Ta boucle ne s'arrête pas : la liste reste ne diminue jamais. Retire l'élément tiré avec "
                              "reste.pop(i)."})


print("Vérifications prêtes. Tu peux commencer.")
