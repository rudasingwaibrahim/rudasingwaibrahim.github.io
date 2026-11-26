/* ═══════════════════════════════════════════════════════════════════
   Σ Sigma — Entraînement interactif des chapitres (Seconde)
   Questions flash (5 min) · QCM intermédiaire · Texte à trous · QCM final
   Données : /assets/quiz/seconde/chN.json (attribut data-quiz du bloc).
   Vanilla, sans dépendance ; KaTeX utilisé s'il est présent (chargé sinon).
   Scores gardés sur l'appareil (localStorage « sigma-quiz-v1 »), sans compte.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var doc = document, body = doc.body;
  /* Données de la saisie tolérante et du clavier mathématique (avant le retour anticipé : utilisées par SigmaQuiz). */
  var VARS = [];
  (function () {
    var base = [1.37, -2.21, 0.53, 3.09];
    for (var k = 0; k < base.length; k++) {
      var o = {}, L = 'abcdefghijklmnopqrstuvwxyz';
      for (var j = 0; j < L.length; j++) o[L[j]] = base[k] + 0.173 * j * (k + 1);
      VARS.push(o);
    }
  })();
  var KEYS = [['−', '-'], [',', ','], ['x', 'x'], ['²', '²'], ['√', '√'], ['π', 'π'], ['/', '/'], ['(', '('], [')', ')']];
  /* Fonctions exportées pour les autres modules (devoirs en ligne) : saisie tolérante, clavier mathématique, rendu KaTeX. */
  window.SigmaQuiz = { norm: norm, evaluate: evaluate, accept: accept, sameValue: sameValue, md: md, tex: tex, esc: esc, mathPad: mathPad, needKatex: needKatex };
  var root = doc.querySelector('[data-quiz]');
  if (!root) return;
  var SRC = root.getAttribute('data-quiz');
  /* Mode « révisions » (page de classe) : data-quiz="liste" et data-quiz-list = fichiers des chapitres séparés par des virgules. */
  var LIST = (root.getAttribute('data-quiz-list') || '').split(',').filter(Boolean);
  var CH = root.getAttribute('data-quiz-ch') || '';
  var SKEY = 'sigma-quiz-v1';
  var SID = LIST.length ? 'seconde/revisions' : 'seconde/ch' + CH;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NB = ' ';
  var ACT = {
    flash: { nom: 'Questions flash', court: 'flash' },
    qcm_inter: { nom: 'QCM intermédiaire', court: 'QCM' },
    trous: { nom: 'Texte à trous', court: 'trous' },
    qcm_final: { nom: 'QCM final', court: 'QCM final' }
  };

  /* ── Outils ─────────────────────────────────────────────────────── */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function el(tag, cls, html) { var e = doc.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function tex(t, disp) {
    if (window.katex) { try { return window.katex.renderToString(t, { throwOnError: false, displayMode: !!disp }); } catch (e) {} }
    return '<span class="qz-tex">' + esc(t) + '</span>';
  }
  /* Texte avec formules $…$ : rendu KaTeX des formules, texte échappé. */
  function md(s) {
    var parts = String(s == null ? '' : s).split('$'), out = '';
    for (var i = 0; i < parts.length; i++) {
      if (i % 2) {
        /* la ponctuation qui suit une formule courte reste collée à elle (pas de « . » seul en début de ligne) ;
           une formule longue garde ses coupures internes (pas de débordement sur téléphone) */
        var m = parts[i].length <= 16 ? (parts[i + 1] || '').match(/^[.,;:)!?\u00a0\u202f]+/) : null, p = m ? m[0] : '';
        if (p) parts[i + 1] = parts[i + 1].slice(p.length);
        out += p ? '<span class="qz-nw">' + tex(parts[i]) + esc(p) + '</span>' : tex(parts[i]);
      } else out += esc(parts[i]).replace(/\n/g, '<br>');
    }
    return out;
  }
  function fmtTime(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
  function dur(s) { s = Math.round(s); var m = Math.floor(s / 60), r = s % 60; return (m ? m + NB + 'min' + (r ? ' ' : '') : '') + (r || !m ? r + NB + 's' : ''); }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function frDate(iso) { var p = (iso || '').split('-'); return p.length === 3 ? p[2] + '/' + p[1] : ''; }

  /* ── KaTeX à la demande ─────────────────────────────────────────── */
  var katexP = null;
  function needKatex() {
    if (window.katex) return Promise.resolve();
    if (katexP) return katexP;
    katexP = new Promise(function (res) {
      if (!doc.querySelector('link[href*="katex.min.css"]')) {
        var l = doc.createElement('link'); l.rel = 'stylesheet'; l.href = '/assets/lib/katex/katex.min.css'; doc.head.appendChild(l);
      }
      var s = doc.querySelector('script[src*="katex.min.js"]');
      if (!s) { s = doc.createElement('script'); s.src = '/assets/lib/katex/katex.min.js'; doc.head.appendChild(s); }
      var t0 = Date.now();
      (function wait() { if (window.katex || Date.now() - t0 > 8000) res(); else setTimeout(wait, 60); })();
    });
    return katexP;
  }

  /* ── Validation tolérante des réponses saisies ──────────────────── */
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
    s = s.replace(/[\s  ]+/g, '').replace(/,/g, '.');
    s = s.replace(/([a-z)])\*/g, '$1').replace(/\*([a-z(])/g, '$1');
    s = s.replace(/sqrt\(([a-z0-9.]+)\)/g, 'sqrt$1').replace(/\^\(([-a-z0-9.]+)\)/g, '^$1');
    s = s.replace(/\(([a-z0-9.]+)\)\/\(([a-z0-9.]+)\)/g, '$1/$2');
    s = s.replace(/^\+/, '').replace(/\.$/, '');
    return s;
  }
  /* Petit évaluateur (nombres, lettres, + − × / ^, parenthèses, sqrt, pi, multiplication implicite). */
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
      /* « num » : un nombre écrit simplement (entier ou décimal ; a/b seulement si la réponse attendue est une fraction),
         de même valeur que la réponse : recopier le calcul de l'énoncé ne suffit pas */
      if (mode === 'num' && (r.indexOf('/') >= 0 ? /^-?(\d+\.?\d*|\.\d+)(\/\d+)?$/ : /^-?(\d+\.?\d*|\.\d+)$/).test(a) && sameValue(a, r, false)) return true;
      if (mode === 'prod' && sortProd(a) === sortProd(r)) return true;
      if (mode === 'dev' && a.indexOf('(') < 0 && sameValue(a, r, true)) return true;
      if (mode === 'fact' && isProduct(a) && sameValue(a, r, true)) return true;
    }
    return false;
  }

  /* ── Scores (localStorage) ──────────────────────────────────────── */
  function sload() { try { var d = JSON.parse(localStorage.getItem(SKEY)); return d && d.s ? d : { v: 1, s: {} }; } catch (e) { return { v: 1, s: {} }; } }
  function ssave(d) { try { localStorage.setItem(SKEY, JSON.stringify(d)); } catch (e) {} }
  function record(act, score, total) {
    var d = sload(), c = d.s[SID] || (d.s[SID] = {}), r = c[act], better = !r || score / total > r.b / r.t;
    if (better) c[act] = { b: score, t: total, d: today(), n: (r ? r.n : 0) + 1 };
    else { r.n = (r.n || 0) + 1; }
    ssave(d); paintBest();
    return better && !!r;
  }
  function paintBest() {
    var c = sload().s[SID] || {};
    root.querySelectorAll('[data-qz-best]').forEach(function (b) {
      var r = c[b.getAttribute('data-qz-best')];
      b.textContent = r ? 'Meilleur' + NB + ': ' + r.b + '/' + r.t + ' · ' + frDate(r.d) : 'Pas encore fait';
      b.classList.toggle('is-done', !!r);
    });
  }
  function gcount(act) {
    var gc = window.goatcounter;
    if (!gc || typeof gc.count !== 'function') return;
    try { gc.count({ path: 'quiz/' + SID + '/' + act, title: ACT[act].nom + (LIST.length ? ' — révisions' : ' — chapitre ' + CH), event: true }); } catch (e) {}
  }
  function markVerified() {
    if (LIST.length) return false;
    var b = doc.querySelector('.prog-btn[data-prog="v"]');
    if (b && b.getAttribute('aria-pressed') !== 'true') { b.click(); return true; }
    return false;
  }

  /* ── Données ────────────────────────────────────────────────────── */
  var DATA = null, dataP = null, lastSeen = {};
  function loadData() {
    if (DATA) return Promise.resolve(DATA);
    if (dataP) return dataP;
    function get(u) { return fetch(u, { credentials: 'same-origin' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }); }
    var p = LIST.length ? Promise.all(LIST.map(function (u) { return get(u).catch(function () { return null; }); })).then(function (all) {
      var qs = [];
      all.forEach(function (d) {
        if (!d || !d.flash || !d.flash.questions) return;
        d.flash.questions.forEach(function (q) {
          var c = {}; for (var k in q) c[k] = q[k];
          c.chap = d.chapitre; qs.push(c);
        });
      });
      if (!qs.length) throw new Error('vide');
      return { flash: { duree: 300, servir: 10, questions: qs } };
    }) : get(SRC);
    dataP = p.then(function (d) { DATA = d; return d; })
      .catch(function (e) { dataP = null; throw e; });
    return dataP;
  }
  /* Tirage : ceux qui n'ont pas été servis à la partie précédente passent d'abord. */
  function draw(act, bank, n) {
    var seen = lastSeen[act] || {}, idx = shuffle(bank.map(function (_, i) { return i; }));
    var fresh = idx.filter(function (i) { return !seen[i]; }), old = idx.filter(function (i) { return seen[i]; });
    var pick = fresh.concat(old).slice(0, Math.min(n, bank.length));
    lastSeen[act] = {}; pick.forEach(function (i) { lastSeen[act][i] = 1; });
    return pick.map(function (i) { return bank[i]; });
  }
  function shuffledChoices(q) {
    var list = q.choix.map(function (c, i) { return { t: c, ok: i === q.bonne }; });
    return (q.choix.length <= 2 || q.fixe) ? list : shuffle(list);
  }

  /* ── Fenêtre de l'activité ──────────────────────────────────────── */
  var dlg = el('div', 'qz-dialog');
  dlg.hidden = true;
  dlg.setAttribute('role', 'dialog'); dlg.setAttribute('aria-modal', 'true'); dlg.setAttribute('aria-labelledby', 'qz-title');
  dlg.innerHTML =
    '<div class="qz-box">' +
      '<div class="qz-head">' +
        '<div class="qz-head-t"><p class="qz-kicker">' + (LIST.length ? 'Révisions · chapitres déjà vus' : 'Chapitre ' + esc(CH) + ' · Entraînement') + '</p><h2 id="qz-title"></h2></div>' +
        '<span class="qz-timer" hidden></span>' +
        '<button class="qz-close" type="button" aria-label="Fermer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg><span>Fermer</span></button>' +
      '</div>' +
      '<div class="qz-prog"><div class="qz-track" role="progressbar" aria-valuemin="0" aria-valuemax="10" aria-valuenow="0" aria-label="Progression"><span></span></div><span class="qz-count"></span></div>' +
      '<div class="qz-body" tabindex="-1"></div>' +
      '<div class="qz-foot"></div>' +
      '<p class="sr-only qz-live" aria-live="polite"></p>' +
    '</div>';
  body.appendChild(dlg);
  var $title = dlg.querySelector('#qz-title'), $timer = dlg.querySelector('.qz-timer'), $body = dlg.querySelector('.qz-body'),
      $foot = dlg.querySelector('.qz-foot'), $track = dlg.querySelector('.qz-track'), $bar = $track.querySelector('span'),
      $count = dlg.querySelector('.qz-count'), $live = dlg.querySelector('[aria-live]'), $prog = dlg.querySelector('.qz-prog');
  var opener = null, run = null, timerId = null;

  function say(t) { $live.textContent = ''; setTimeout(function () { $live.textContent = t; }, 30); }
  function setProgress(i, n, label) {
    $prog.hidden = false;
    $track.setAttribute('aria-valuemax', n); $track.setAttribute('aria-valuenow', i);
    $bar.style.width = (n ? Math.round(100 * i / n) : 0) + '%';
    $count.textContent = label || '';
  }
  function focusables() {
    return Array.prototype.slice.call(dlg.querySelectorAll('button, input, [href], [tabindex]:not([tabindex="-1"])'))
      .filter(function (n) { return !n.disabled && n.offsetParent !== null; });
  }
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key === 'Tab') {
      var f = focusables(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && (doc.activeElement === first || doc.activeElement === $body)) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      return;
    }
    if (run && run.onKey) run.onKey(e);
  });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
  dlg.querySelector('.qz-close').addEventListener('click', close);

  function open(act, from) {
    opener = from || doc.activeElement;
    dlg.hidden = false; body.classList.add('qz-open');
    $title.textContent = ACT[act].nom;
    $timer.hidden = true; $prog.hidden = true;
    $body.innerHTML = '<p class="qz-loading">Chargement…</p>'; $foot.innerHTML = '';
    dlg.querySelector('.qz-close').focus();
    gcount(act);
    Promise.all([loadData(), needKatex()]).then(function () {
      if (dlg.hidden) return;
      start(act);
    }).catch(function () {
      $body.innerHTML = '<p class="qz-msg qz-msg--ko">Impossible de charger l\'entraînement. Vérifie ta connexion, puis réessaie.</p>';
      $foot.innerHTML = '';
      var b = btn('Réessayer', 'btn btn--sm', function () { open(act, opener); }); $foot.appendChild(b);
    });
  }
  function close() {
    if (dlg.hidden) return;
    stopTimer(); run = null;
    dlg.hidden = true; body.classList.remove('qz-open');
    if (opener && opener.focus) opener.focus();
  }
  function btn(label, cls, fn) { var b = el('button', cls, label); b.type = 'button'; b.addEventListener('click', fn); return b; }
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }
  function scrollTop() { $body.scrollTop = 0; var box = dlg.querySelector('.qz-box'); if (box) box.scrollTop = 0; }

  /* ── Clavier mathématique (téléphone) ───────────────────────────── */
  function mathPad(getInput) {
    var pad = el('div', 'qz-pad');
    pad.setAttribute('role', 'group'); pad.setAttribute('aria-label', 'Clavier mathématique');
    KEYS.forEach(function (k) {
      var b = el('button', 'qz-key', esc(k[0])); b.type = 'button';
      b.setAttribute('aria-label', { '−': 'moins', ',': 'virgule', '²': 'au carré', '√': 'racine carrée', 'π': 'pi', '/': 'fraction (barre)', '(': 'parenthèse ouvrante', ')': 'parenthèse fermante', 'x': 'x' }[k[0]]);
      b.addEventListener('pointerdown', function (e) { e.preventDefault(); });
      b.addEventListener('click', function () {
        var inp = getInput(); if (!inp || inp.disabled) return;
        var s = inp.selectionStart == null ? inp.value.length : inp.selectionStart, t = inp.selectionEnd == null ? s : inp.selectionEnd;
        var ins = k[1] === '-' ? '−' : k[1];
        inp.value = inp.value.slice(0, s) + ins + inp.value.slice(t);
        try { inp.setSelectionRange(s + ins.length, s + ins.length); } catch (e) {}
        inp.focus(); inp.dispatchEvent(new Event('input'));
      });
      pad.appendChild(b);
    });
    return pad;
  }
  function numericOnly(q) { return (q.rep || []).every(function (r) { return /^[-−+]?[\d\s,./]+$/.test(r); }); }

  /* ── Démarrage d'une activité ───────────────────────────────────── */
  function start(act) {
    stopTimer();
    var d = DATA[act];
    if (!d) { $body.innerHTML = '<p class="qz-msg">Cette activité n\'est pas encore prête.</p>'; return; }
    if (act === 'trous') return startTrous(d);
    return startQuiz(act, d);
  }

  function startQuiz(act, d) {
    var qs = draw(act, d.questions, d.servir || 10), i = 0, answers = [], t0 = Date.now(), dureeMax = d.duree || 0,
        doneInTime = null, chosen = null, isFinal = act === 'qcm_final', isFlash = act === 'flash';
    run = { act: act };
    if (isFlash && dureeMax) {
      $timer.hidden = false; $timer.classList.remove('is-over');
      var tick = function () {
        var left = dureeMax - (Date.now() - t0) / 1000;
        if (left <= 0) {
          if (doneInTime === null) { doneInTime = answers.length; say('Temps écoulé. Tu peux finir les questions.'); $timer.classList.add('is-over'); }
          $timer.textContent = 'Temps écoulé'; $timer.setAttribute('aria-label', 'Temps écoulé');
        } else { $timer.textContent = fmtTime(left); $timer.setAttribute('aria-label', 'Temps restant ' + fmtTime(left)); }
      };
      tick(); timerId = setInterval(tick, 1000);
    }
    function show() {
      var q = qs[i];
      chosen = null;
      setProgress(i, qs.length, 'Question ' + (i + 1) + ' / ' + qs.length);
      $body.innerHTML = ''; $foot.innerHTML = '';
      var qn = el('div', 'qz-q', (q.chap ? '<span class="qz-chap">Chapitre ' + esc(q.chap) + '</span>' : '') + md(q.q)); qn.id = 'qz-q';
      $body.appendChild(qn);
      var fb = el('div', 'qz-fb'); fb.hidden = true;
      if (q.type === 'saisie') {
        var wrap = el('div', 'qz-field');
        var inp = el('input', 'qz-input'); inp.type = 'text'; inp.autocomplete = 'off'; inp.spellcheck = false;
        inp.setAttribute('autocapitalize', 'off'); inp.setAttribute('autocorrect', 'off');
        inp.setAttribute('aria-labelledby', 'qz-q'); inp.setAttribute('enterkeyhint', 'done');
        inp.inputMode = numericOnly(q) ? 'decimal' : 'text';
        inp.placeholder = 'Ta réponse';
        wrap.appendChild(mathPad(function () { return inp; }));
        wrap.appendChild(inp);
        $body.appendChild(wrap); $body.appendChild(fb);
        var hint = el('p', 'qz-hint', 'Valide avec <kbd>Entrée</kbd>.'); $body.appendChild(hint);
        var validate = function () {
          if (!inp.value.trim()) { inp.focus(); say('Écris une réponse, ou touche « Je ne sais pas ».'); inp.classList.add('is-empty'); return; }
          finishQ(accept(inp.value, q), inp.value, fb, inp);
        };
        inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); if (!inp.disabled) validate(); } });
        inp.addEventListener('input', function () { inp.classList.remove('is-empty'); });
        $foot.appendChild(btn('Je ne sais pas', 'btn btn--ghost btn--sm qz-skip', function () { finishQ(false, '', fb, inp); }));
        $foot.appendChild(btn('Valider', 'btn btn--sm qz-main', validate));
        setTimeout(function () { inp.focus({ preventScroll: true }); }, 30);
      } else {
        var list = el('div', 'qz-choices'); list.setAttribute('role', 'group'); list.setAttribute('aria-labelledby', 'qz-q');
        var ch = shuffledChoices(q);
        ch.forEach(function (c, k) {
          var b = el('button', 'qz-choice', '<span class="qz-letter" aria-hidden="true">' + 'ABCDEF'[k] + '</span><span class="qz-ct">' + md(c.t) + '</span>');
          b.type = 'button';
          if (isFinal) b.setAttribute('aria-pressed', 'false');
          b.addEventListener('click', function () {
            if (b.disabled) return;
            if (isFinal) {
              chosen = c;
              list.querySelectorAll('.qz-choice').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
              main.disabled = false;
            } else {
              list.querySelectorAll('.qz-choice').forEach(function (o, kk) {
                o.disabled = true;
                if (ch[kk].ok) o.classList.add('is-ok');
              });
              if (!c.ok) b.classList.add('is-ko');
              finishQ(c.ok, c.t, fb, null);
            }
          });
          list.appendChild(b);
        });
        $body.appendChild(list); $body.appendChild(fb);
        var main;
        if (isFinal) {
          main = btn(i === qs.length - 1 ? 'Valider et voir la correction' : 'Valider', 'btn btn--sm qz-main', function () {
            if (!chosen) return;
            answers.push({ q: q, ok: chosen.ok, rep: chosen.t });
            i++; if (i < qs.length) { show(); scrollTop(); } else end();
          });
          main.disabled = true;
          $foot.appendChild(el('p', 'qz-foot-note', 'Correction détaillée à la fin.'));
          $foot.appendChild(main);
        }
        setTimeout(function () { var f = list.querySelector('.qz-choice'); if (f) f.focus({ preventScroll: true }); }, 30);
      }
    }
    function finishQ(ok, rep, fb, inp) {
      var q = qs[i];
      answers.push({ q: q, ok: ok, rep: rep });
      if (inp) { inp.disabled = true; inp.classList.add(ok ? 'is-ok' : 'is-ko'); var pd = $body.querySelector('.qz-pad'); if (pd) pd.hidden = true; }
      var good = q.type === 'saisie' ? (q.aff || q.rep[0]) : q.choix[q.bonne];
      fb.hidden = false; fb.className = 'qz-fb ' + (ok ? 'qz-fb--ok' : 'qz-fb--ko');
      fb.innerHTML = '<p class="qz-fb-t">' + (ok ? 'Bonne réponse' + NB + '!' : (rep ? 'Pas tout à fait.' : 'Voici la réponse.') + ' Réponse attendue' + NB + ': ' + md(good)) + '</p>' +
        (q.expl ? '<p class="qz-fb-e">' + md(q.expl) + '</p>' : '');
      say(ok ? 'Bonne réponse.' : 'Réponse incorrecte.');
      $foot.innerHTML = '';
      var last = i === qs.length - 1;
      var nx = btn(last ? 'Voir le bilan' : 'Question suivante', 'btn btn--sm qz-main', function () { i++; if (i < qs.length) { show(); scrollTop(); } else end(); });
      $foot.appendChild(nx);
      setProgress(i + 1, qs.length, 'Question ' + (i + 1) + ' / ' + qs.length);
      setTimeout(function () { nx.focus({ preventScroll: true }); if (fb.scrollIntoView) fb.scrollIntoView({ block: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' }); }, 30);
    }
    run.onKey = function (e) {
      if (e.target && e.target.tagName === 'INPUT') return;
      var n = '1234'.indexOf(e.key); if (n < 0) n = 'abcd'.indexOf((e.key || '').toLowerCase());
      if (n >= 0 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        var cs = $body.querySelectorAll('.qz-choice'); if (cs[n] && !cs[n].disabled) { e.preventDefault(); cs[n].click(); cs[n].focus(); }
      }
    };
    function end() {
      stopTimer();
      var el0 = (Date.now() - t0) / 1000, score = answers.filter(function (a) { return a.ok; }).length, n = qs.length;
      var rec = record(act, score, n);
      var extra = '';
      if (isFlash && dureeMax) {
        if (doneInTime === null) extra = 'Terminé en ' + dur(el0) + ', avant la fin des 5' + NB + 'minutes.';
        else {
          var okIn = answers.slice(0, doneInTime).filter(function (a) { return a.ok; }).length;
          extra = 'En 5' + NB + 'min, tu as répondu à ' + doneInTime + ' question' + (doneInTime > 1 ? 's' : '') + ' sur ' + n + ' (' + okIn + ' juste' + (okIn > 1 ? 's' : '') + '). Tu as tout fini en ' + dur(el0) + '.';
        }
      }
      var verified = false, passMsg = '';
      if (isFinal) {
        var seuil = DATA.qcm_final.seuil || Math.ceil(0.75 * n);
        if (score >= seuil) { verified = markVerified(); passMsg = 'QCM final réussi (seuil' + NB + ': ' + seuil + '/' + n + ').' + (verified ? ' L\'étape «' + NB + 'J\'ai vérifié mes acquis' + NB + '» est cochée dans Ma progression.' : ''); }
        else passMsg = 'Seuil de réussite' + NB + ': ' + seuil + '/' + n + '. Relis les corrections ci-dessous, revois le cours, puis retente ta chance.';
      }
      bilan(act, score, n, extra, passMsg, rec, isFinal ? answers : answers.filter(function (a) { return !a.ok; }), isFinal, isFinal && score >= (DATA.qcm_final.seuil || 9));
    }
    show();
  }

  function startTrous(d) {
    var texts = draw('trous', d.textes, d.servir || 4), i = 0, good = 0, total = 0, wrong = [];
    run = { act: 'trous' };
    function show() {
      var T = texts[i];
      setProgress(i, texts.length, 'Texte ' + (i + 1) + ' / ' + texts.length);
      $body.innerHTML = ''; $foot.innerHTML = '';
      $body.appendChild(el('h3', 'qz-ttitle', md(T.titre || 'Complète')));
      var holes = [], html = '', src = String(T.texte), inMath = false, mathBuf = '', txtBuf = '';
      function flushTxt() { if (txtBuf) { html += esc(txtBuf).replace(/\n/g, '<br>'); txtBuf = ''; } }
      function flushMath() { if (mathBuf.trim()) html += tex(mathBuf); mathBuf = ''; }
      var k = 0;
      while (k < src.length) {
        if (src.substr(k, 2) === '{{') {
          var e = src.indexOf('}}', k);
          var reps = src.slice(k + 2, e).split('|');
          if (inMath) flushMath(); else flushTxt();
          var n = holes.length;
          holes.push({ rep: reps, math: inMath });
          var w = Math.max(3, Math.min(16, reps[0].replace(/\\[a-z]+/g, 'x').length + 1));
          html += '<span class="qz-hole"><input class="qz-input qz-input--hole" type="text" data-h="' + n + '" style="--w:' + w + 'ch" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Trou ' + (n + 1) + '"></span>';
          k = e + 2; continue;
        }
        var c = src[k];
        if (c === '$') { if (inMath) { flushMath(); inMath = false; } else { flushTxt(); inMath = true; } k++; continue; }
        if (inMath) mathBuf += c; else txtBuf += c;
        k++;
      }
      if (inMath) flushMath(); else flushTxt();
      var lastInp = null;
      var pad = mathPad(function () { return lastInp; });
      $body.appendChild(pad);
      var p = el('div', 'qz-ttext', html); $body.appendChild(p);
      var inputs = p.querySelectorAll('input');
      inputs.forEach(function (inp, n) {
        inp.addEventListener('focus', function () { lastInp = inp; });
        inp.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { e.preventDefault(); if (inputs[n + 1]) inputs[n + 1].focus(); else check(); }
        });
      });
      lastInp = inputs[0];
      var fb = el('div', 'qz-fb'); fb.hidden = true; $body.appendChild(fb);
      $body.appendChild(el('p', 'qz-hint', '<kbd>Entrée</kbd> passe au trou suivant.'));
      var checked = false;
      function check() {
        if (checked) return; checked = true;
        var ok = 0;
        inputs.forEach(function (inp, n) {
          var h = holes[n], r = accept(inp.value, { rep: h.rep });
          inp.disabled = true; inp.classList.add(r ? 'is-ok' : 'is-ko');
          if (r) ok++;
          else {
            var s = el('span', 'qz-sol', h.math ? tex(h.rep[0]) : esc(h.rep[0]));
            s.setAttribute('aria-label', 'Réponse attendue : ' + h.rep[0]);
            inp.parentNode.appendChild(s);
          }
        });
        good += ok; total += inputs.length; pad.hidden = true;
        if (ok < inputs.length) wrong.push({ T: T, ok: ok, n: inputs.length });
        fb.hidden = false; fb.className = 'qz-fb ' + (ok === inputs.length ? 'qz-fb--ok' : 'qz-fb--ko');
        fb.innerHTML = '<p class="qz-fb-t">' + ok + ' trou' + (ok > 1 ? 's' : '') + ' juste' + (ok > 1 ? 's' : '') + ' sur ' + inputs.length + (ok === inputs.length ? NB + '!' : '. Les réponses attendues sont affichées en vert.') + '</p>' +
          (T.expl ? '<p class="qz-fb-e">' + md(T.expl) + '</p>' : '');
        say(ok + ' sur ' + inputs.length);
        $foot.innerHTML = '';
        var last = i === texts.length - 1;
        var nx = btn(last ? 'Voir le bilan' : 'Texte suivant', 'btn btn--sm qz-main', function () { i++; if (i < texts.length) { show(); scrollTop(); } else end(); });
        $foot.appendChild(nx);
        setProgress(i + 1, texts.length, 'Texte ' + (i + 1) + ' / ' + texts.length);
        setTimeout(function () { nx.focus({ preventScroll: true }); if (fb.scrollIntoView) fb.scrollIntoView({ block: 'nearest' }); }, 30);
      }
      $foot.appendChild(btn('Vérifier', 'btn btn--sm qz-main', check));
      setTimeout(function () { if (inputs[0]) inputs[0].focus({ preventScroll: true }); }, 30);
    }
    function end() {
      var rec = record('trous', good, total);
      bilan('trous', good, total, 'Sur ' + texts.length + ' textes.', '', rec, wrong.map(function (w) { return { T: w.T, ok: false, info: w.ok + '/' + w.n }; }), false, false);
    }
    show();
  }

  function bilan(act, score, n, extra, passMsg, record, review, isFinal, passed) {
    setProgress(n, n, 'Bilan');
    var r = n ? score / n : 0;
    var msg = r >= .9 ? 'Excellent' + NB + '! Tu maîtrises ces notions.' : r >= .7 ? 'Très bien' + NB + '! Encore un petit effort pour tout réussir.' :
      r >= .5 ? 'C\'est en bonne voie. Regarde les corrections et recommence.' : 'Courage' + NB + ': relis le cours, puis recommence. Chaque essai te fait progresser.';
    $body.innerHTML = ''; $foot.innerHTML = '';
    var head = el('div', 'qz-score' + (isFinal ? (passed ? ' is-pass' : ' is-fail') : ''),
      '<p class="qz-score-n"><b>' + score + '</b><span>/' + n + '</span></p><div><p class="qz-score-m">' + esc(msg) + '</p>' +
      (record ? '<p class="qz-record">Nouveau meilleur score' + NB + '!</p>' : '') +
      (extra ? '<p class="qz-score-x">' + esc(extra) + '</p>' : '') +
      (passMsg ? '<p class="qz-score-x qz-pass">' + esc(passMsg) + '</p>' : '') + '</div>');
    $body.appendChild(head);
    if (review.length) {
      $body.appendChild(el('h3', 'qz-rev-t', isFinal ? 'Correction détaillée' : (act === 'trous' ? 'Textes à revoir' : 'Tes erreurs, corrigées')));
      var ol = el('ol', 'qz-rev');
      review.forEach(function (a) {
        var li = el('li', a.ok ? 'is-ok' : 'is-ko');
        if (a.T) {
          li.innerHTML = '<p class="qz-rev-q"><b>' + md(a.T.titre || '') + '</b> — ' + esc(a.info) + ' juste(s)</p><p class="qz-rev-a">' + md(a.T.texte.replace(/\{\{([^|}]*)[^}]*\}\}/g, '⟦$1⟧')) + '</p>' + (a.T.expl ? '<p class="qz-rev-e">' + md(a.T.expl) + '</p>' : '');
          li.querySelectorAll('.qz-rev-a').forEach(function (p) { p.innerHTML = p.innerHTML.replace(/⟦/g, '<mark>').replace(/⟧/g, '</mark>'); });
        } else {
          var q = a.q, good = q.type === 'saisie' ? (q.aff || q.rep[0]) : q.choix[q.bonne];
          li.innerHTML = '<p class="qz-rev-q">' + md(q.q) + '</p>' +
            '<p class="qz-rev-a"><span class="qz-tag ' + (a.ok ? 'ok' : 'ko') + '">' + (a.ok ? 'Juste' : 'À revoir') + '</span> ' +
            (a.ok ? 'Ta réponse' + NB + ': ' + md(good) : (a.rep ? 'Ta réponse' + NB + ': <s>' + (q.type === 'saisie' ? esc(a.rep) : md(a.rep)) + '</s> · ' : '') + 'Réponse attendue' + NB + ': <b>' + md(good) + '</b>') + '</p>' +
            (q.expl ? '<p class="qz-rev-e">' + md(q.expl) + '</p>' : '');
        }
        ol.appendChild(li);
      });
      $body.appendChild(ol);
    } else {
      $body.appendChild(el('p', 'qz-msg qz-msg--ok', 'Aucune erreur' + NB + ': bravo' + NB + '!'));
    }
    $foot.appendChild(btn('Fermer', 'btn btn--ghost btn--sm', close));
    var again = btn('Recommencer (nouveau tirage)', 'btn btn--sm qz-main', function () { scrollTop(); start(act); });
    $foot.appendChild(again);
    say('Bilan : ' + score + ' sur ' + n);
    scrollTop();
    setTimeout(function () { again.focus({ preventScroll: true }); }, 30);
  }

  /* ── Branchement des cartes ─────────────────────────────────────── */
  doc.querySelectorAll('[data-qz-open]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); open(b.getAttribute('data-qz-open'), b); });
  });
  paintBest();
  /* KaTeX : chargé dès maintenant s'il manque, pour que la première activité s'ouvre sans attente. */
  if ('requestIdleCallback' in window) window.requestIdleCallback(needKatex); else setTimeout(needKatex, 300);
  /* N'affiche que les activités présentes dans le fichier (les autres cartes sont masquées). */
  loadData().then(function (d) {
    var any = false;
    doc.querySelectorAll('[data-qz-open]').forEach(function (b) {
      var a = b.getAttribute('data-qz-open'), ok = !!(d[a] && ((d[a].questions && d[a].questions.length) || (d[a].textes && d[a].textes.length)));
      var item = b.closest('[data-qz-item]') || b;
      item.hidden = !ok; if (ok) any = true;
    });
    doc.querySelectorAll('[data-qz-block]').forEach(function (x) { x.hidden = !any; });
    if (LIST.length) {
      var n = doc.querySelector('[data-qz-nb]');
      if (n) n.textContent = d.flash.questions.length + ' questions';
    }
  }).catch(function () {});
  window.addEventListener('storage', function (e) { if (e.key === SKEY) paintBest(); });
})();
