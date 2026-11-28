"""Vérifications du carnet Python « Seconde · Chapitre 4 · Multiples, diviseurs et parité ».

Ce fichier accompagne le carnet ch4-multiples-diviseurs.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch4 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_est_multiple(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_est_multiple', 'verifier_nombre_multiples', 'verifier_plus_grand_multiple', 'verifier_plus_grand_multiple_2', 'verifier_nombre_diviseurs', 'verifier_afficher_diviseurs', 'verifier_est_pair', 'verifier_cagettes']

# ─────────────────────────────────────────────────────────────────────────────
# Mécanique commune des vérifications (elle ne concerne pas l'élève).
# Tout ce qui commence par _ reste invisible après « from ... import * ».
# ─────────────────────────────────────────────────────────────────────────────
import sys as _sys
import io as _io
import re as _re
import contextlib as _contextlib

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
            return
        obj = g[nom]
        if obj is Ellipsis:
            print("✘ Pas encore : « " + nom + " » vaut encore ... .")
            print("  → Remplace les ... par ta réponse, exécute la cellule, puis relance cette vérification.")
            return
        code = getattr(obj, "__code__", None)
        if code is not None and _contient_points(code):
            print("✘ Pas encore : il reste des ... à remplacer dans ta fonction " + nom + ".")
            print("  → Remplace chaque ... par ton code, exécute la cellule de ta fonction,"
                  " puis relance cette vérification.")
            return
        objets.append(obj)
    try:
        bilan = _executer(test, objets, g)
    except _PasEncore as e:
        print("✘ Pas encore : " + str(e))
        return
    except _TropLong:
        print("✘ Pas encore : ta fonction ne s'arrête pas (sa boucle a fait des centaines de milliers de tours).")
        print("  → " + aide.get("boucle", "Vérifie ta boucle while : la variable testée doit changer à chaque "
                                          "tour, pour que la condition finisse par devenir fausse."))
        return
    except NameError as e:
        nom = _nom_inconnu(e)
        print("✘ Pas encore : ta fonction utilise le nom « " + nom + " », que Python ne connaît pas.")
        print("  → Vérifie son orthographe (Python distingue majuscules et minuscules). "
              "Si c'est une fonction écrite plus haut dans le carnet, exécute d'abord sa cellule.")
        return
    except ZeroDivisionError:
        print("✘ Pas encore : ta fonction divise par 0, ce qui est impossible.")
        print("  → " + aide.get("division", "Repère la division (/, // ou %) dont le diviseur vaut 0."))
        return
    except IndexError:
        print("✘ Pas encore : ta fonction demande un élément de la liste qui n'existe pas (indice trop grand).")
        print("  → " + aide.get("indice", "Les indices d'une liste de longueur n vont de 0 à n - 1."))
        return
    except RecursionError:
        print("✘ Pas encore : ta fonction s'appelle elle-même sans jamais s'arrêter.")
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
        return
    except Exception:
        print("✘ Pas encore : ta fonction s'arrête sur une erreur.")
        print("  → Appelle ta fonction toute seule dans une nouvelle cellule (par exemple avec un petit nombre)"
              " pour voir le message de Python, puis relis ton code ligne par ligne.")
        return
    print("✔ Juste : " + bilan)


# ─────────────────────────────────────────────────────────────────────────────
# Vérifications du carnet (une fonction par cellule « Vérification »).
# ─────────────────────────────────────────────────────────────────────────────

def _booleen(r, appel, conseil):
    """Refuse un nombre ou autre chose qu'un booléen."""
    if r is True or r is False:
        return
    if _est_nombre(r):
        _faux(appel + " renvoie le nombre " + _montre(r) + " : la fonction doit renvoyer True ou False. "
              + conseil)
    _faux(appel + " doit renvoyer True ou False. Ta fonction renvoie " + _montre(r) + ".")


