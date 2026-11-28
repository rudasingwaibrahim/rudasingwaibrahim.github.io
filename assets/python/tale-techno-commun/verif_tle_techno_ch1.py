"""Vérifications du carnet Python « Terminale technologique · Chapitre 1 · Sommes de termes et symbole Σ ».

Ce fichier accompagne le carnet ch1-sommes-suites.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tle_techno_ch1 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_somme_carres(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_somme_carres', 'verifier_vocabulaire', 'verifier_somme_cubes', 'verifier_somme_inverses', 'verifier_capital', 'verifier_capital_formule', 'verifier_nombre_versements']

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


def _test_somme_carres(somme_carres):
    r = somme_carres(3)
    if r == 5:
        _faux("somme_carres(3) renvoie 5 = 1² + 2² : le dernier terme 3² manque. "
              "Le compteur doit aller jusqu'à n inclus : range(1, n + 1).")
    if r == 9:
        _faux("somme_carres(3) renvoie 9 = 3² : ta fonction garde seulement le dernier terme. "
              "L'accumulateur s'écrit S = S + k ** 2.")
    if r in (4, 8):
        _faux("somme_carres(3) renvoie " + str(r) + " : tu as sans doute écrit k ^ 2. En Python, le carré s'écrit "
              "k ** 2 (le symbole ^ est un autre opérateur).")
    if r == 6 or r == 12:
        _faux("somme_carres(3) renvoie " + str(r) + " : tu as écrit k * 2 (le double de k). Le carré s'écrit k ** 2.")
    if r == 1:
        _faux("somme_carres(3) renvoie 1 = 1² : la boucle s'arrête après un seul tour. " + _RETURN)
    if r != 14:
        _faux("1² + 2² + 3² = 1 + 4 + 9 = 14. Ta fonction renvoie " + _montre(r) + ".")
    if somme_carres(1) != 1:
        _faux("somme_carres(1) doit renvoyer 1² = 1. Ta fonction renvoie " + _montre(somme_carres(1)) + ".")
    r = somme_carres(10)
    if r != 385:
        _faux("la somme des 10 premiers carrés vaut 385. Ta fonction renvoie " + _montre(r) + ".")
    return "somme_carres(3) = 14, somme_carres(1) = 1 et somme_carres(10) = 385."


def verifier_somme_carres():
    """Vérifie la fonction somme_carres."""
    _verifier(_test_somme_carres, ["somme_carres"])


def _test_vocabulaire(accumulateur, compteur, valeur_initiale_S, dernier_k):
    if accumulateur != "S":
        if accumulateur == "k":
            _faux("tu as échangé les rôles. L'accumulateur est la variable dans laquelle on ajoute les termes "
                  "un à un : c'est S.")
        _faux("l'accumulateur est la variable dans laquelle on ajoute les termes un à un : c'est \"S\" "
              "(écrit entre guillemets, en majuscule). Tu as répondu " + _montre(accumulateur) + ".")
    if compteur != "k":
        _faux("le compteur est la variable qui parcourt les indices 1, 2, ..., n : c'est \"k\" "
              "(écrit entre guillemets). Tu as répondu " + _montre(compteur) + ".")
    if valeur_initiale_S != 0:
        _faux("avant d'ajouter le premier terme, la somme vaut 0 : S = 0. Tu as répondu " + _montre(valeur_initiale_S) + ".")
    if dernier_k == 11:
        _faux("range(1, 11) s'arrête juste avant 11 : au dernier tour, k vaut 10, comme l'indice "
              "du haut du symbole Σ.")
    if dernier_k != 10:
        _faux("pour somme_carres(10), le compteur va de 1 à 10 : au dernier tour, k vaut 10. "
              "Tu as répondu " + _montre(dernier_k) + ".")
    return "S est l'accumulateur, k le compteur ; S vaut 0 au départ et k vaut 10 au dernier tour de somme_carres(10)."


def verifier_vocabulaire():
    """Vérifie les quatre réponses sur le vocabulaire de l'algorithme."""
    _verifier(_test_vocabulaire, ["accumulateur", "compteur", "valeur_initiale_S", "dernier_k"])


