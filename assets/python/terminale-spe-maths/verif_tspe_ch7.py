"""Vérifications du carnet Python « Terminale spécialité · Chapitre 7 · Loi binomiale : simulation, planche de Galton, surréservation ».

Ce fichier accompagne le carnet ch7-loi-binomiale-galton.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch7 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_binomiale(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_binomiale', 'verifier_galton', 'verifier_proba', 'verifier_seuil_surreservation']

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
def _test_binomiale(bernoulli, binomiale):
    with _Graine(70):
        b = [bernoulli(0.3) for k in range(2000)]
    for x in b:
        if x != 0 and x != 1:
            _faux("bernoulli(0.3) doit renvoyer 0 ou 1. Ta fonction renvoie " + _montre(x) + ".")
    f = b.count(1) / 2000
    if abs(f - 0.7) < 0.04:
        _faux("bernoulli(0.3) renvoie 1 avec une fréquence proche de 0,7 : le succès a la probabilité p, la condition est "
              "random() < p.")
    if abs(f - 0.3) > 0.04:
        _faux("sur 2000 essais, bernoulli(0.3) renvoie 1 avec la fréquence " + _ecrire(f, 3) + ", trop loin de 0,3.")
    with _Graine(71):
        r = [binomiale(10, 0.3) for k in range(1500)]
    for x in r:
        if not isinstance(x, int) or x < 0 or x > 10:
            _faux("binomiale(10, 0.3) doit renvoyer un entier de 0 à 10. Ta fonction renvoie " + _montre(x) + ".")
    if r.count(0) + r.count(1) == 1500:
        _faux("binomiale(10, 0.3) ne renvoie que 0 ou 1 : il faut ajouter chaque succès au compteur, succes = succes + bernoulli(p).")
    if r.count(0) + r.count(10) == 1500:
        _faux("binomiale(10, 0.3) ne renvoie que 0 ou 10 : les épreuves doivent être indépendantes, avec un nouveau tirage "
              "bernoulli(p) à chaque tour de boucle.")
    m = sum(r) / 1500
    if abs(m - 3) > 0.2:
        _faux("sur 1500 simulations, la moyenne de binomiale(10, 0.3) vaut " + _ecrire(m, 3) + ", trop loin de E(X) = np = 3.")
    return "bernoulli(0.3) renvoie 1 dans " + _ecrire(100 * f, 1) + " % des cas ; la moyenne de 1500 réalisations de B(10 ; 0,3) vaut " + _ecrire(m, 2) + " (E(X) = 3)."


def verifier_binomiale():
    """Vérifie les fonctions bernoulli et binomiale."""
    _verifier(_test_binomiale, ["bernoulli", "binomiale"])


def _test_galton(echantillon, galton):
    with _Graine(72):
        e = echantillon(50, 10, 0.5)
    _est_liste(e, "echantillon(50, 10, 0.5)")
    if len(e) != 50:
        _faux("echantillon(50, 10, 0.5) doit renvoyer 50 réalisations. Ta liste en contient " + str(len(e))
              + " : écris [binomiale(n, p) for j in range(N)].")
    for x in e:
        if not isinstance(x, int) or x < 0 or x > 10:
            _faux("chaque élément de echantillon(50, 10, 0.5) doit être un entier de 0 à 10 (une réalisation de B(10 ; 0,5)). "
                  "Ta liste contient " + _montre(x) + ".")
    with _Graine(73):
        g = galton(10, 2000)
    _est_liste(g, "galton(10, 2000)")
    if len(g) != 11:
        _faux("galton(10, 2000) doit renvoyer 11 effectifs (réceptacles 0 à 10). Ta liste en contient " + str(len(g)) + ".")
    t = 0
    for x in g:
        t = t + x
    if t <= 11:
        _faux("les effectifs de galton(10, 2000) valent au plus 1 : chaque bille doit augmenter de 1 l'effectif de son réceptacle, "
              "effectifs[r] = effectifs[r] + 1.")
    if t != 2000:
        _faux("la somme des effectifs de galton(10, 2000) doit valoir 2000 (une bille par réceptacle). Elle vaut " + str(t) + ".")
    if abs(g[5] / 2000 - 0.2461) > 0.05:
        _faux("le réceptacle 5 reçoit " + _ecrire(g[5] / 2000, 3) + " des billes ; on attend environ P(X = 5) ≈ 0,246.")
    return "galton(10, 2000) renvoie " + _montre(g) + " : le réceptacle 5 reçoit " + _ecrire(100 * g[5] / 2000, 1) + " % des billes (P(X = 5) ≈ 24,6 %)."


def verifier_galton():
    """Vérifie les fonctions echantillon et galton."""
    _verifier(_test_galton, ["echantillon", "galton"],
              aide={"indice": "Un réceptacle a un numéro de 0 à n : vérifie que echantillon renvoie des réalisations de B(n ; p), "
                              "avec binomiale(n, p)."})


def _p(n, q, k):
    return _math.comb(n, k) * q ** k * (1 - q) ** (n - k)


def _test_proba(proba, proba_inf):
    r = proba(11, 0.4, 3)
    _nombre_attendu(r, "proba(11, 0.4, 3)")
    if _proche(r, 0.4 ** 3 * 0.6 ** 8):
        _faux("proba(11, 0.4, 3) renvoie la probabilité d'UN chemin : il faut multiplier par le nombre de chemins, comb(n, k).")
    if _proche(r, _math.comb(11, 3) * 0.4 ** 3 * 0.6 ** 11):
        _faux("l'exposant de 1 - p est le nombre d'échecs, n - k : (1 - p) ** (n - k).")
    if not _proche(r, _p(11, 0.4, 3), 1e-9):
        _faux("P(X = 3) = C(11, 3) × 0,4³ × 0,6⁸ ≈ 0,1774. Ta fonction renvoie " + _montre(r) + ".")
    r = proba_inf(11, 0.4, 5)
    if _proche(r, sum([_p(11, 0.4, i) for i in range(5)]), 1e-9):
        _faux("proba_inf(11, 0.4, 5) oublie P(X = 5) : pour i de 0 à k, écris range(k + 1).")
    if not _proche(r, sum([_p(11, 0.4, i) for i in range(6)]), 1e-9):
        _faux("P(X ≤ 5) ≈ 0,7535 pour X ~ B(11 ; 0,4). Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(proba_inf(11, 0.4, 11), 1, 1e-9):
        _faux("P(X ≤ 11) doit valoir 1 pour X ~ B(11 ; 0,4).")
    return "P(X = 3) ≈ 0,1774 et P(X ≤ 5) ≈ 0,7535 pour X ~ B(11 ; 0,4) ; P(X ≤ 11) = 1."


def verifier_proba():
    """Vérifie les fonctions proba et proba_inf."""
    _verifier(_test_proba, ["proba", "proba_inf"])


def _seuil(n, q, a):
    k = 0
    while 1 - sum([_p(n, q, i) for i in range(k + 1)]) > a:
        k = k + 1
    return k


def _test_seuil_surreservation(seuil_surreservation):
    try:
        r = seuil_surreservation(100, 0.15, 0.05)
    except OverflowError:
        _faux("ta boucle dépasse k = n sans s'arrêter (Python finit par calculer des nombres trop grands) : la condition doit "
              "porter sur P(X > k) = 1 - proba_inf(n, p, k), et non sur P(X = k).")
    if r == 0:
        _faux("seuil_surreservation(100, 0.15, 0.05) renvoie 0 : ta condition est fausse dès le départ. P(X > k) se calcule "
              "avec 1 - proba_inf(n, p, k).")
    if r != 21:
        _faux("P(X > 20) ≈ 0,066 > 0,05 et P(X > 21) ≈ 0,039 ≤ 0,05 : seuil_surreservation(100, 0.15, 0.05) doit renvoyer 21. "
              "Ta fonction renvoie " + _montre(r) + ". P(X > k) = 1 - P(X ≤ k) : utilise proba_inf.")
    for n, q, a in [(100, 0.15, 0.01), (50, 0.1, 0.05)]:
        if seuil_surreservation(n, q, a) != _seuil(n, q, a):
            _faux("seuil_surreservation(" + str(n) + ", " + str(q) + ", " + str(a) + ") doit renvoyer " + str(_seuil(n, q, a)) + ".")
    return "seuil_surreservation(100, 0.15, 0.05) = 21 ; avec α = 0,01, k = 24 ; pour B(50 ; 0,1) et α = 0,05, k = 9."


def verifier_seuil_surreservation():
    """Vérifie la fonction seuil_surreservation."""
    _verifier(_test_seuil_surreservation, ["seuil_surreservation"],
              aide={"boucle": "Ta boucle ne s'arrête pas : la condition doit porter sur P(X > k) = 1 - proba_inf(n, p, k), "
                              "qui diminue quand k augmente."})


print("Vérifications prêtes. Tu peux commencer.")
