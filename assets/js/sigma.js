/* ═══════════════════════════════════════════════════════════════════
   Σ Sigma — scripts du site (menu, recherche, constellation, parcours)
   Aucun service externe ; tout fonctionne sans compte et sans cookie.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var doc = document, body = doc.body;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = window.matchMedia('(min-width: 1100px)');

  /* ── Menu ─────────────────────────────────────────────────────────── */
  var panel = doc.getElementById('site-menu');
  var toggles = Array.prototype.slice.call(doc.querySelectorAll('[data-menu-toggle]'));
  var lastToggle = null;
  function setMenu(open, from) {
    if (!panel) return;
    panel.hidden = !open;
    body.classList.toggle('menu-open', open);
    toggles.forEach(function (t) {
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (t.classList.contains('menu-btn')) {
        var l = t.querySelector('.lbl'); if (l) l.textContent = open ? 'Fermer' : 'Menu';
      }
    });
    if (open) { lastToggle = from || null; panel.scrollTop = 0; }
    else if (from === 'esc' && lastToggle) { lastToggle.focus(); }
  }
  toggles.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.stopPropagation();
      setMenu(panel.hidden, t);
    });
  });
  if (panel) {
    panel.addEventListener('click', function (e) {
      e.stopPropagation();
      if (e.target.closest('a')) setMenu(false);
    });
    doc.addEventListener('click', function () { if (!panel.hidden) setMenu(false); });
    panel.querySelectorAll('.menu-group-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        var sub = doc.getElementById(b.getAttribute('aria-controls'));
        var open = b.getAttribute('aria-expanded') !== 'true';
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (sub) sub.hidden = !open;
      });
    });
  }
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel && !panel.hidden) setMenu(false, 'esc');
  });
  if (desktop.addEventListener) desktop.addEventListener('change', function () { if (panel && !panel.hidden) setMenu(false); });

  /* ── Formules (KaTeX, chargé seulement sur les pages qui en contiennent) ── */
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(doc.querySelector('main') || body, {
        delimiters: [{ left: '$', right: '$', display: false }],
        throwOnError: false, ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'input']
      });
    } catch (e) {}
  }

  /* ── Liens PDF : nouvel onglet (contenus anciens) ─────────────────── */
  doc.querySelectorAll('a[href$=".pdf"]:not([target])').forEach(function (a) {
    a.target = '_blank'; a.rel = 'noopener';
  });

  /* ── Statistiques anonymes (GoatCounter, sans cookies) ─────────────
     Clics sur les PDF et ouverture des jeux Sigma Arcade, comptés comme événements.
     Sans effet si GoatCounter n'est pas activé (goatcounter_code vide). */
  doc.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var gc = window.goatcounter;
    if (!gc || typeof gc.count !== 'function') return;
    var u; try { u = new URL(a.href, location.href); } catch (err) { return; }
    if (u.origin !== location.origin) return;
    var path = null, title = (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120);
    if (/\.pdf$/i.test(u.pathname)) path = 'pdf' + decodeURIComponent(u.pathname);
    else { var m = u.pathname.match(/^\/sigma-arcade\/([a-z0-9-]+)\/?$/); if (m) path = 'jeu/' + m[1]; }
    if (!path) return;
    try { gc.count({ path: path, title: title || path, event: true }); } catch (err) {}
  });

  /* ── Recherche ────────────────────────────────────────────────────── */
  var dlg = doc.getElementById('search');
  var input = doc.getElementById('search-input');
  var list = doc.getElementById('search-results');
  var status = doc.getElementById('search-status');
  var filterBtns = dlg ? Array.prototype.slice.call(dlg.querySelectorAll('.search-filters button')) : [];
  var index = null, loading = null, kind = '', sel = -1, opener = null;

  function norm(s) {
    return (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
      .replace(/[’'`]/g, ' ').replace(/œ/g, 'oe').replace(/æ/g, 'ae');
  }
  function esc(s) { return (s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function load() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch('/search.json', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      var seen = {};
      index = d.filter(function (x) {
        if (!x || !x.u) return false;
        var key = x.u + '|' + x.c; if (seen[key]) return false; seen[key] = 1; return true;
      }).map(function (x) { x.nt = norm(x.t); x.nc = norm(x.c); return x; });
      return index;
    }).catch(function () { index = []; return index; });
    return loading;
  }
  var KW = { 'Classe': 9, 'Chapitre': 7, 'Jeu': 6, 'Cours': 4, 'Exercices': 3, 'Évaluation': 2, 'Page': 1 };
  function search(q) {
    var nq = norm(q).trim();
    var toks = nq.split(/\s+/).filter(Boolean);
    var res = [];
    if (!index) return res;
    index.forEach(function (x) {
      if (kind && x.k !== kind) return;
      if (!toks.length) { if (x.k === 'Classe' || x.k === 'Jeu') res.push({ x: x, s: KW[x.k] }); return; }
      var hay = x.nt + ' ' + x.nc, s = KW[x.k] || 0;
      for (var i = 0; i < toks.length; i++) {
        if (hay.indexOf(toks[i]) < 0) return;
        if (x.nt.indexOf(toks[i]) >= 0) s += 10;
        if ((' ' + x.nt).indexOf(' ' + toks[i]) >= 0) s += 4;
      }
      if (x.nt.indexOf(nq) === 0) s += 40; else if (x.nt.indexOf(nq) >= 0) s += 20;
      res.push({ x: x, s: s });
    });
    res.sort(function (a, b) { return b.s - a.s || a.x.t.length - b.x.t.length; });
    return res.slice(0, 40).map(function (r) { return r.x; });
  }
  function mark(t, q) {
    var toks = norm(q).trim().split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!toks.length) return esc(t);
    var nt = norm(t), marks = new Array(t.length + 1).join('0').split('');
    toks.forEach(function (w) { var i = nt.indexOf(w); while (i >= 0) { for (var k = i; k < i + w.length; k++) marks[k] = '1'; i = nt.indexOf(w, i + w.length); } });
    var out = '', on = false;
    for (var i = 0; i < t.length; i++) {
      if (marks[i] === '1' && !on) { out += '<mark>'; on = true; }
      if (marks[i] !== '1' && on) { out += '</mark>'; on = false; }
      out += esc(t[i]);
    }
    return out + (on ? '</mark>' : '');
  }
  function render() {
    var q = input.value;
    var r = search(q);
    sel = -1;
    if (!r.length) {
      list.innerHTML = '<li class="search-empty" role="presentation">' + (index ? 'Aucun résultat pour <b>' + esc(q) + '</b>. Essayez un autre mot (« fonction », « vecteurs », « DS blanc »…).' : 'Chargement…') + '</li>';
      input.setAttribute('aria-expanded', 'false');
      if (status) status.textContent = index ? 'Aucun résultat' : '';
      return;
    }
    var head = q.trim() ? '' : '<li class="search-empty" role="presentation">Accès rapide&nbsp;: <b>classes</b> et <b>jeux</b>. Tapez un mot pour chercher partout.</li>';
    list.innerHTML = head + r.map(function (x, i) {
      var pdf = /\.pdf$/i.test(x.u);
      return '<li role="option" id="sr-' + i + '" aria-selected="false"><a href="' + esc(x.u) + '"' + (pdf ? ' target="_blank" rel="noopener"' : '') + ' tabindex="-1">' +
        '<span class="sr-type" data-k="' + esc(x.k) + '">' + esc(x.k) + '</span>' +
        '<span><span class="sr-title">' + mark(x.t, q) + '</span><span class="sr-ctx">' + esc(x.c) + (pdf ? ' · PDF' : '') + '</span></span></a></li>';
    }).join('');
    input.setAttribute('aria-expanded', 'true');
    if (status) status.textContent = r.length + (r.length > 1 ? ' résultats' : ' résultat');
  }
  function move(d) {
    var opts = list.querySelectorAll('[role="option"]');
    if (!opts.length) return;
    if (sel >= 0 && opts[sel]) opts[sel].setAttribute('aria-selected', 'false');
    sel = (sel + d + opts.length) % opts.length;
    opts[sel].setAttribute('aria-selected', 'true');
    input.setAttribute('aria-activedescendant', opts[sel].id);
    opts[sel].scrollIntoView({ block: 'nearest' });
  }
  function openSearch(q, from) {
    if (!dlg) return;
    opener = from || doc.activeElement;
    if (panel && !panel.hidden) setMenu(false);
    dlg.hidden = false;
    body.classList.add('search-open');
    body.style.overflow = 'hidden';
    if (typeof q === 'string') input.value = q;
    input.focus();
    render();
    load().then(render);
  }
  function closeSearch() {
    if (!dlg || dlg.hidden) return;
    dlg.hidden = true;
    body.classList.remove('search-open');
    body.style.overflow = '';
    input.removeAttribute('aria-activedescendant');
    if (opener && opener.focus) opener.focus();
  }
  if (dlg) {
    doc.querySelectorAll('[data-search-open]').forEach(function (b) {
      b.addEventListener('click', function (e) { e.stopPropagation(); openSearch(undefined, b); });
    });
    dlg.querySelector('[data-search-close]').addEventListener('click', closeSearch);
    dlg.addEventListener('click', function (e) { if (e.target === dlg) closeSearch(); });
    input.addEventListener('input', render);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') {
        var opts = list.querySelectorAll('[role="option"] a');
        var a = opts[sel >= 0 ? sel : 0];
        if (a) { e.preventDefault(); a.click(); if (a.target === '_blank') closeSearch(); }
      }
    });
    filterBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        kind = b.getAttribute('data-k');
        filterBtns.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        render(); input.focus();
      });
    });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); closeSearch(); return; }
      if (e.key === 'Tab') {
        var f = Array.prototype.slice.call(dlg.querySelectorAll('input, button, [role="option"] a')).filter(function (n) { return n.offsetParent !== null; });
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    list.addEventListener('click', function (e) { var a = e.target.closest('a'); if (a && a.target === '_blank') closeSearch(); });
    doc.addEventListener('keydown', function (e) {
      var t = e.target, typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if ((e.key === '/' && !typing) || ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K'))) {
        if (dlg.hidden) { e.preventDefault(); openSearch(); }
      }
    });
    var qp = new URLSearchParams(location.search).get('q');
    if (qp) openSearch(qp);
  }

  /* ── Parcours du chapitre : étape active ──────────────────────────── */
  var pnav = doc.querySelector('.parcours-nav');
  if (pnav && 'IntersectionObserver' in window) {
    var links = {};
    pnav.querySelectorAll('a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (x.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].classList.toggle('is-active', k === x.target.id); });
        }
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    Object.keys(links).forEach(function (k) { var s = doc.getElementById(k); if (s) io.observe(s); });
  }

  /* ── Mathématicien de la semaine ──────────────────────────────────── */
  (function () {
    var data = window.mathData || [];
    var img = doc.getElementById('math-image');
    if (!data.length || !img) return;
    var $ = function (id) { return doc.getElementById(id); };
    var start = new Date(new Date().getFullYear(), 0, 1);
    var cur = Math.floor(Math.floor((Date.now() - start) / 86400000) / 7) % data.length;
    img.addEventListener('error', function () { img.style.visibility = 'hidden'; });
    function show(i) {
      var m = data[i]; if (!m) return;
      img.style.visibility = '';
      if (m.image) img.src = m.image;
      img.alt = 'Portrait de ' + (m.nom || '');
      $('math-name').textContent = m.nom || '';
      $('math-dates').textContent = m.dates || '';
      $('math-resume').textContent = m.resume || '';
      $('math-apport').textContent = m.apport || '';
      $('math-citation').textContent = m.citation ? '« ' + m.citation + ' »' : '';
    }
    var p = $('math-prev'), n = $('math-next');
    if (p) p.addEventListener('click', function () { cur = (cur - 1 + data.length) % data.length; show(cur); });
    if (n) n.addEventListener('click', function () { cur = (cur + 1) % data.length; show(cur); });
    show(cur);
  })();

  /* ── Constellation de l'accueil ───────────────────────────────────────
     Des symboles mathématiques dérivent comme des étoiles et se relient ;
     régulièrement, quelques étoiles se rangent en figure (polygone régulier,
     parabole, sinusoïde) tracée en or. Pause hors écran ; image fixe si
     l'utilisateur préfère réduire les animations. */
  (function () {
    var cv = doc.getElementById('constellation');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var W = 0, H = 0, dpr = 1, nodes = [], D = 140, running = false, visible = true, last = 0;
    var GLYPHS = ['π', 'Σ', '∫', '√', '∞', 'Δ', 'θ', 'φ', '≈', '±', 'x²', 'ƒ', '∈', 'e', 'i', '∂', '÷', '≤', '%', 'α'];
    var FIGS = [
      { n: 3, name: 'triangle équilatéral' }, { n: 4, name: 'carré' }, { n: 5, name: 'pentagone régulier' },
      { n: 6, name: 'hexagone régulier' }, { n: 5, name: 'y = x²', kind: 'para' }, { n: 7, name: 'y = sin x', kind: 'sin' }
    ];
    var fig = null, figT = 0, figIdx = Math.floor(Math.random() * FIGS.length), nextFig = 1.6;
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function size() {
      var r = cv.getBoundingClientRect();
      W = Math.max(1, r.width); H = Math.max(1, r.height);
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      D = Math.max(90, Math.min(160, W * 0.16));
      var target = Math.round(Math.max(26, Math.min(78, W * H / 15000)));
      while (nodes.length < target) nodes.push(mk());
      if (nodes.length > target) nodes.length = target;
      nodes.forEach(function (n) { if (n.x > W) n.x = rnd(0, W); if (n.y > H) n.y = rnd(0, H); });
    }
    function mk() {
      var g = Math.random() < 0.38;
      var a = rnd(0, Math.PI * 2), v = rnd(5, 14);
      return { x: rnd(0, W), y: rnd(0, H), vx: Math.cos(a) * v, vy: Math.sin(a) * v, g: g ? GLYPHS[Math.floor(Math.random() * GLYPHS.length)] : null,
               s: g ? rnd(13, 22) : rnd(1, 2.2), ph: rnd(0, 6.28), tx: null, ty: null };
    }
    function startFigure() {
      var f = FIGS[figIdx++ % FIGS.length];
      var right = W > 760;
      var cx = right ? rnd(W * 0.6, W * 0.84) : rnd(W * 0.25, W * 0.75);
      var cy = right ? rnd(H * 0.25, H * 0.6) : rnd(H * 0.12, H * 0.32);
      var R = Math.min(W, H) * (right ? 0.17 : 0.14);
      var pts = [];
      for (var i = 0; i < f.n; i++) {
        if (f.kind === 'para') { var u = -1 + 2 * i / (f.n - 1); pts.push([cx + u * R * 1.2, cy + R * 0.9 - u * u * R * 1.6]); }
        else if (f.kind === 'sin') { var u2 = i / (f.n - 1); pts.push([cx - R * 1.4 + u2 * R * 2.8, cy - Math.sin(u2 * Math.PI * 2) * R * 0.6]); }
        else { var a = -Math.PI / 2 + i * 2 * Math.PI / f.n; pts.push([cx + Math.cos(a) * R, cy + Math.sin(a) * R]); }
      }
      var free = nodes.slice().sort(function (a, b) { return (Math.hypot(a.x - cx, a.y - cy)) - (Math.hypot(b.x - cx, b.y - cy)); });
      var members = free.slice(0, f.n);
      members.forEach(function (m, i) { m.tx = pts[i][0]; m.ty = pts[i][1]; });
      fig = { f: f, m: members, closed: !f.kind, cx: cx, cy: cy, R: R }; figT = 0;
    }
    function endFigure() { if (fig) fig.m.forEach(function (m) { m.tx = m.ty = null; }); fig = null; nextFig = 2.2; }
    function step(dt) {
      if (fig) { figT += dt; if (figT > 6.2) endFigure(); }
      else { nextFig -= dt; if (nextFig <= 0) startFigure(); }
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        if (n.tx !== null) { var k = Math.min(1, dt * 2.2); n.x += (n.tx - n.x) * k; n.y += (n.ty - n.y) * k; }
        else {
          n.x += n.vx * dt; n.y += n.vy * dt;
          if (n.x < -30) n.x = W + 30; else if (n.x > W + 30) n.x = -30;
          if (n.y < -30) n.y = H + 30; else if (n.y > H + 30) n.y = -30;
        }
        n.ph += dt * 1.4;
      }
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1;
      for (var i = 0; i < nodes.length; i++) {
        var a = nodes[i];
        for (var j = i + 1; j < nodes.length; j++) {
          var b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy;
          if (d2 < D * D) {
            var al = (1 - Math.sqrt(d2) / D) * 0.32;
            ctx.strokeStyle = 'rgba(126,154,255,' + al.toFixed(3) + ')';
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
      }
      if (fig) {
        var t = figT, alpha = t < 1.2 ? t / 1.2 : t > 5.2 ? Math.max(0, (6.2 - t)) : 1;
        ctx.strokeStyle = 'rgba(232,199,102,' + (0.85 * alpha).toFixed(3) + ')';
        ctx.lineWidth = 1.6;
        ctx.shadowColor = 'rgba(232,199,102,.6)'; ctx.shadowBlur = 12;
        ctx.beginPath();
        fig.m.forEach(function (m, i) { if (i) ctx.lineTo(m.x, m.y); else ctx.moveTo(m.x, m.y); });
        if (fig.closed) ctx.closePath();
        ctx.stroke();
        ctx.shadowBlur = 0;
        ctx.fillStyle = 'rgba(232,199,102,' + (0.9 * alpha).toFixed(3) + ')';
        ctx.font = '600 14px Outfit, system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(fig.f.name, fig.cx, fig.cy + fig.R * (fig.f.kind ? 1.25 : 1.35) + 8);
      }
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (var k = 0; k < nodes.length; k++) {
        var n = nodes[k], tw = 0.65 + 0.35 * Math.sin(n.ph);
        var inFig = n.tx !== null;
        if (n.g) {
          ctx.fillStyle = inFig ? 'rgba(245,222,150,' + (0.95 * tw).toFixed(3) + ')' : 'rgba(190,205,255,' + (0.5 * tw).toFixed(3) + ')';
          ctx.font = '500 ' + n.s.toFixed(0) + 'px Outfit, system-ui, sans-serif';
          ctx.fillText(n.g, n.x, n.y);
        } else {
          ctx.fillStyle = inFig ? 'rgba(245,222,150,.95)' : 'rgba(235,240,255,' + (0.75 * tw).toFixed(3) + ')';
          ctx.beginPath(); ctx.arc(n.x, n.y, inFig ? 2.6 : n.s, 0, 6.2832); ctx.fill();
        }
      }
      ctx.textBaseline = 'alphabetic';
    }
    function loop(ts) {
      if (!running) return;
      var dt = last ? Math.min(0.05, (ts - last) / 1000) : 0.016;
      last = ts;
      step(dt); draw();
      requestAnimationFrame(loop);
    }
    function play() { if (running || reduceMotion || !visible || doc.hidden) return; running = true; last = 0; requestAnimationFrame(loop); }
    function pause() { running = false; }
    size();
    if (reduceMotion) {
      // image fixe : une figure déjà formée
      startFigure(); fig.m.forEach(function (m) { m.x = m.tx; m.y = m.ty; }); figT = 2; draw();
      window.addEventListener('resize', function () { size(); draw(); });
      return;
    }
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(size, 150); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; visible ? play() : pause(); }).observe(cv);
    }
    doc.addEventListener('visibilitychange', function () { doc.hidden ? pause() : play(); });
    play();
  })();
})();