def _test_somme_cubes(somme_cubes):
    r = somme_cubes(4)
    if r == 36:
        _faux("somme_cubes(4) renvoie 36 = 1³ + 2³ + 3³ : le dernier terme 4³ manque. Utilise range(1, n + 1).")
    if r == 30:
        _faux("somme_cubes(4) renvoie 30 : tu as écrit k * 3 (le triple de k). Le cube s'écrit k ** 3.")
    if r == 64:
        _faux("somme_cubes(4) renvoie 64 = 4³ : ta fonction garde seulement le dernier terme. "
              "L'accumulateur s'écrit S = S + k ** 3.")
    if r == 10:
        _faux("somme_cubes(4) renvoie 10 : tu as sans doute écrit k ^ 3. En Python, le cube s'écrit k ** 3 "
              "(le symbole ^ est un autre opérateur).")
    if r == 1:
        _faux("somme_cubes(4) renvoie 1 = 1³ : la boucle s'arrête après un seul tour. " + _RETURN)
    if r != 100:
        _faux("1³ + 2³ + 3³ + 4³ = 1 + 8 + 27 + 64 = 100. Ta fonction renvoie " + _montre(r) + ".")
    r = somme_cubes(10)
    if r != 3025:
        _faux("la somme des 10 premiers cubes vaut 3025. Ta fonction renvoie " + _montre(r) + ".")
    return "somme_cubes(4) = 100 et somme_cubes(10) = 3025."


def verifier_somme_cubes():
    """Vérifie la fonction somme_cubes."""
    _verifier(_test_somme_cubes, ["somme_cubes"])


def _inverses_exact(n):
    s = _F(0)
    for k in range(1, n + 1):
        s = s + _F(1, k)
    return s