def _test_est_multiple(est_multiple):
    r = est_multiple(12, 3)
    _booleen(r, "est_multiple(12, 3)", "Compare le reste à 0 avec == : a % b == 0.")
    if r is False and est_multiple(3, 12) is True and est_multiple(5, 12) is True:
        _faux("est_multiple(3, 12) et est_multiple(5, 12) renvoient True : tu as sans doute utilisé le quotient a // b. "
              "C'est le reste a % b qu'il faut comparer à 0.")
    if r is False and est_multiple(3, 12) is True:
        _faux("tu as inversé a et b. On veut savoir si a est un multiple de b, donc on calcule le reste a % b.")
    if r is not True:
        _faux("12 = 4 × 3, donc est_multiple(12, 3) doit renvoyer True. Ta fonction renvoie " + _montre(r) + ".")
    r = est_multiple(14, 3)
    if r is not False:
        _faux("14 = 4 × 3 + 2 : le reste n'est pas nul, donc est_multiple(14, 3) doit renvoyer False. "
              "Ta fonction renvoie " + _montre(r) + ".")
    if est_multiple(3, 12) is not False:
        _faux("3 est un diviseur de 12, mais pas un multiple de 12 : est_multiple(3, 12) doit renvoyer False.")
    if est_multiple(0, 7) is not True:
        _faux("0 = 0 × 7 : 0 est un multiple de tout entier, donc est_multiple(0, 7) doit renvoyer True.")
    if est_multiple(1001, 7) is not True:
        _faux("1001 = 143 × 7 : est_multiple(1001, 7) doit renvoyer True.")
    return "est_multiple(12, 3) renvoie True, est_multiple(14, 3) renvoie False ; les cas (3, 12), (0, 7) et (1001, 7) sont justes aussi."


def verifier_est_multiple():
    """Vérifie la fonction est_multiple."""
    _verifier(_test_est_multiple, ["est_multiple"])


def _test_nombre_multiples(nombre_multiples):
    r = nombre_multiples(5, 100)
    if r == 1050:
        _faux("ta fonction additionne les multiples (5 + 10 + ... + 100 = 1050). "
              "Un compteur augmente de 1 : compteur = compteur + 1.")
    if r == 100:
        _faux("ta fonction compte tous les nombres de 1 à 100 : la condition après if est toujours vraie. "
              "Le test est est_multiple(a, b), ou a % b == 0.")
    if r == 2:
        _faux("ta fonction renvoie 2 : elle compte les diviseurs de 5 (1 et 5). Tu as inversé : "
              "on cherche les nombres a qui sont des multiples de b, donc le test est est_multiple(a, b).")
    if r == 1:
        _faux("ta fonction renvoie 1 : le compteur doit augmenter de 1 à chaque multiple trouvé, "
              "compteur = compteur + 1 (et non compteur = 1).")
    if r == 0:
        _faux("ta fonction renvoie 0 : le compteur n'augmente jamais. Vérifie le test après if "
              "et la ligne compteur = compteur + 1. " + _RETURN)
    if r != 20:
        _faux("entre 1 et 100, les multiples de 5 sont 5, 10, ..., 100 : il y en a 20. "
              "Ta fonction renvoie " + _montre(r) + ".")
    r = nombre_multiples(7, 500)
    if r != 71:
        _faux("entre 1 et 500, il y a 71 multiples de 7 (le dernier est 497 = 71 × 7). "
              "Ta fonction renvoie " + _montre(r) + ". Vérifie que la boucle va jusqu'à n inclus : range(1, n + 1).")
    r = nombre_multiples(12, 11)
    if r != 0:
        _faux("aucun multiple de 12 n'est compris entre 1 et 11 : la réponse est 0. Ta fonction renvoie " + _montre(r) + ".")
    return "20 multiples de 5 entre 1 et 100, 71 multiples de 7 entre 1 et 500, aucun multiple de 12 entre 1 et 11."


def verifier_nombre_multiples():
    """Vérifie la fonction nombre_multiples."""
    _verifier(_test_nombre_multiples, ["nombre_multiples"])


def _test_plus_grand_multiple(plus_grand_multiple):
    if plus_grand_multiple(5, 35) == 31 and plus_grand_multiple(7, 30) == 24:
        _faux("ta boucle avance de 1 en 1 : elle doit avancer de a en a, avec m = m + a.")
    r = plus_grand_multiple(3, 20)
    if r == 3:
        _faux("plus_grand_multiple(3, 20) renvoie 3 : la boucle s'arrête après un seul tour. " + _RETURN)
    if r != 18:
        _faux("les multiples de 3 sont 0, 3, 6, ..., 18, 21... Le plus grand qui ne dépasse pas 20 est 18. "
              "Ta fonction renvoie " + _montre(r) + ".")
    r = plus_grand_multiple(5, 35)
    if r != 35:
        _faux("35 = 7 × 5 est lui-même un multiple de 5, et 35 ≤ 35 : la réponse est 35. "
              "Ta fonction renvoie " + _montre(r) + ".")
    r = plus_grand_multiple(7, 3)
    if r != 0:
        _faux("ici b = 3 est plus petit que a = 7 : le seul multiple de 7 compris entre 0 et 3 est 0. "
              "Ta fonction renvoie " + _montre(r) + ".")
    return "plus_grand_multiple(3, 20) = 18, plus_grand_multiple(5, 35) = 35 et plus_grand_multiple(7, 3) = 0."


