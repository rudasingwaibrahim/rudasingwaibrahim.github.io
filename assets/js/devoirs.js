/* ═══════════════════════════════════════════════════════════════════
   Σ Sigma — Devoirs maison en ligne
   Page /devoirs/ (liste) et page d'un devoir (#dv-app, voir _includes/devoir.html).
   - Mode réel : sujet personnalisé et correction demandés au serveur Google Apps Script
     du professeur (data-url) ; le corrigé ne vient jamais dans le navigateur.
   - Mode démo (data-url vide) : moteur SigmaMoteur inclus dans la page, rien n'est envoyé.
   - Brouillon gardé sur l'appareil (localStorage « sigma-devoir-v1:… ») : sujet, réponses,
     temps de travail, envoi en attente. Le réseau peut couper : rien n'est perdu.
   Réutilise assets/js/quiz.js (window.SigmaQuiz) : rendu KaTeX, clavier mathématique.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var doc = document, NB = ' ';
  var LS_ID = 'sigma-devoirs-ident', LS_PREF = 'sigma-devoir-v1:';
  var NOM_RE = /^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$/;

  /* ── Outils ─────────────────────────────────────────────────────── */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function SQ() { return window.SigmaQuiz || null; }
  function md(s) { var q = SQ(); return q ? q.md(s) : esc(String(s == null ? '' : s).replace(/\$/g, '')).replace(/\n/g, '<br>'); }
  function el(tag, cls, html) { var e = doc.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function load(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function normIdent(s) {
    return String(s == null ? '' : s).replace(/[’`ʼ]/g, "'").normalize('NFD').replace(/[̀-ͯ]/g, '')
      .toLowerCase().replace(/[^a-z' -]/g, '').replace(/[\s-]+/g, ' ').trim();
  }
  function propre(s) { return String(s == null ? '' : s).replace(/[’`ʼ]/g, "'").replace(/\s+/g, ' ').trim(); }
  function nomValide(s) { return !!s && s.length <= 40 && NOM_RE.test(s) && /[A-Za-zÀ-ÖØ-öø-ÿ]/.test(s); }
  function cle(id, ident, demo) { return LS_PREF + (demo ? 'demo:' : '') + id + ':' + normIdent(ident.nom) + '|' + normIdent(ident.prenom) + '|' + ident.classe; }
  function uid() {
    if (window.crypto && crypto.getRandomValues) { var a = new Uint32Array(3); crypto.getRandomValues(a); return Array.prototype.map.call(a, function (x) { return x.toString(36); }).join('-'); }
    return Date.now().toString(36) + '-' + Math.random().toString(36).slice(2);
  }
  function heure(ts) { var d = new Date(ts); return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); }
  function dateLongue(iso) {
    if (!iso) return '';
    var d = new Date(iso); if (isNaN(d)) return '';
    var j = d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
    return j + ' à ' + d.getHours() + NB + 'h' + NB + ('0' + d.getMinutes()).slice(-2);
  }
  function fr(n) { return String(n).replace('.', ','); }
  function api(url, payload, ms) {
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var t = setTimeout(function () { if (ctrl) ctrl.abort(); }, ms || 30000);
    var opt = payload
      ? { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload), redirect: 'follow', credentials: 'omit' }
      : { method: 'GET', redirect: 'follow', credentials: 'omit' };
    if (ctrl) opt.signal = ctrl.signal;
    var u = payload ? url : url + (url.indexOf('?') < 0 ? '?' : '&') + 'action=liste';
    return fetch(u, opt).then(function (r) {
      clearTimeout(t);
      if (!r.ok) throw { reseau: true, status: r.status };
      return r.json().catch(function () { throw { reseau: true, illisible: true }; });
    }, function () { clearTimeout(t); throw { reseau: true }; });
  }

  /* ═══ Page /devoirs/ : statut des devoirs ══════════════════════════ */
  var liste = doc.querySelector('[data-dv-liste]');
  if (liste) {
    var url = liste.getAttribute('data-url') || '', ident = load(LS_ID);
    var cards = liste.querySelectorAll('[data-dv-id]');
    var local = function (card) {
      if (!ident) return '';
      var id = card.getAttribute('data-dv-id'), d = load(cle(id, ident, !url));
      if (!d) return '';
      if (d.resultat) return ' <span class="chip chip--green">Rendu · ' + fr(d.resultat.note) + '/20</span>';
      if (d.sujet) return ' <span class="chip chip--gold">Brouillon sur cet appareil</span>';
      return '';
    };
    cards.forEach(function (c) { var s = c.querySelector('[data-dv-statut]'); if (s) s.insertAdjacentHTML('beforeend', local(c)); });
    if (url) {
      api(url, null, 20000).then(function (r) {
        var by = {};
        (r.devoirs || []).forEach(function (d) { by[d.id] = d; });
        cards.forEach(function (c) {
          var d = by[c.getAttribute('data-dv-id')], s = c.querySelector('[data-dv-statut]');
          if (!s) return;
          var t = !d ? '<span class="chip chip--off">Pas encore ouvert</span>'
            : d.ouvert ? '<span class="chip chip--green">Ouvert</span>' + (d.dateLimite ? ' <span class="dv-lim">à rendre avant le ' + esc(dateLongue(d.dateLimite)) + '</span>' : '')
            : '<span class="chip chip--off">Fermé</span>';
          s.innerHTML = t + local(c);
        });
      }).catch(function () {
        cards.forEach(function (c) { var s = c.querySelector('[data-dv-statut]'); if (s) s.innerHTML = '<span class="chip chip--off">Statut indisponible (connexion)</span>' + local(c); });
      });
    }
  }

  /* ═══ Page d'un devoir ═════════════════════════════════════════════ */
  var app = doc.getElementById('dv-app');
  if (!app) return;
  var C = {
    id: app.getAttribute('data-devoir'), url: app.getAttribute('data-url') || '', jeton: app.getAttribute('data-jeton') || '',
    classes: (app.getAttribute('data-classes') || '').split('|').filter(Boolean), titre: app.getAttribute('data-titre') || 'Devoir',
    retour: app.getAttribute('data-retour') || '/devoirs/', demoDispo: app.hasAttribute('data-demo-dispo') && !!window.SigmaMoteur
  };
  var demo = false, ident = null, D = null, K = '', saveTimer = null, lastAct = Date.now(), actTimer = null;

  function persist() { if (D && K) { D.maj = Date.now(); save(K, D); } }
  function show(html) { app.innerHTML = ''; if (typeof html === 'string') app.innerHTML = html; else app.appendChild(html); }
  function top() { var r = app.getBoundingClientRect(); if (r.top < 0 || r.top > window.innerHeight) window.scrollTo({ top: Math.max(0, window.scrollY + r.top - 90), behavior: 'auto' }); }
  function focusFirst(sel) { var f = app.querySelector(sel); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 30); }
  function demoBanner() { return demo ? '<p class="dv-demo-banner"><b>Mode démo</b> · le devoir est corrigé sur cet appareil et rien n\'est envoyé au professeur.</p>' : ''; }
  function katex() { var q = SQ(); return q && q.needKatex ? q.needKatex() : Promise.resolve(); }

  /* ── Écran « bientôt disponible » (serveur non installé) ────────── */
  function ecranIndispo() {
    stopActif();
    show('<section class="dv-panel dv-indispo" aria-labelledby="dv-t">' +
      '<span class="dv-sigma" aria-hidden="true">Σ</span>' +
      '<h2 id="dv-t">Les devoirs en ligne seront bientôt disponibles</h2>' +
      '<p>Ton professeur t\'indiquera quand ce devoir sera ouvert. Tu pourras alors le faire ici, sur ton téléphone ou un ordinateur.</p>' +
      (C.demoDispo ? '<p class="dv-muted">En attendant, le <b>mode démo</b> montre le devoir complet, corrigé sur cet appareil. Rien n\'est envoyé.</p>' +
        '<p><button class="btn" type="button" data-demo>Essayer en mode démo</button></p>' : '') +
      '<p><a href="' + esc(C.retour) + '">Retour aux devoirs</a></p></section>');
    var b = app.querySelector('[data-demo]');
    if (b) b.addEventListener('click', function () { demo = true; ecranIdentite(); });
  }

  /* ── Écran d'identité ───────────────────────────────────────────── */
  function ecranIdentite(msg) {
    stopActif();
    var mem = load(LS_ID) || {}, cls = C.classes;
    var f = el('form', 'dv-panel dv-ident');
    f.setAttribute('novalidate', ''); f.setAttribute('aria-labelledby', 'dv-t');
    f.innerHTML = demoBanner() +
      '<h2 id="dv-t">Qui fait ce devoir&nbsp;?</h2>' +
      '<p class="dv-muted">Écris ton nom et ton prénom comme sur PRONOTE. Ton sujet est personnel&nbsp;: tes camarades ont les mêmes questions, avec d\'autres nombres.</p>' +
      (msg ? '<p class="dv-alert dv-alert--ko" role="alert">' + esc(msg) + '</p>' : '') +
      '<div class="dv-fields">' +
        '<p class="dv-f"><label for="dv-nom">Nom</label><input id="dv-nom" name="nom" type="text" autocomplete="family-name" autocapitalize="characters" spellcheck="false" maxlength="40" required aria-describedby="dv-e-nom"><span class="dv-err" id="dv-e-nom"></span></p>' +
        '<p class="dv-f"><label for="dv-prenom">Prénom</label><input id="dv-prenom" name="prenom" type="text" autocomplete="given-name" autocapitalize="words" spellcheck="false" maxlength="40" required aria-describedby="dv-e-prenom"><span class="dv-err" id="dv-e-prenom"></span></p>' +
      '</div>' +
      '<fieldset class="dv-classes" aria-describedby="dv-e-classe"><legend>Classe</legend>' +
        cls.map(function (c, i) { return '<label class="dv-classe"><input type="radio" name="classe" value="' + esc(c) + '"' + (mem.classe === c ? ' checked' : '') + '><span>' + esc(c) + '</span></label>'; }).join('') +
        '<span class="dv-err" id="dv-e-classe"></span></fieldset>' +
      '<p class="dv-rgpd">Tes nom, prénom, classe, réponses et note sont transmis uniquement à ton professeur et conservés dans son espace Google pendant l\'année scolaire. <a href="/mentions-legales/#ml-devoirs">En savoir plus</a>.</p>' +
      '<div class="dv-actions"><button class="btn" type="submit">Commencer le devoir</button>' +
      (demo ? '<button class="btn btn--ghost btn--sm" type="button" data-quit-demo>Quitter le mode démo</button>' : '') + '</div>';
    show(f);
    f.nom.value = mem.nom || ''; f.prenom.value = mem.prenom || '';
    var q = f.querySelector('[data-quit-demo]');
    if (q) q.addEventListener('click', function () { demo = false; ecranIndispo(); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var nom = propre(f.nom.value), prenom = propre(f.prenom.value), c = f.querySelector('input[name="classe"]:checked'), ok = true;
      [['nom', nom, 'Écris ton nom (lettres, espaces, tirets ou apostrophes).'], ['prenom', prenom, 'Écris ton prénom (lettres, espaces, tirets ou apostrophes).']].forEach(function (x) {
        var bad = !nomValide(x[1]), inp = f[x[0]];
        inp.setAttribute('aria-invalid', bad ? 'true' : 'false');
        f.querySelector('#dv-e-' + x[0]).textContent = bad ? x[2] : '';
        if (bad && ok) { inp.focus(); ok = false; }
      });
      f.querySelector('#dv-e-classe').textContent = c ? '' : 'Choisis ta classe.';
      if (!c) { if (ok) f.querySelector('input[name="classe"]').focus(); ok = false; }
      if (!ok) return;
      ident = { nom: nom, prenom: prenom, classe: c.value };
      save(LS_ID, ident);
      ouvrir();
    });
    if (!mem.nom) focusFirst('#dv-nom');
  }

  /* ── Ouverture : brouillon, résultat déjà obtenu, ou nouveau sujet ── */
  function ouvrir() {
    K = cle(C.id, ident, demo);
    D = load(K);
    if (D && D.v === 1 && D.envoiEnAttente && D.sujet) return envoyer();
    if (D && D.v === 1 && D.resultat) return ecranResultat();
    if (D && D.v === 1 && D.sujet) return ecranDevoir(true);
    chargerSujet(1);
  }

  function nouveauBrouillon(sujet, info) {
    D = { v: 1, ident: ident, demo: demo, essai: info.essai, essaisMax: info.essaisMax, dateLimite: info.dateLimite || null,
      sujet: sujet, reponses: {}, actif: 0, idRendu: uid(), debut: new Date().toISOString(), resultat: null, envoiEnAttente: false };
    persist();
  }

  function chargerSujet(essaiDemo) {
    stopActif();
    show('<section class="dv-panel dv-wait" aria-live="polite"><span class="dv-spin" aria-hidden="true"></span><p>Préparation de ton sujet personnel…</p></section>');
    if (demo) {
      var s = window.SigmaMoteur.sujet(C.id, ident, essaiDemo, 'demo');
      nouveauBrouillon(s, { essai: essaiDemo, essaisMax: 2, dateLimite: null });
      return katex().then(function () { ecranDevoir(false); });
    }
    api(C.url, { action: 'sujet', devoir: C.id, jeton: C.jeton, nom: ident.nom, prenom: ident.prenom, classe: ident.classe }, 40000)
      .then(function (r) {
        if (!r || !r.ok) return ecranErreur(r || {});
        nouveauBrouillon(r.sujet, r);
        return katex().then(function () { ecranDevoir(false); });
      })
      .catch(function () {
        ecranErreur({ code: 'RESEAU', message: 'Impossible de joindre le serveur des devoirs. Vérifie ta connexion (données mobiles ou Wi-Fi), puis réessaie.' }, function () { chargerSujet(essaiDemo); });
      });
  }

  /* ── Écran du devoir ────────────────────────────────────────────── */
  function nbRepondues() {
    var n = 0;
    D.sujet.questions.forEach(function (q) { if (repondue(q)) n++; });
    return n;
  }
  function repondue(q) {
    var r = D.reponses[q.id];
    if (q.type === 'qcm') return typeof r === 'number';
    if (q.type === 'trous') return Array.isArray(r) && r.some(function (x) { return x && String(x).trim(); });
    return !!(r && String(r).trim());
  }
  function inputMode(inp, clavier) {
    inp.type = 'text'; inp.autocomplete = 'off'; inp.spellcheck = false;
    inp.setAttribute('autocapitalize', 'off'); inp.setAttribute('autocorrect', 'off'); inp.setAttribute('enterkeyhint', 'next');
    inp.inputMode = clavier === 'nombre' ? 'numeric' : 'text';
  }
  /* Clavier mathématique de quiz.js, complété pour les produits (× et ^) et les trous (+). */
  function pad(getInput, clavier) {
    var q = SQ();
    if (!q || !q.mathPad) return null;
    var p = q.mathPad(getInput);
    var extra = clavier === 'produit' ? [['×', '×', 'fois'], ['^', '^', 'puissance']] : clavier === 'texte' ? [['+', '+', 'plus']] : [];
    if (extra.length) {
      extra.forEach(function (k) {
        var b = el('button', 'qz-key', esc(k[0])); b.type = 'button'; b.setAttribute('aria-label', k[2]);
        b.addEventListener('pointerdown', function (e) { e.preventDefault(); });
        b.addEventListener('click', function () {
          var inp = getInput(); if (!inp || inp.disabled) return;
          var s = inp.selectionStart == null ? inp.value.length : inp.selectionStart, t = inp.selectionEnd == null ? s : inp.selectionEnd;
          inp.value = inp.value.slice(0, s) + k[1] + inp.value.slice(t);
          try { inp.setSelectionRange(s + 1, s + 1); } catch (e) {}
          inp.focus(); inp.dispatchEvent(new Event('input'));
        });
        p.appendChild(b);
      });
    }
    return p;
  }

  function ecranDevoir(reprise) {
    var S = D.sujet, wrap = el('div', 'dv-devoir');
    var restant = D.essaisMax ? D.essaisMax - D.essai + 1 : null;
    wrap.innerHTML = demoBanner() +
      '<section class="dv-head" aria-labelledby="dv-t">' +
        '<div class="dv-head-t"><p class="eyebrow">' + esc(S.chapitre || '') + '</p><h2 id="dv-t">' + esc(S.titre || C.titre) + '</h2>' +
        '<p class="dv-who"><b>' + esc(ident.prenom) + ' ' + esc(ident.nom.toUpperCase()) + '</b> · ' + esc(ident.classe) + (D.essaisMax ? ' · essai ' + D.essai + ' sur ' + D.essaisMax : '') + '</p>' +
        (D.dateLimite ? '<p class="dv-lim">À rendre avant le <b>' + esc(dateLongue(D.dateLimite)) + '</b></p>' : '') + '</div>' +
        '<button class="btn btn--ghost btn--sm" type="button" data-pasmoi>Ce n\'est pas moi</button>' +
      '</section>' +
      (reprise ? '<p class="dv-alert dv-alert--ok" role="status">Brouillon retrouvé sur cet appareil&nbsp;: tu reprends là où tu t\'étais arrêté.</p>' : '') +
      '<p class="dv-consigne">' + S.questions.length + ' questions, ' + S.total + ' points, de la plus facile à la plus exigeante. Tes réponses sont enregistrées automatiquement sur cet appareil&nbsp;: tu peux fermer la page et revenir plus tard.' +
        (restant && restant > 1 ? ' Après l\'envoi, tu pourras refaire le devoir avec un nouveau sujet (autres nombres).' : '') + '</p>';
    var ol = el('ol', 'dv-qs');
    var lastNiv = '';
    S.questions.forEach(function (q) {
      if (q.niveauTexte && q.niveau !== lastNiv) { ol.appendChild(el('li', 'dv-niv-sep dv-niv--' + q.niveau, '<span>' + esc(q.niveauTexte) + '</span>')); lastNiv = q.niveau; }
      ol.appendChild(question(q));
    });
    wrap.appendChild(ol);
    var bar = el('div', 'dv-bar');
    bar.innerHTML = '<div class="dv-bar-t"><span class="dv-prog" data-prog></span><span class="dv-save" data-save aria-live="polite"></span></div><button class="btn" type="button" data-rendre>Rendre mon devoir</button>';
    wrap.appendChild(bar);
    show(wrap);
    wrap.querySelector('[data-pasmoi]').addEventListener('click', function () { ecranIdentite(); });
    wrap.querySelector('[data-rendre]').addEventListener('click', confirmer);
    majBarre(D.maj ? 'Brouillon enregistré sur cet appareil à ' + heure(D.maj) : '');
    startActif();
    top();
  }
  function majBarre(msg) {
    var p = app.querySelector('[data-prog]'), s = app.querySelector('[data-save]');
    if (p) p.textContent = nbRepondues() + ' / ' + D.sujet.questions.length + ' réponses';
    if (s && msg != null) s.textContent = msg;
  }
  function modifie() {
    lastAct = Date.now();
    majBarre(null);
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      persist();
      majBarre('Brouillon enregistré sur cet appareil à ' + heure(Date.now()));
    }, 350);
  }

  function question(q) {
    var li = el('li', 'dv-q'); li.id = 'dv-' + q.id;
    var qid = 'dv-qt-' + q.id;
    li.innerHTML = '<div class="dv-q-h"><span class="dv-num" aria-hidden="true">' + q.numero + '</span><h3 id="' + qid + '"><span class="sr-only">Question ' + q.numero + ' : </span>' + esc(q.titre) + '</h3><span class="dv-pts">' + q.points + NB + 'pt' + (q.points > 1 ? 's' : '') + '</span></div>' +
      '<div class="dv-q-e qz-q" id="' + qid + '-e">' + md(q.enonce) + '</div>' + (q.aide ? '<p class="dv-aide">' + md(q.aide) + '</p>' : '');
    var r = D.reponses[q.id];
    if (q.type === 'qcm') {
      var list = el('div', 'qz-choices'); list.setAttribute('role', 'group'); list.setAttribute('aria-labelledby', qid + ' ' + qid + '-e');
      q.choix.forEach(function (c, k) {
        var b = el('button', 'qz-choice', '<span class="qz-letter" aria-hidden="true">' + 'ABCDEF'[k] + '</span><span class="qz-ct">' + md(c) + '</span>');
        b.type = 'button'; b.setAttribute('aria-pressed', r === k ? 'true' : 'false');
        b.addEventListener('click', function () {
          var deja = D.reponses[q.id] === k;
          if (deja) delete D.reponses[q.id]; else D.reponses[q.id] = k;
          list.querySelectorAll('.qz-choice').forEach(function (o, kk) { o.setAttribute('aria-pressed', !deja && kk === k ? 'true' : 'false'); });
          modifie();
        });
        list.appendChild(b);
      });
      li.appendChild(list);
    } else if (q.type === 'saisie') {
      var wrap = el('div', 'qz-field');
      var inp = el('input', 'qz-input'); inputMode(inp, q.clavier);
      inp.setAttribute('aria-labelledby', qid + ' ' + qid + '-e'); inp.placeholder = 'Ta réponse'; inp.maxLength = 120;
      inp.value = typeof r === 'string' ? r : '';
      if (q.clavier !== 'nombre') { var p = pad(function () { return inp; }, q.clavier); if (p) wrap.appendChild(p); }
      wrap.appendChild(inp);
      inp.addEventListener('input', function () { D.reponses[q.id] = inp.value; modifie(); });
      inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); suivant(li); } });
      li.appendChild(wrap);
    } else if (q.type === 'trous') {
      var arr = Array.isArray(r) ? r.slice() : [], parts = String(q.texte).split(/\[\[(\d+)\]\]/), html = '';
      for (var i = 0; i < parts.length; i++) {
        if (i % 2 === 0) html += md(parts[i]);
        else {
          var n = +parts[i];
          html += '<span class="qz-hole"><input class="qz-input qz-input--hole" type="text" data-h="' + n + '" style="--w:7ch" maxlength="60" aria-label="Trou ' + (n + 1) + ' de la question ' + q.numero + '"></span>';
        }
      }
      var lastInp = null;
      var p2 = pad(function () { return lastInp; }, 'texte');
      if (p2) li.appendChild(p2);
      var t = el('div', 'qz-ttext dv-trous', html); li.appendChild(t);
      var inputs = t.querySelectorAll('input');
      inputs.forEach(function (inp2, k) {
        inputMode(inp2, (q.trous && q.trous[k] && q.trous[k].clavier) || 'texte');
        inp2.value = typeof arr[k] === 'string' ? arr[k] : '';
        inp2.addEventListener('focus', function () { lastInp = inp2; });
        inp2.addEventListener('input', function () {
          var cur = Array.isArray(D.reponses[q.id]) ? D.reponses[q.id] : [];
          while (cur.length < inputs.length) cur.push('');
          cur[k] = inp2.value; D.reponses[q.id] = cur; modifie();
        });
        inp2.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); if (inputs[k + 1]) inputs[k + 1].focus(); else suivant(li); } });
      });
      lastInp = inputs[0] || null;
    }
    return li;
  }
  function suivant(li) {
    var n = li.nextElementSibling;
    while (n && !n.classList.contains('dv-q')) n = n.nextElementSibling;
    var f = n ? n.querySelector('input, .qz-choice') : app.querySelector('[data-rendre]');
    if (f) { f.focus({ preventScroll: true }); if (f.scrollIntoView) f.scrollIntoView({ block: 'center' }); }
  }

  /* Temps de travail : compté par tranches de 15 s quand la page est visible et que l'élève a agi depuis moins de 2 min. */
  function startActif() {
    stopActif();
    lastAct = Date.now();
    actTimer = setInterval(function () {
      if (!D || doc.hidden || Date.now() - lastAct > 120000) return;
      D.actif = (D.actif || 0) + 15; persist();
    }, 15000);
  }
  function stopActif() { if (actTimer) { clearInterval(actTimer); actTimer = null; } }
  ['pointerdown', 'keydown', 'scroll'].forEach(function (t) { doc.addEventListener(t, function () { lastAct = Date.now(); }, { passive: true }); });

  /* ── Confirmation ───────────────────────────────────────────────── */
  function confirmer() {
    clearTimeout(saveTimer); persist();
    var manq = D.sujet.questions.filter(function (q) { return !repondue(q); }).map(function (q) { return q.numero; });
    var opener = doc.activeElement;
    var m = el('div', 'dv-modal');
    m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-labelledby', 'dv-m-t'); m.setAttribute('aria-describedby', 'dv-m-d');
    var restants = D.essaisMax - D.essai;
    m.innerHTML = '<div class="dv-modal-box"><h2 id="dv-m-t">Rendre ton devoir&nbsp;?</h2><div id="dv-m-d">' +
      '<p>Tu as répondu à <b>' + (D.sujet.questions.length - manq.length) + ' question' + (D.sujet.questions.length - manq.length > 1 ? 's' : '') + ' sur ' + D.sujet.questions.length + '</b>.</p>' +
      (manq.length ? '<p class="dv-alert dv-alert--warn">Sans réponse&nbsp;: question' + (manq.length > 1 ? 's ' : ' ') + manq.join(', ') + '. Une question sans réponse rapporte 0 point.</p>' : '') +
      '<p>Après l\'envoi, tu ne pourras plus modifier ces réponses' + (demo ? '' : '&nbsp;; ta note sera transmise au professeur') + '.' +
      (restants > 0 ? ' Il te restera ' + restants + ' essai' + (restants > 1 ? 's' : '') + ', avec un nouveau sujet.' : ' C\'est ton dernier essai.') + '</p></div>' +
      '<div class="dv-actions"><button class="btn btn--ghost" type="button" data-non>Continuer le devoir</button><button class="btn" type="button" data-oui>Oui, je rends mon devoir</button></div></div>';
    doc.body.appendChild(m); doc.body.classList.add('qz-open');
    function fermer(go) {
      m.remove(); doc.body.classList.remove('qz-open');
      if (go) envoyer(); else if (opener && opener.focus) opener.focus();
    }
    m.querySelector('[data-non]').addEventListener('click', function () { fermer(false); });
    m.querySelector('[data-oui]').addEventListener('click', function () { fermer(true); });
    m.addEventListener('click', function (e) { if (e.target === m) fermer(false); });
    m.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); fermer(false); }
      if (e.key === 'Tab') {
        var f = m.querySelectorAll('button'), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && doc.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
    setTimeout(function () { m.querySelector('[data-oui]').focus(); }, 30);
  }

  /* ── Envoi ──────────────────────────────────────────────────────── */
  var envoiEnCours = false;
  function envoyer() {
    stopActif();
    if (envoiEnCours) return;
    if (demo) {
      var c = window.SigmaMoteur.corriger(C.id, ident, D.essai, 'demo', D.reponses);
      var rest = Math.max(0, D.essaisMax - D.essai);
      D.resultat = { note: c.note, sur: c.sur, points: c.points, total: c.total, detail: c.detail, essai: D.essai, essaisMax: D.essaisMax, restants: rest, peutRefaire: rest > 0, date: new Date().toISOString() };
      persist();
      return katex().then(ecranResultat);
    }
    D.envoiEnAttente = true; persist();
    envoiEnCours = true;
    show('<section class="dv-panel dv-wait" aria-live="polite"><span class="dv-spin" aria-hidden="true"></span><p>Envoi de ton devoir au professeur…</p><p class="dv-muted">Ne ferme pas la page. Si le réseau coupe, tes réponses restent sur cet appareil.</p></section>');
    top();
    api(C.url, { action: 'rendre', devoir: C.id, jeton: C.jeton, nom: ident.nom, prenom: ident.prenom, classe: ident.classe,
      essai: D.essai, idRendu: D.idRendu, duree: D.actif || 0, reponses: D.reponses }, 45000)
      .then(function (r) {
        envoiEnCours = false;
        if (!r || !r.ok) {
          if (r && r.code === 'OCCUPE') return ecranEchecEnvoi(r.message);
          D.envoiEnAttente = false; persist();
          return ecranErreur(r || {});
        }
        D.envoiEnAttente = false;
        D.resultat = { note: r.note, sur: r.sur, points: r.points, total: r.total, detail: r.detail, essai: r.essai, essaisMax: r.essaisMax, restants: r.restants, peutRefaire: r.peutRefaire, dateLimite: r.dateLimite, date: new Date().toISOString() };
        persist();
        return katex().then(ecranResultat);
      })
      .catch(function () { envoiEnCours = false; ecranEchecEnvoi(); });
  }
  function ecranEchecEnvoi(msg) {
    show('<section class="dv-panel dv-echec" aria-labelledby="dv-t">' +
      '<h2 id="dv-t">Ton devoir n\'est pas encore envoyé</h2>' +
      '<p class="dv-alert dv-alert--warn" role="alert">' + esc(msg || 'Le réseau ne répond pas pour l\'instant.') + '</p>' +
      '<p>Tes réponses sont <b>bien gardées sur cet appareil</b>. Réessaie dès que tu as du réseau (données mobiles ou Wi-Fi)&nbsp;: l\'envoi repartira aussi tout seul quand la connexion reviendra, tant que cette page reste ouverte.</p>' +
      '<div class="dv-actions"><button class="btn" type="button" data-retry>Réessayer l\'envoi</button><button class="btn btn--ghost" type="button" data-back>Revoir mes réponses</button></div></section>');
    app.querySelector('[data-retry]').addEventListener('click', envoyer);
    app.querySelector('[data-back]').addEventListener('click', function () { D.envoiEnAttente = false; persist(); ecranDevoir(false); });
    focusFirst('[data-retry]');
    top();
  }
  window.addEventListener('online', function () { if (D && D.envoiEnAttente && !envoiEnCours && app.querySelector('.dv-echec')) envoyer(); });

  /* ── Erreurs du serveur ─────────────────────────────────────────── */
  function ecranErreur(r, retry) {
    stopActif();
    var code = r.code || 'SERVEUR', msg = r.message || 'Le serveur des devoirs a rencontré un problème. Réessaie dans quelques minutes.';
    var extra = '', btns = '';
    if (code === 'ESSAIS' && r.meilleureNote != null) extra = '<p>Ta meilleure note à ce devoir&nbsp;: <b>' + fr(r.meilleureNote) + '/20</b>.</p>';
    if (code === 'SUJET_PERIME') btns += '<button class="btn" type="button" data-nouveau>Charger mon sujet à jour</button>';
    if (retry || code === 'SERVEUR' || code === 'OCCUPE') btns += '<button class="btn" type="button" data-retry>Réessayer</button>';
    if (code === 'IDENTITE' || code === 'CLASSE') btns += '<button class="btn" type="button" data-ident>Corriger mon nom ou ma classe</button>';
    show('<section class="dv-panel" aria-labelledby="dv-t"><h2 id="dv-t">' + (code === 'RESEAU' ? 'Pas de connexion' : 'Devoir indisponible') + '</h2>' +
      '<p class="dv-alert dv-alert--ko" role="alert">' + esc(msg) + '</p>' + extra +
      '<div class="dv-actions">' + btns + '<a class="btn btn--ghost" href="' + esc(C.retour) + '">Retour aux devoirs</a></div></section>');
    var b;
    if ((b = app.querySelector('[data-retry]'))) b.addEventListener('click', retry || function () { ouvrir(); });
    if ((b = app.querySelector('[data-nouveau]'))) b.addEventListener('click', function () { try { localStorage.removeItem(K); } catch (e) {} D = null; chargerSujet(1); });
    if ((b = app.querySelector('[data-ident]'))) b.addEventListener('click', function () { ecranIdentite(); });
    focusFirst('.dv-actions .btn');
    top();
  }

  /* ── Résultat et correction ─────────────────────────────────────── */
  function reponseEleve(q, r) {
    if (q.type === 'qcm') return typeof r === 'number' && q.choix[r] != null ? md(q.choix[r]) : '';
    return r && String(r).trim() ? '<span class="dv-rep">' + esc(r) + '</span>' : '';
  }
  function ecranResultat() {
    stopActif();
    var R = D.resultat, S = D.sujet, n = R.note, wrap = el('div', 'dv-resultat');
    var msg = n >= 18 ? 'Excellent' + NB + '! Tu maîtrises ce chapitre.' : n >= 14 ? 'Très bien' + NB + '! Regarde la correction des quelques erreurs.' :
      n >= 10 ? 'C\'est en bonne voie. Lis attentivement la correction.' : 'Courage' + NB + ': relis le cours, puis la correction ci-dessous. Chaque essai te fait progresser.';
    var parQ = {};
    S.questions.forEach(function (q) { parQ[q.id] = q; });
    var html = demoBanner() +
      '<section class="qz-score dv-score ' + (n >= 10 ? 'is-pass' : 'is-fail') + '" aria-labelledby="dv-t">' +
        '<p class="qz-score-n"><b>' + fr(n) + '</b><span>/20</span></p><div><h2 id="dv-t" class="qz-score-m">' + esc(msg) + '</h2>' +
        '<p class="qz-score-x">' + esc(ident.prenom) + ' ' + esc(ident.nom.toUpperCase()) + ' · ' + esc(ident.classe) + ' · essai ' + R.essai + ' sur ' + R.essaisMax + '</p>' +
        '<p class="qz-score-x">' + (demo ? 'Mode démo&nbsp;: note calculée sur cet appareil, rien n\'a été envoyé.' : 'Ta note a bien été transmise à ton professeur.') + '</p></div>' +
      '</section>' +
      '<div class="dv-actions dv-actions--res">' +
        (R.peutRefaire ? '<button class="btn" type="button" data-refaire>Refaire le devoir (nouveau sujet)</button>' : '') +
        '<a class="btn btn--ghost" href="' + esc(C.retour) + '">Retour aux devoirs</a></div>' +
      (R.peutRefaire ? '<p class="dv-muted">Il te reste ' + R.restants + ' essai' + (R.restants > 1 ? 's' : '') + '. Le nouveau sujet a les mêmes questions avec d\'autres nombres' + (demo ? '' : '&nbsp;; le professeur voit tous tes essais') + '.</p>' : '') +
      '<h2 class="dv-h2">Correction détaillée</h2><ol class="qz-rev dv-rev">';
    R.detail.forEach(function (c) {
      var q = parQ[c.id] || { type: 'saisie', enonce: '', numero: c.numero }, r = D.reponses[c.id];
      var cls = c.statut === 'juste' ? 'is-ok' : (c.statut === 'partiel' ? 'is-part' : 'is-ko');
      var tag = c.statut === 'juste' ? '<span class="qz-tag ok">Juste</span>' : c.statut === 'partiel' ? '<span class="qz-tag part">En partie</span>' : c.statut === 'vide' ? '<span class="qz-tag ko">Sans réponse</span>' : '<span class="qz-tag ko">À revoir</span>';
      html += '<li class="' + cls + '"><p class="qz-rev-q"><b>Question ' + c.numero + ' — ' + esc(c.titre) + '</b> <span class="dv-pts">' + fr(c.points) + '/' + c.max + '</span></p>' +
        '<p class="dv-rev-e">' + md(q.enonce) + '</p>';
      if (q.type === 'trous' && c.trous) {
        var arr = Array.isArray(r) ? r : [], parts = String(q.texte).split(/\[\[(\d+)\]\]/), t = '';
        for (var i = 0; i < parts.length; i++) {
          if (i % 2 === 0) t += md(parts[i]);
          else {
            var k = +parts[i], h = c.trous[k] || {}, v = arr[k] && String(arr[k]).trim();
            t += h.ok ? '<mark class="dv-h-ok">' + esc(v) + '</mark>' : (v ? '<s class="dv-h-ko">' + esc(v) + '</s> ' : '<span class="dv-h-vide">(vide)</span> ') + '<mark class="dv-h-sol">' + md(h.attendu) + '</mark>';
          }
        }
        html += '<p class="qz-rev-a dv-trous-c">' + tag + ' ' + t + '</p>';
      } else {
        var mine = reponseEleve(q, r);
        html += '<p class="qz-rev-a">' + tag + ' ' + (c.statut === 'juste' ? 'Ta réponse' + NB + ': ' + (mine || md(c.attendu))
          : (mine ? 'Ta réponse' + NB + ': <s>' + mine + '</s> · ' : '') + 'Réponse attendue' + NB + ': <b>' + md(c.attendu) + '</b>') + '</p>';
      }
      if (c.explication) html += '<p class="qz-rev-e">' + md(c.explication) + '</p>';
      html += '</li>';
    });
    html += '</ol>';
    wrap.innerHTML = html;
    show(wrap);
    var b = wrap.querySelector('[data-refaire]');
    if (b) b.addEventListener('click', function () {
      var e = R.essai + 1;
      try { localStorage.removeItem(K); } catch (x) {}
      D = null;
      chargerSujet(e);
    });
    top();
    focusFirst('#dv-t');
    var h = wrap.querySelector('#dv-t'); if (h) h.setAttribute('tabindex', '-1');
  }

  /* ── Démarrage ──────────────────────────────────────────────────── */
  katex().then(function () {
    if (!C.url) {
      if (location.hash === '#demo' && C.demoDispo) { demo = true; ecranIdentite(); }
      else ecranIndispo();
    } else ecranIdentite();
  });
})();
