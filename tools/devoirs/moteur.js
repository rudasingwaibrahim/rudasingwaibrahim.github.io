/* ==== DÉBUT MOTEUR SIGMA ====
   Moteur des devoirs en ligne Σ Sigma : sujets personnalisés et corrigé.
   Source unique : tools/devoirs/moteur.js. NE PAS MODIFIER ailleurs :
   « python3 tools/devoirs/sync.py » le recopie dans tools/devoirs/Code.gs (serveur)
   et dans _includes/devoirs/moteur-demo.js (mode démo du site, inclus seulement
   tant que devoirs_url est vide dans _config.yml).
   La saisie tolérante (norm, evaluate, accept…) est une copie conforme de assets/js/quiz.js. */
var SigmaMoteur = (function () {
  'use strict';

  /* ── Hachage et hasard déterministe ──────────────────────────────── */
  function hash32(str) {
    var h = 0x811c9dc5;
    str = String(str);
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b) >>> 0; h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35) >>> 0; h ^= h >>> 16;
    return h >>> 0;
  }
  function Hasard(seed) {
    var a = seed >>> 0;
    function reel() {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    return {
      reel: reel,
      entier: function (min, max) { return min + Math.floor(reel() * (max - min + 1)); },
      choisir: function (t) { return t[Math.floor(reel() * t.length)]; },
      melanger: function (t) { t = t.slice(); for (var i = t.length - 1; i > 0; i--) { var j = Math.floor(reel() * (i + 1)); var x = t[i]; t[i] = t[j]; t[j] = x; } return t; }
    };
  }
  /* Identité normalisée : « Léa  D'ALMEIDA » = « léa d'almeida » (accents, casse, espaces, tirets). */
  function normIdent(s) {
    return String(s == null ? '' : s).replace(/[’`ʼ]/g, "'").normalize('NFD').replace(/[̀-ͯ]/g, '')
      .toLowerCase().replace(/[^a-z' -]/g, '').replace(/[\s-]+/g, ' ').trim();
  }
  function graine(devoir, nom, prenom, classe, essai, sel) {
    return hash32([sel || '', devoir, normIdent(nom), normIdent(prenom), String(classe), String(essai)].join('|'));
  }

  /* ── Saisie tolérante : copie conforme de assets/js/quiz.js ──────── */
  function norm(s) {
    s = String(s == null ? '' : s).replace(/\$/g, '');
    s = s.replace(/\\(overrightarrow|vec)\{([^{}]*)\}/g, '$2');
    s = s.replace(/\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}/g, '($1)/($2)')
      .replace(/\\sqrt\{([^{}]*)\}/g, 'sqrt($1)').replace(/\\(times|cdot)/g, '*').replace(/\\pi/g, 'pi')
      .replace(/\\(left|right)/g, '').replace(/\{,\}/g, ',').replace(/\\[,;!: ]/g, '').replace(/\\/g, '');
    s = s.replace(/[{}]/g, function (c) { return c === '{' ? '(' : ')'; });
    s = s.replace(/[−‒–—‐]/g, '-').replace(/[×·⋅∙✕]/g, '*').replace(/÷/g, '/')
      .replace(/²/g, '^2').replace(/³/g, '^3').replace(/√/g, 'sqrt').replace(/π/g, 'pi')
      .replace(/[’`']/g, "'").replace(/\*\*/g, '^');
    s = s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
    s = s.replace(/[\s  ]+/g, '').replace(/,/g, '.');
    s = s.replace(/([a-z)])\*/g, '$1').replace(/\*([a-z(])/g, '$1');
    s = s.replace(/sqrt\(([a-z0-9.]+)\)/g, 'sqrt$1').replace(/\^\(([-a-z0-9.]+)\)/g, '^$1');
    s = s.replace(/\(([a-z0-9.]+)\)\/\(([a-z0-9.]+)\)/g, '$1/$2');
    s = s.replace(/^\+/, '').replace(/\.$/, '');
    return s;
  }
  function evaluate(str, vars) {
    var toks = [], i = 0, m;
    var re = /\s*(\d+\.?\d*|\.\d+|sqrt|pi|[a-z]|[-+*\/^()])/y;
    while (i < str.length) {
      re.lastIndex = i; m = re.exec(str);
      if (!m) throw new Error('jeton');
      toks.push(m[1]); i = re.lastIndex;
    }
    var p = 0;
    function peek() { return toks[p]; }
    function starts(t) { return t != null && (/^[\d.]/.test(t) || /^[a-z]/.test(t) || t === '('); }
    function expr() { var v = term(); while (peek() === '+' || peek() === '-') { var o = toks[p++]; var w = term(); v = o === '+' ? v + w : v - w; } return v; }
    function term() {
      var v = unary();
      for (;;) {
        var t = peek();
        if (t === '*' || t === '/') { p++; var w = unary(); v = t === '*' ? v * w : v / w; }
        else if (starts(t)) { v = v * power(); }
        else return v;
      }
    }
    function unary() { if (peek() === '-') { p++; return -unary(); } if (peek() === '+') { p++; return unary(); } return power(); }
    function power() { var b = primary(); if (peek() === '^') { p++; return Math.pow(b, unary()); } return b; }
    function primary() {
      var t = toks[p++];
      if (t == null) throw new Error('fin');
      if (t === '(') { var v = expr(); if (toks[p++] !== ')') throw new Error(')'); return v; }
      if (t === 'sqrt') { var a = power(); return Math.sqrt(a); }
      if (t === 'pi') return Math.PI;
      if (/^[\d.]/.test(t)) return parseFloat(t);
      if (/^[a-z]$/.test(t)) { if (!vars || !(t in vars)) throw new Error('var'); return vars[t]; }
      throw new Error('?');
    }
    var r = expr();
    if (p !== toks.length) throw new Error('reste');
    return r;
  }
  var VARS = [];
  (function () {
    var base = [1.37, -2.21, 0.53, 3.09];
    for (var k = 0; k < base.length; k++) {
      var o = {}, L = 'abcdefghijklmnopqrstuvwxyz';
      for (var j = 0; j < L.length; j++) o[L[j]] = base[k] + 0.173 * j * (k + 1);
      VARS.push(o);
    }
  })();
  function sameValue(a, b, withVars) {
    try {
      var sets = withVars ? VARS : [null];
      for (var k = 0; k < sets.length; k++) {
        var x = evaluate(a, sets[k]), y = evaluate(b, sets[k]);
        if (!isFinite(x) || !isFinite(y) || Math.abs(x - y) > 1e-9 * Math.max(1, Math.abs(y))) return false;
      }
      return true;
    } catch (e) { return false; }
  }
  function stripParens(s) { var prev; do { prev = s; s = s.replace(/\([^()]*\)/g, 'P'); } while (s !== prev); return s; }
  function isProduct(s) { return s.indexOf('(') >= 0 && !/[+\-]/.test(stripParens(s).replace(/^-/, '')); }
  function sortProd(s) { return s.split('*').sort().join('*'); }
  function accept(input, q) {
    var a = norm(input);
    if (!a) return false;
    var reps = q.rep || [], mode = q.mode || 'txt';
    for (var i = 0; i < reps.length; i++) {
      var r = norm(reps[i]);
      if (a === r) return true;
      if (mode === 'num' && (r.indexOf('/') >= 0 ? /^-?(\d+\.?\d*|\.\d+)(\/\d+)?$/ : /^-?(\d+\.?\d*|\.\d+)$/).test(a) && sameValue(a, r, false)) return true;
      if (mode === 'prod' && sortProd(a) === sortProd(r)) return true;
      if (mode === 'dev' && a.indexOf('(') < 0 && sameValue(a, r, true)) return true;
      if (mode === 'fact' && isProduct(a) && sameValue(a, r, true)) return true;
    }
    return false;
  }

  /* ── Arithmétique ────────────────────────────────────────────────── */
  function estPremier(n) { if (n < 2) return false; for (var d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; }
  function facteurs(n) { var f = [], d = 2; while (n > 1) { var e = 0; while (n % d === 0) { n /= d; e++; } if (e) f.push([d, e]); d++; } return f; }
  function diviseurs(n) { var t = []; for (var d = 1; d <= n; d++) if (n % d === 0) t.push(d); return t; }
  function pgcdInterne(a, b) { while (b) { var r = a % b; a = b; b = r; } return a; } /* usage interne (construction), jamais affiché */
  /* Écritures LaTeX */
  function nb(n) { var s = String(Math.abs(n)); if (s.length > 3) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, '\\,'); return (n < 0 ? '-' : '') + s; }
  function texFact(n) { return facteurs(n).map(function (f) { return f[1] > 1 ? f[0] + '^{' + f[1] + '}' : String(f[0]); }).join(' \\times '); }
  function txtFact(n) { return facteurs(n).map(function (f) { return f[1] > 1 ? f[0] + '^' + f[1] : String(f[0]); }).join(' × '); }
  function liste(t) { return t.map(function (x) { return '$' + nb(x) + '$'; }).join(', '); }

  /* Décomposition saisie par l'élève : produit de nombres premiers (puissances permises, ordre libre). */
  function decompOk(input, n) {
    var s = norm(input).replace(/(\d)x(?=\d)/g, '$1*').replace(/\.(?=\d)/g, '*');
    if (!/^\d+(\^\d+)?(\*\d+(\^\d+)?)*$/.test(s)) return false;
    var parts = s.split('*'), prod = 1, vu = {};
    for (var i = 0; i < parts.length; i++) {
      var m = parts[i].match(/^(\d+)(?:\^(\d+))?$/), p = +m[1], e = m[2] ? +m[2] : 1;
      if (!estPremier(p) || e < 1 || e > 30) return false;
      vu[p] = (vu[p] || 0) + e;
    }
    for (var q in vu) prod *= Math.pow(+q, vu[q]);
    return prod === n;
  }
  /* Une réponse saisie, avec la petite tolérance propre aux trous (parenthèses extérieures superflues). */
  function accepte(input, spec) {
    var v = String(input == null ? '' : input).trim();
    if (!v) return false;
    if (spec.mode === 'decomp') return decompOk(v, spec.n);
    if (spec.mode === 'dev') { var w = v.replace(/^\s*\((.*)\)\s*$/, '$1'); if (w !== v && w.indexOf('(') < 0 && w.indexOf(')') < 0) v = w; }
    return accept(v, spec);
  }

  /* ═══ Devoirs ══════════════════════════════════════════════════════
     Chaque question : fonction (R) → objet. Champs publics : type, titre, enonce, choix, texte, clavier, points.
     Champs du corrigé (jamais envoyés au navigateur en mode réel) : bonne, rep, mode, n, trous[].rep, aff, expl, params. */
  var DEVOIRS = {};
  var NIV = { f: 'Pour démarrer', m: 'Je m\'entraîne', e: 'Je vais plus loin' };

  DEVOIRS['seconde-ch4-dm1'] = {
    titre: 'DM 1 — Multiples, diviseurs, pair et impair',
    chapitre: 'Seconde · Chapitre 4 — Nombres entiers',
    questions: [
      /* Q1 — facile : reconnaître un multiple */
      function (R) {
        var a = R.choisir([6, 7, 8, 9, 11, 12, 13, 14, 15]), k = R.entier(12, 45), bon = a * k, faux = [];
        while (faux.length < 3) {
          var kk = R.entier(12, 45), r = R.entier(1, a - 1), v = a * kk + r;
          if (v !== bon && faux.indexOf(v) < 0) faux.push(v);
        }
        var ordre = R.melanger([bon].concat(faux));
        return {
          niveau: 'f', titre: 'Reconnaître un multiple', type: 'qcm', points: 2,
          enonce: 'Parmi les nombres suivants, un seul est un multiple de $' + a + '$. Lequel ?',
          choix: ordre.map(function (v) { return '$' + nb(v) + '$'; }), bonne: ordre.indexOf(bon),
          expl: '$' + nb(bon) + ' = ' + a + ' \\times ' + k + '$ avec $' + k + '$ entier : c\'est un multiple de $' + a + '$. Les autres ne le sont pas, car la division par $' + a + '$ laisse un reste non nul : ' +
            faux.map(function (v) { return '$' + nb(v) + ' = ' + a + ' \\times ' + Math.floor(v / a) + ' + ' + (v % a) + '$'; }).join(' ; ') + '.',
          params: { a: a, bon: bon, faux: faux }
        };
      },
      /* Q2 — facile : écrire un impair sous la forme 2k + 1 */
      function (R) {
        var k = R.entier(120, 980), n = 2 * k + 1;
        return {
          niveau: 'f', titre: 'Écriture d\'un nombre impair', type: 'saisie', clavier: 'nombre', points: 2,
          enonce: 'Le nombre $' + nb(n) + '$ est impair : il s\'écrit $' + nb(n) + ' = 2k + 1$ avec $k$ entier. Quelle est la valeur de $k$ ?',
          mode: 'num', rep: [String(k)], aff: '$k = ' + nb(k) + '$',
          expl: '$' + nb(n) + ' - 1 = ' + nb(n - 1) + '$ et $' + nb(n - 1) + ' \\div 2 = ' + nb(k) + '$, donc $' + nb(n) + ' = 2 \\times ' + nb(k) + ' + 1$.',
          params: { n: n, k: k }
        };
      },
      /* Q3 — moyenne : compter les diviseurs */
      function (R) {
        var n, d;
        do { n = R.entier(36, 200); d = diviseurs(n); } while (d.length < 6 || d.length > 12);
        var paires = [];
        for (var i = 0; i < d.length && d[i] * d[i] <= n; i++) paires.push(d[i] + ' \\times ' + (n / d[i]));
        return {
          niveau: 'm', titre: 'Diviseurs d\'un entier', type: 'saisie', clavier: 'nombre', points: 2,
          enonce: 'Combien le nombre $' + n + '$ a-t-il de diviseurs positifs (en comptant $1$ et $' + n + '$) ?',
          mode: 'num', rep: [String(d.length)], aff: '$' + d.length + '$ diviseurs',
          expl: 'On cherche les diviseurs par paires : $' + n + ' = ' + paires.join(' = ') + '$. Les diviseurs de $' + n + '$ sont donc ' + liste(d) + ' : il y en a $' + d.length + '$.',
          params: { n: n, nd: d.length }
        };
      },
      /* Q4 — moyenne : plus grand multiple de a inférieur ou égal à b (algorithme du programme) */
      function (R) {
        var a, b, q, r;
        do { a = R.choisir([7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25]); b = R.entier(150, 999); q = Math.floor(b / a); r = b % a; } while (r === 0 || r === a - 1);
        var m = a * q;
        return {
          niveau: 'm', titre: 'Plus grand multiple inférieur ou égal à un nombre', type: 'saisie', clavier: 'nombre', points: 2,
          enonce: 'Quel est le plus grand multiple de $' + a + '$ inférieur ou égal à $' + nb(b) + '$ ?',
          mode: 'num', rep: [String(m)], aff: '$' + nb(m) + '$',
          expl: 'On divise $' + nb(b) + '$ par $' + a + '$ : $' + nb(b) + ' = ' + a + ' \\times ' + q + ' + ' + r + '$ avec $0 < ' + r + ' < ' + a + '$. ' +
            'Donc $' + a + ' \\times ' + q + ' = ' + nb(m) + ' \\leqslant ' + nb(b) + '$, alors que le multiple suivant, $' + a + ' \\times ' + (q + 1) + ' = ' + nb(m + a) + '$, dépasse $' + nb(b) + '$. ' +
            'C\'est ce que fait l\'algorithme du cours : partir de $0$ et ajouter $' + a + '$ tant que le résultat reste inférieur ou égal à $' + nb(b) + '$.',
          params: { a: a, b: b, q: q, r: r, m: m }
        };
      },
      /* Q5 — moyenne : démonstration guidée à trous (le carré d'un nombre impair est impair) */
      function (R) {
        var K = R.entier(11, 60), n = 2 * K + 1, k2 = 2 * K * K + 2 * K;
        return {
          niveau: 'm', titre: 'Démonstration : carré d\'un nombre impair', type: 'trous', points: 2,
          enonce: 'Complète la démonstration de la propriété du cours : « le carré d\'un nombre impair est impair », puis applique-la au nombre impair $' + n + '$.',
          texte: 'Soit $a$ un entier impair : il existe un entier $k$ tel que $a = 2k + 1$.\n' +
            'Alors $a^2 = (2k + 1)^2 = 4k^2 +$ [[0]] $+ 1 = 2 \\times$ ( [[1]] ) $+ 1$.\n' +
            'Comme $2k^2 + 2k$ est un entier, $a^2$ est [[2]].\n' +
            'Application : $' + n + ' = 2 \\times ' + K + ' + 1$, donc $' + n + '^2 = 2 \\times$ [[3]] $+ 1$.',
          trous: [
            { rep: ['4k'], mode: 'dev', aff: '$4k$', clavier: 'texte' },
            { rep: ['2k^2+2k'], mode: 'dev', aff: '$2k^2 + 2k$', clavier: 'texte' },
            { rep: ['impair', 'unimpair', 'unnombreimpair'], mode: 'txt', aff: 'impair', clavier: 'texte' },
            { rep: [String(k2)], mode: 'num', aff: '$' + nb(k2) + '$', clavier: 'nombre' }
          ],
          aff: '$4k$ ; $2k^2 + 2k$ ; impair ; $' + n + '^2 = 2 \\times ' + nb(k2) + ' + 1$',
          expl: 'On développe avec $(a + b)^2 = a^2 + 2ab + b^2$ : $(2k + 1)^2 = 4k^2 + 4k + 1$, puis on factorise par $2$ les deux premiers termes : $4k^2 + 4k = 2(2k^2 + 2k)$. ' +
            'Pour l\'application, avec $k = ' + K + '$ : $2k^2 + 2k = 2 \\times ' + (K * K) + ' + 2 \\times ' + K + ' = ' + nb(k2) + '$, et l\'on vérifie que $' + n + '^2 = ' + nb(n * n) + ' = 2 \\times ' + nb(k2) + ' + 1$.',
          params: { K: K, n: n, k2: k2 }
        };
      },
      /* Q6 — moyenne : fraction irréductible */
      function (R) {
        var p, q, g;
        do { p = R.entier(2, 29); q = R.entier(3, 31); g = R.choisir([6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]); }
        while (p === q || pgcdInterne(p, q) !== 1 || g * p > 999 || g * q > 999);
        var A = g * p, B = g * q;
        return {
          niveau: 'm', titre: 'Fraction irréductible', type: 'saisie', clavier: 'fraction', points: 2,
          enonce: 'Écris la fraction $\\dfrac{' + A + '}{' + B + '}$ sous forme irréductible.',
          aide: 'Écris ta fraction avec la barre /, par exemple 3/4.',
          mode: 'txt', rep: [p + '/' + q], aff: '$\\dfrac{' + p + '}{' + q + '}$',
          expl: '$' + A + ' = ' + g + ' \\times ' + p + '$ et $' + B + ' = ' + g + ' \\times ' + q + '$ : $' + g + '$ est un diviseur commun de $' + A + '$ et de $' + B + '$. On simplifie par $' + g + '$ : $\\dfrac{' + A + '}{' + B + '} = \\dfrac{' + p + ' \\times ' + g + '}{' + q + ' \\times ' + g + '} = \\dfrac{' + p + '}{' + q + '}$. ' +
            'Les nombres $' + p + '$ et $' + q + '$ n\'ont plus de diviseur commun autre que $1$ : la fraction est irréductible.',
          params: { A: A, B: B, p: p, q: q }
        };
      },
      /* Q7 — exigeante : parité d'une expression, pour tout entier n */
      function (R) {
        var b = R.entier(1, 9), c = R.entier(1, 9);
        var A = 'n^2 + ' + (b === 1 ? '' : b) + 'n + ' + c, bn = (b === 1 ? '' : b) + 'n';
        var choix = ['$A$ est pair pour tout entier $n$.', '$A$ est impair pour tout entier $n$.', 'La parité de $A$ dépend de l\'entier $n$.'];
        var bonne = b % 2 === 1 ? (c % 2 === 0 ? 0 : 1) : 2, expl;
        if (b % 2 === 1) {
          expl = '$n^2 + ' + bn + ' = n(n + ' + b + ')$. Si $n$ est pair, ce produit est pair. Si $n$ est impair, $n + ' + b + '$ est pair (impair + impair), donc le produit est encore pair. ' +
            'Ainsi $n^2 + ' + bn + '$ est toujours pair, et $A = (n^2 + ' + bn + ') + ' + c + '$ a la parité de $' + c + '$ : $A$ est toujours ' + (c % 2 === 0 ? 'pair' : 'impair') + '.';
        } else {
          expl = '$' + b + 'n = 2 \\times ' + (b / 2) + 'n$ est toujours pair, mais $n^2$ a la parité de $n$ (le carré d\'un pair est pair, le carré d\'un impair est impair). ' +
            'Par exemple, pour $n = 0$ : $A = ' + c + '$ ; pour $n = 1$ : $A = ' + (1 + b + c) + '$. Ces deux nombres n\'ont pas la même parité : la parité de $A$ dépend de $n$.';
        }
        var ordre = R.melanger([0, 1, 2]);
        return {
          niveau: 'e', titre: 'Parité d\'une expression', type: 'qcm', points: 2,
          enonce: 'Pour tout entier $n$, on pose $A = ' + A + '$. Quelle affirmation est vraie ?',
          choix: ordre.map(function (i) { return choix[i]; }), bonne: ordre.indexOf(bonne), expl: expl,
          params: { b: b, c: c, verdict: ['pair', 'impair', 'depend'][bonne] }
        };
      },
      /* Q8 — exigeante : entiers consécutifs (modélisation) */
      function (R) {
        var k = R.choisir([3, 5]), n = R.entier(18, 240), h = (k - 1) / 2, mil = n + h, S = k * mil, grand = n + k - 1;
        var mots = { 3: 'trois', 5: 'cinq' }, termes = k === 3 ? '$m - 1$, $m$ et $m + 1$' : '$m - 2$, $m - 1$, $m$, $m + 1$ et $m + 2$';
        return {
          niveau: 'e', titre: 'Entiers consécutifs', type: 'saisie', clavier: 'nombre', points: 2,
          enonce: 'La somme de ' + mots[k] + ' entiers consécutifs est égale à $' + nb(S) + '$. Quel est le plus grand de ces ' + mots[k] + ' entiers ?',
          mode: 'num', rep: [String(grand)], aff: '$' + nb(grand) + '$',
          expl: 'Notons $m$ l\'entier du milieu : les ' + mots[k] + ' entiers sont ' + termes + ', et leur somme vaut $' + k + 'm$. ' +
            'Donc $' + k + 'm = ' + nb(S) + '$, soit $m = ' + nb(S) + ' \\div ' + k + ' = ' + nb(mil) + '$. Les entiers vont de $' + nb(n) + '$ à $' + nb(grand) + '$ : le plus grand est $' + nb(grand) + '$.',
          params: { k: k, S: S, grand: grand }
        };
      },
      /* Q9 — exigeante : démonstration guidée à trous (somme de deux multiples) */
      function (R) {
        var a = R.choisir([3, 4, 6, 7, 8, 9, 11, 12, 13]), p = R.entier(21, 140), q;
        do { q = R.entier(21, 140); } while (q === p);
        var A = a * p, B = a * q;
        return {
          niveau: 'e', titre: 'Démonstration : somme de deux multiples', type: 'trous', points: 4,
          enonce: 'Complète la démonstration de la propriété du cours : «\u00a0la somme de deux multiples de $' + a + '$ est un multiple de $' + a + '$\u00a0», puis applique-la.',
          texte: 'Soient $b$ et $c$ deux multiples de $' + a + '$. Il existe deux entiers $k$ et $m$ tels que $b = ' + a + 'k$ et $c =$ [[0]].\n' +
            'Alors $b + c = ' + a + 'k + ' + a + 'm = ' + a + ' \\times$ ( [[1]] ).\n' +
            'La somme de deux entiers est un entier : $b + c$ est donc un [[2]] de $' + a + '$.\n' +
            'Application : $' + nb(A) + ' = ' + a + ' \\times ' + p + '$ et $' + nb(B) + ' = ' + a + ' \\times ' + q + '$, donc $' + nb(A) + ' + ' + nb(B) + ' = ' + a + ' \\times$ [[3]].',
          trous: [
            { rep: [a + 'm'], mode: 'dev', aff: '$' + a + 'm$', clavier: 'texte' },
            { rep: ['k+m'], mode: 'dev', aff: '$k + m$', clavier: 'texte' },
            { rep: ['multiple', 'multiples', 'unmultiple'], mode: 'txt', aff: 'multiple', clavier: 'texte' },
            { rep: [String(p + q)], mode: 'num', aff: '$' + (p + q) + '$', clavier: 'nombre' }
          ],
          aff: '$c = ' + a + 'm$ ; $b + c = ' + a + '(k + m)$ ; multiple ; $' + nb(A) + ' + ' + nb(B) + ' = ' + a + ' \\times ' + (p + q) + '$',
          expl: '$c$ est un multiple de $' + a + '$ : $c = ' + a + 'm$. On factorise par $' + a + '$ : $' + a + 'k + ' + a + 'm = ' + a + '(k + m)$, et $k + m$ est un entier. ' +
            'Pour l\'application : $' + nb(A) + ' + ' + nb(B) + ' = ' + a + ' \\times ' + p + ' + ' + a + ' \\times ' + q + ' = ' + a + ' \\times (' + p + ' + ' + q + ') = ' + a + ' \\times ' + (p + q) + ' = ' + nb(A + B) + '$.',
          params: { a: a, p: p, q: q }
        };
      }
    ]
  };

  /* ── Génération et correction ───────────────────────────────────── */
  function genererComplet(devoir, g) {
    var D = DEVOIRS[devoir];
    if (!D) return null;
    return D.questions.map(function (fn, i) {
      var q = fn(Hasard(hash32(g + '|q' + (i + 1))));
      q.id = 'q' + (i + 1); q.numero = i + 1; q.niveauTexte = NIV[q.niveau];
      ['enonce', 'aide', 'texte', 'aff', 'expl'].forEach(function (k) { if (typeof q[k] === 'string') q[k] = typo(q[k]); });
      if (q.choix) q.choix = q.choix.map(typo);
      if (q.trous) q.trous.forEach(function (t) { t.aff = typo(t.aff); });
      return q;
    });
  }
  /* Typographie française hors formules : espace insécable avant : ; ! ? » et après « (pas de ponctuation seule en début de ligne). */
  function typo(s) {
    return String(s).split('$').map(function (p, i) { return i % 2 ? p : p.replace(/ ([:;!?»])/g, '\u00a0$1').replace(/« /g, '«\u00a0'); }).join('$');
  }
  var PUBLICS = ['id', 'numero', 'niveau', 'niveauTexte', 'titre', 'type', 'clavier', 'points', 'enonce', 'aide', 'choix', 'texte'];
  function versionPublique(q) {
    var o = {};
    PUBLICS.forEach(function (k) { if (q[k] != null) o[k] = q[k]; });
    if (q.trous) o.trous = q.trous.map(function (t) { return { clavier: t.clavier || 'texte' }; });
    return o;
  }
  /* Sujet public (sans corrigé) */
  function sujet(devoir, ident, essai, sel) {
    var D = DEVOIRS[devoir];
    if (!D) return null;
    var qs = genererComplet(devoir, graine(devoir, ident.nom, ident.prenom, ident.classe, essai, sel));
    var total = qs.reduce(function (s, q) { return s + q.points; }, 0);
    return { devoir: devoir, titre: D.titre, chapitre: D.chapitre, essai: essai, total: total, questions: qs.map(versionPublique) };
  }
  /* Correction : reponses = { q1: 2, q2: "786", q9: ["7m", "k+m", "multiple", "203"] } (QCM : indice du choix). */
  function corriger(devoir, ident, essai, sel, reponses) {
    var qs = genererComplet(devoir, graine(devoir, ident.nom, ident.prenom, ident.classe, essai, sel));
    if (!qs) return null;
    reponses = reponses || {};
    var detail = [], points = 0, total = 0;
    qs.forEach(function (q) {
      var r = reponses[q.id], pts = 0, vide = false, trous = null;
      if (q.type === 'qcm') {
        var idx = (typeof r === 'number' || (typeof r === 'string' && /^\d+$/.test(r))) ? +r : -1;
        vide = idx < 0;
        if (idx === q.bonne) pts = q.points;
      } else if (q.type === 'saisie') {
        vide = !(typeof r === 'string' && r.trim());
        if (!vide && accepte(r, q)) pts = q.points;
      } else if (q.type === 'trous') {
        var arr = Array.isArray(r) ? r : [], par = q.points / q.trous.length;
        trous = q.trous.map(function (t, i) {
          var v = typeof arr[i] === 'string' ? arr[i] : '', ok = !!v.trim() && accepte(v, t);
          if (ok) pts += par;
          return { ok: ok, attendu: t.aff };
        });
        vide = !arr.some(function (v) { return typeof v === 'string' && v.trim(); });
      }
      points += pts; total += q.points;
      detail.push({
        id: q.id, numero: q.numero, titre: q.titre, points: pts, max: q.points,
        statut: pts === q.points ? 'juste' : (pts > 0 ? 'partiel' : (vide ? 'vide' : 'faux')),
        attendu: q.type === 'qcm' ? q.choix[q.bonne] : q.aff, bonne: q.type === 'qcm' ? q.bonne : undefined,
        explication: q.expl, trous: trous || undefined
      });
    });
    var note = Math.round(20 * points / total * 2) / 2;
    return { note: note, sur: 20, points: points, total: total, detail: detail };
  }

  return {
    version: '1.0', DEVOIRS: DEVOIRS, hash32: hash32, Hasard: Hasard, normIdent: normIdent, graine: graine,
    norm: norm, accept: accept, accepte: accepte, decompOk: decompOk, estPremier: estPremier, facteurs: facteurs,
    genererComplet: genererComplet, sujet: sujet, corriger: corriger, existe: function (d) { return !!DEVOIRS[d]; },
    titre: function (d) { return DEVOIRS[d] ? DEVOIRS[d].titre : d; }
  };
})();
/* ==== FIN MOTEUR SIGMA ==== */