def _test_somme_inverses(somme_inverses):
    r = somme_inverses(4)
    if _proche(r, 1):
        _faux("somme_inverses(4) renvoie 1. Deux causes possibles : tu ajoutes 1 / n à chaque tour (le terme dépend "
              "du compteur : 1 / k), " + _RETURN_OU)
    if _proche(r, 0.25):
        _faux("somme_inverses(4) renvoie 0,25 = 1/4 : ta fonction garde seulement le dernier terme. "
              "L'accumulateur s'écrit S = S + 1 / k.")
    if _proche(r, _inverses_exact(3)):
        _faux("somme_inverses(4) renvoie 1 + 1/2 + 1/3 : le dernier terme 1/4 manque. Utilise range(1, n + 1).")
    if not _proche(r, _F(25, 12)):
        _faux("1 + 1/2 + 1/3 + 1/4 = 25/12 ≈ 2.083333. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(somme_inverses(1), 1):
        _faux("somme_inverses(1) doit renvoyer 1. Ta fonction renvoie " + _montre(somme_inverses(1)) + ".")
    exact = _inverses_exact(100)
    r = somme_inverses(100)
    if not _proche(r, exact):
        _faux("somme_inverses(100) devrait valoir environ " + str(round(float(exact), 6))
              + ". Ta fonction renvoie " + _montre(r) + ".")
    return "somme_inverses(4) ≈ 2.083333 (c'est 25/12), somme_inverses(1) = 1 et somme_inverses(100) ≈ " \
        + str(round(float(exact), 6)) + "."


def verifier_somme_inverses():
    """Vérifie la fonction somme_inverses."""
    _verifier(_test_somme_inverses, ["somme_inverses"],
              aide={"division": "Au premier tour, k vaut 0 et 1 / 0 n'existe pas. La somme commence à k = 1 : "
                                "range(1, n + 1)."})


def _V_exact(n):
    V = _F(500)
    for annee in range(2, n + 1):
        V = _F(103, 100) * V + 500
    return V


def _euros(x):
    return str(round(float(x), 2)).replace(".", ",") + " €"


def _test_capital(capital):
    r1 = capital(1)
    if not _proche(r1, 500):
        _faux("juste après le 1er versement, le capital est 500 €. Ta fonction renvoie " + _montre(r1) + ".")
    r2, r3 = capital(2), capital(3)
    if _proche(r2, 515) and _proche(r3, 515.45):
        _faux("tu multiplies par 0,03 : c'est le montant des intérêts. Pour ajouter 3 %, on multiplie par "
              "1 + 3/100 = 1,03.")
    if _proche(r2, 515) and _proche(r3, 530.45):
        _faux("tu oublies le nouveau versement : chaque année, V devient 1,03 × V + 500.")
    if _proche(r2, 1030):
        _faux("tu ajoutes le versement avant de calculer les intérêts : le nouveau versement ne rapporte rien "
              "la première année. V devient 1,03 × V + 500.")
    if not _proche(r2, 1015):
        _faux("V_2 = 1,03 × 500 + 500 = 1015. Ta fonction renvoie " + _montre(r2) + ".")
    if _proche(r3, 1015):
        _faux("capital(3) renvoie 1015, comme capital(2) : la boucle s'arrête après un seul tour. " + _RETURN)
    if not _proche(r3, 1545.45):
        _faux("V_3 = 1,03 × 1015 + 500 = 1545,45. Ta fonction renvoie " + _montre(r3) + ".")
    for n in range(4, 31):
        r = capital(n)
        if not _proche(r, _V_exact(n)):
            _faux("capital(" + str(n) + ") devrait valoir environ " + _euros(_V_exact(n))
                  + ". Ta fonction renvoie " + _montre(r) + ".")
    return "V_1 = 500 €, V_2 = 1015 €, V_3 = 1545,45 €, et les capitaux suivants jusqu'à V_30 sont justes."


def verifier_capital():
    """Vérifie la fonction capital."""
    _verifier(_test_capital, ["capital"])


def _test_capital_formule(capital_formule):
    r = capital_formule(1)
    if _proche(r, 0):
        _faux("capital_formule(1) renvoie 0 : il y a n termes, de 1,03⁰ à 1,03ⁿ⁻¹, donc l'exposant dans la "
              "formule est n.")
    if not _proche(r, 500):
        _faux("capital_formule(1) doit renvoyer 500. Ta fonction renvoie " + _montre(r)
              + ". Vérifie les parenthèses : 500 * (1.03 ** n - 1) / (1.03 - 1).")
    for n in range(1, 31):
        r = capital_formule(n)
        if not _proche(r, _V_exact(n)):
            _faux("pour n = " + str(n) + ", la formule devrait donner environ " + _euros(_V_exact(n))
                  + ". Ta fonction renvoie " + _montre(r) + ". Vérifie les parenthèses : "
                  "500 * (1.03 ** n - 1) / (1.03 - 1).")
    return "la formule donne le même capital que la boucle pour n = 1, 2, ..., 30."


def verifier_capital_formule():
    """Vérifie la fonction capital_formule."""
    _verifier(_test_capital_formule, ["capital_formule"],
              aide={"division": "Le dénominateur de la formule est 1,03 - 1 = 0,03 : écris (1.03 - 1), "
                                "avec des parenthèses."})


def _test_nombre_versements(nombre_versements, capital):
    if not (_proche(capital(15), _V_exact(15)) and _proche(capital(16), _V_exact(16))):
        _faux("vérifie d'abord ta fonction capital (cellule verifier_capital()) : le tableau doit montrer un "
              "capital inférieur à 10 000 € après 15 versements et supérieur après 16.")
    r = nombre_versements
    if r == 20:
        _faux("au bout de 20 versements, on a versé 10 000 € : ce n'est pas la question. On cherche quand le "
              "capital dépasse 10 000 € pour la première fois.")
    if r == 15:
        _faux("après 15 versements, le capital vaut environ 9 299 € : il ne dépasse pas encore 10 000 €.")
    if r == 17:
        _faux("après 16 versements, le capital dépasse déjà 10 000 € : 17 n'est pas la première fois.")
    if r != 16:
        _faux("relis le tableau : on cherche le premier n pour lequel le capital dépasse 10 000 €. "
              "Tu as répondu " + _montre(r) + ".")
    return "après 15 versements, le capital vaut environ 9 299 € ; il dépasse 10 000 € pour la première fois " \
           "après 16 versements (environ 10 078 €)."


def verifier_nombre_versements():
    """Vérifie la réponse nombre_versements."""
    _verifier(_test_nombre_versements, ["nombre_versements", "capital"])


print("Vérifications prêtes. Tu peux commencer.")