def verifier_plus_grand_multiple():
    """Vérifie la fonction plus_grand_multiple."""
    _verifier(_test_plus_grand_multiple, ["plus_grand_multiple"],
              aide={"boucle": "Dans la boucle, m doit augmenter de a à chaque tour : m = m + a."})


def _test_plus_grand_multiple_2(plus_grand_multiple_2):
    r = plus_grand_multiple_2(3, 20)
    if isinstance(r, float):
        _faux("ta fonction renvoie le nombre décimal " + _montre(r) + " : le symbole / donne un quotient décimal. "
              "Le quotient de la division euclidienne s'écrit b // a.")
    if r == 6:
        _faux("ta fonction renvoie 6 : c'est le quotient 20 // 3. Le multiple cherché est a × quotient, soit 3 × 6 = 18.")
    if r == 20:
        _faux("ta fonction renvoie 20, qui n'est pas un multiple de 3. Attention aux priorités : "
              "écris a * (b // a), avec des parenthèses.")
    if r != 18:
        _faux("plus_grand_multiple_2(3, 20) doit renvoyer 18. Ta fonction renvoie " + _montre(r) + ".")
    for a in range(1, 13):
        for b in range(0, 61):
            r = plus_grand_multiple_2(a, b)
            if r != a * (b // a):
                _faux("pour a = " + str(a) + " et b = " + str(b) + ", le plus grand multiple de a inférieur ou égal "
                      "à b est " + str(a * (b // a)) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "ta formule donne le bon résultat pour les 732 couples (a ; b) essayés, avec 1 ≤ a ≤ 12 et 0 ≤ b ≤ 60."


def verifier_plus_grand_multiple_2():
    """Vérifie la fonction plus_grand_multiple_2."""
    _verifier(_test_plus_grand_multiple_2, ["plus_grand_multiple_2"],
              aide={"division": "Ici a n'est jamais nul : vérifie que tu divises b par a, et non par autre chose."})


def _test_nombre_diviseurs(nombre_diviseurs):
    r = nombre_diviseurs(12)
    if r == 5:
        _faux("ta fonction oublie un diviseur : n est toujours un diviseur de lui-même. "
              "La boucle doit aller jusqu'à n inclus : range(1, n + 1).")
    if r == 12:
        _faux("ta fonction compte tous les nombres de 1 à 12 : il faut garder seulement ceux qui divisent n, "
              "avec le test if n % d == 0:")
    if r == 1:
        _faux("ta fonction ne trouve qu'un diviseur de 12. Deux causes possibles : tu testes si d est un multiple "
              "de n (il faut tester si n est un multiple de d : n % d == 0), " + _RETURN_OU)
    if r == 28:
        _faux("ta fonction additionne les diviseurs (1 + 2 + 3 + 4 + 6 + 12 = 28). "
              "Un compteur augmente de 1 : compteur = compteur + 1.")
    if r == 0:
        _faux("ta fonction renvoie 0 : le compteur n'augmente jamais. Dans la boucle, écris le test "
              "if n % d == 0: puis, en dessous et décalé, compteur = compteur + 1.")
    if r != 6:
        _faux("les diviseurs positifs de 12 sont 1, 2, 3, 4, 6 et 12 : il y en a 6. Ta fonction renvoie " + _montre(r) + ".")
    r = nombre_diviseurs(1)
    if r != 1:
        _faux("1 a un seul diviseur positif : 1. Ta fonction renvoie " + _montre(r) + ".")
    r = nombre_diviseurs(36)
    if r != 9:
        _faux("36 a 9 diviseurs positifs : 1, 2, 3, 4, 6, 9, 12, 18, 36. Ta fonction renvoie " + _montre(r) + ".")
    return "12 a 6 diviseurs positifs, 1 en a 1 et 36 en a 9."


def verifier_nombre_diviseurs():
    """Vérifie la fonction nombre_diviseurs."""
    _verifier(_test_nombre_diviseurs, ["nombre_diviseurs"],
              aide={"division": "Ta boucle commence à 0, et on ne peut pas diviser par 0. "
                                "Un diviseur n'est jamais nul : commence à 1, range(1, n + 1)."})


def _affichage(afficher_diviseurs, n):
    r, texte = _sortie(afficher_diviseurs, n)
    morceaux = texte.split()
    nombres = []
    for m in morceaux:
        if m.lstrip("-").isdigit():
            nombres.append(int(m))
        else:
            _faux("afficher_diviseurs(" + str(n) + ") doit afficher seulement des nombres. "
                  "Elle affiche : " + texte.strip().replace("\n", " ") + ".")
    return nombres


def _test_afficher_diviseurs(afficher_diviseurs):
    obtenus = _affichage(afficher_diviseurs, 12)
    if obtenus == []:
        _faux("afficher_diviseurs(12) n'affiche rien. Vérifie le test après if, et que la ligne print(d) "
              "est bien décalée sous le if.")
    if obtenus == [12]:
        _faux("ta fonction n'affiche que 12 : tu testes si d est un multiple de n. "
              "Il faut tester si n est un multiple de d, avec n % d == 0.")
    if obtenus == list(range(1, 13)):
        _faux("ta fonction affiche tous les nombres de 1 à 12 : la condition après if est toujours vraie. "
              "Il faut garder seulement les d qui divisent n : n % d == 0.")
    if obtenus != [1, 2, 3, 4, 6, 12]:
        _faux("afficher_diviseurs(12) doit afficher 1, 2, 3, 4, 6 et 12. Ta fonction affiche "
              + ", ".join(str(x) for x in obtenus) + ".")
    obtenus = _affichage(afficher_diviseurs, 30)
    if obtenus != [1, 2, 3, 5, 6, 10, 15, 30]:
        _faux("les diviseurs positifs de 30 sont 1, 2, 3, 5, 6, 10, 15 et 30. Ta fonction affiche "
              + ", ".join(str(x) for x in obtenus) + ".")
    obtenus = _affichage(afficher_diviseurs, 1)
    if obtenus != [1]:
        _faux("le seul diviseur positif de 1 est 1. Ta fonction affiche "
              + (", ".join(str(x) for x in obtenus) if obtenus else "rien") + ".")
    return "afficher_diviseurs(12) affiche 1, 2, 3, 4, 6 et 12 ; les cas n = 30 et n = 1 sont justes aussi."


def verifier_afficher_diviseurs():
    """Vérifie la fonction afficher_diviseurs."""
    _verifier(_test_afficher_diviseurs, ["afficher_diviseurs"],
              aide={"division": "On ne peut pas diviser par 0 : la boucle doit commencer à 1."})


def _test_est_pair(est_pair):
    r = est_pair(10)
    _booleen(r, "est_pair(10)", "Compare le reste à 0 avec == : n % 2 == 0.")
    if r is False and est_pair(7) is True:
        _faux("ta fonction répond l'inverse : elle teste si n est impair. "
              "Un nombre pair a un reste nul dans la division par 2 : n % 2 == 0.")
    if r is not True:
        _faux("10 = 2 × 5 est pair : est_pair(10) doit renvoyer True. Ta fonction renvoie " + _montre(r) + ".")
    if est_pair(7) is not False:
        _faux("7 = 2 × 3 + 1 est impair : est_pair(7) doit renvoyer False.")
    if est_pair(0) is not True:
        _faux("0 = 2 × 0 est pair : est_pair(0) doit renvoyer True.")
    if est_pair(-4) is not True:
        _faux("-4 = 2 × (-2) est pair : est_pair(-4) doit renvoyer True.")
    if est_pair(-3) is not False:
        _faux("-3 = 2 × (-2) + 1 est impair : est_pair(-3) doit renvoyer False.")
    return "est_pair(10) renvoie True, est_pair(7) renvoie False ; les cas 0, -4 et -3 sont justes aussi."


def verifier_est_pair():
    """Vérifie la fonction est_pair."""
    _verifier(_test_est_pair, ["est_pair"])


def _test_cagettes(mangues_rangees, cagettes, reste):
    if mangues_rangees == 20:
        _faux("20 est le nombre de cagettes, pas le nombre de mangues rangées : utilise plus_grand_multiple(12, 250).")
    if mangues_rangees != 240:
        _faux("le nombre de mangues rangées est le plus grand multiple de 12 inférieur ou égal à 250. "
              "Tu as " + _montre(mangues_rangees) + ".")
    if isinstance(cagettes, float):
        _faux("le nombre de cagettes doit être un entier : utilise le quotient 250 // 12, et non 250 / 12.")
    if cagettes != 20:
        _faux("240 mangues remplissent 240 ÷ 12 cagettes. Tu as " + _montre(cagettes) + ".")
    if reste != 10:
        _faux("il reste 250 - 240 mangues (c'est aussi 250 % 12). Tu as " + _montre(reste) + ".")
    return "240 mangues rangées dans 20 cagettes pleines, il en reste 10 : 250 = 12 × 20 + 10."


def verifier_cagettes():
    """Vérifie les trois réponses du défi des mangues."""
    _verifier(_test_cagettes, ["mangues_rangees", "cagettes", "reste"])


print("Vérifications prêtes. Tu peux commencer.")
