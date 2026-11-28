/* Σ Sigma — activités en ligne (pages /en-ligne/…/).
   - Python : éditeur + console, exécutés sur l'appareil par Pyodide (hébergé sur le site, dans un Web Worker) ;
     lien « Ouvrir dans Basthon » qui emporte le code tel qu'il est dans l'éditeur (paramètre script=, compressé
     comme le fait Basthon : zlib + base64url ; sinon texte brut, que Basthon accepte aussi).
   - GeoGebra : appliquette officielle (www.geogebra.org/apps/deployggb.js), chargée à la demande,
     préparée par des commandes (evalCommand) ; l'élève fait lui-même la manipulation demandée.
   Aucune donnée n'est envoyée au site ; aucun cookie, aucun compte. */
(function () {
  'use strict';

  /* ───────────── Python ───────────── */
  function PyBox(root, rang) {
    this.root = root;
    this.ed = root.querySelector('[data-py-code]');
    this.out = root.querySelector('[data-py-out]');
    this.form = root.querySelector('[data-py-repl]');
    this.line = root.querySelector('[data-py-line]');
    this.state = root.querySelector('[data-py-state]');
    this.start = this.ed ? this.ed.value : '';
    this.hist = []; this.hpos = 0;
    this.busy = false; this.w = null;
    var self = this;
    root.querySelectorAll('[data-py-act]').forEach(function (b) {
      b.addEventListener('click', function () { self[b.getAttribute('data-py-act')](); });
    });
    if (this.form) this.form.addEventListener('submit', function (e) { e.preventDefault(); self.eval(); });
    if (this.line) this.line.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowUp' && self.hist.length) { e.preventDefault(); self.hpos = Math.max(0, self.hpos - 1); self.line.value = self.hist[self.hpos]; }
      if (e.key === 'ArrowDown' && self.hist.length) { e.preventDefault(); self.hpos = Math.min(self.hist.length, self.hpos + 1); self.line.value = self.hist[self.hpos] || ''; }
    });
    if (this.ed) this.ed.addEventListener('keydown', function (e) { self.key(e); });
    var bas = root.querySelector('[data-basthon]');
    if (bas) bas.addEventListener('click', function (e) { e.preventDefault(); self.basthon(bas); });
    /* Un seul Python démarre avec la page ; les éditeurs suivants démarrent le leur au premier clic
       (chaque démarrage charge environ 13 Mo, lourd sur un téléphone). */
    if (!rang) this.boot();
    else { this.ready = false; this.setState('Python démarrera au premier clic sur « Exécuter » ou « Valider ».', ''); }
  }
  PyBox.prototype.setState = function (t, cls) {
    if (!this.state) return;
    this.state.textContent = t; this.state.className = 'py-state' + (cls ? ' py-state--' + cls : '');
  };
  PyBox.prototype.print = function (t, cls) {
    var s = document.createElement('span'); if (cls) s.className = cls; s.textContent = t;
    this.out.appendChild(s); this.out.scrollTop = this.out.scrollHeight;
  };
  PyBox.prototype.boot = function () {
    var self = this;
    this.ready = false; this.setState('Chargement de Python…', 'wait');
    this.root.classList.add('is-loading');
    try { this.w = new Worker('/assets/js/en-ligne-py-worker.mjs', { type: 'module' }); }
    catch (e) { this.setState('Python ne peut pas démarrer sur ce navigateur : utilise le bouton « Ouvrir dans Basthon ».', 'err'); return; }
    this.w.onmessage = function (e) {
      var m = e.data || {};
      if (m.type === 'ready') { self.ready = true; self.root.classList.remove('is-loading'); self.setState('Python est prêt.', 'ok'); }
      else if (m.type === 'out') self.print(m.text);
      else if (m.type === 'err') self.print(m.text, 'py-err');
      else if (m.type === 'fatal') self.setState('Python n’a pas pu démarrer (' + m.text + '). Utilise le bouton « Ouvrir dans Basthon ».', 'err');
      else if (m.type === 'done') { self.busy = false; self.root.classList.remove('is-running'); self.setState('Terminé.', 'ok'); if (self.line) self.line.focus({ preventScroll: true }); }
    };
    this.w.onerror = function () { self.setState('Python n’a pas pu démarrer. Utilise le bouton « Ouvrir dans Basthon ».', 'err'); };
  };
  PyBox.prototype.send = function (type, code) {
    if (!this.w) this.boot();
    if (!this.w) return;
    if (this.busy) { this.setState('Patiente : le programme précédent tourne encore (ou clique sur « Arrêter »).', 'wait'); return; }
    this.busy = true; this.root.classList.add('is-running');
    this.setState(this.ready ? 'Exécution…' : 'Chargement de Python… le programme partira tout seul.', 'wait');
    this.w.postMessage({ type: type, code: code });
  };
  PyBox.prototype.run = function () {
    this.out.textContent = '';
    this.print('>>> exécution du programme\n', 'py-info');
    this.send('run', this.ed.value);
  };
  PyBox.prototype.eval = function () {
    var c = this.line.value;
    if (!c.trim()) return;
    this.hist.push(c); this.hpos = this.hist.length;
    this.print('>>> ' + c + '\n', 'py-cmd');
    this.line.value = '';
    this.send('eval', c);
  };
  PyBox.prototype.stop = function () {
    if (this.w) this.w.terminate();
    this.busy = false; this.root.classList.remove('is-running');
    this.print('\nProgramme arrêté.\n', 'py-err');
    this.boot();
  };
  PyBox.prototype.clear = function () { this.out.textContent = ''; };
  PyBox.prototype.reset = function () {
    if (this.ed) this.ed.value = this.start;
    this.out.textContent = '';
    if (this.w && !this.busy) this.w.postMessage({ type: 'reset' });
    this.setState('Code de départ rétabli.', 'ok');
  };
  /* Éditeur : Tab = 4 espaces, Entrée garde l'indentation (et l'augmente après « : »). */
  PyBox.prototype.key = function (e) {
    var ta = this.ed, v = ta.value, a = ta.selectionStart, b = ta.selectionEnd;
    if (e.key === 'Tab' && !e.shiftKey) {
      e.preventDefault(); ta.setRangeText('    ', a, b, 'end');
    } else if (e.key === 'Enter' && !e.ctrlKey && !e.metaKey) {
      var deb = v.lastIndexOf('\n', a - 1) + 1, ligne = v.slice(deb, a);
      var ind = (ligne.match(/^ */) || [''])[0];
      if (/:\s*$/.test(ligne)) ind += '    ';
      e.preventDefault(); ta.setRangeText('\n' + ind, a, b, 'end');
    } else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault(); this.run();
    }
  };
  /* Lien Basthon : https://console.basthon.fr/?script=<contenu> (voir basthon.fr/documentation/liens/). */
  function b64url(bytes) {
    var s = ''; for (var i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
    return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  async function deflate(text) {
    var cs = new CompressionStream('deflate');
    var flux = new Blob([new TextEncoder().encode(text)]).stream().pipeThrough(cs);
    return new Uint8Array(await new Response(flux).arrayBuffer());
  }
  PyBox.prototype.basthonURL = async function () {
    /* Programme de l'éditeur ; console seule : les instructions déjà saisies (ou celle proposée). */
    var src = this.ed ? this.ed.value : (this.hist.length ? this.hist.join('\n') : (this.line ? this.line.value : ''));
    var code = src.replace(/\r\n|\r|\n/g, '\r\n');
    var p;
    try { p = b64url(await deflate(code)); } catch (e) { p = code; }
    var u = new URL('https://console.basthon.fr/');
    u.searchParams.set('kernel', 'python');
    u.searchParams.set('script', p);
    return u.href.replace(/\(/g, '%28').replace(/\)/g, '%29');
  };
  PyBox.prototype.basthon = async function (a) {
    var url = await this.basthonURL();
    a.setAttribute('href', url);
    var w = window.open(url, '_blank', 'noopener');
    if (!w) location.href = url;
  };

  /* ───────────── GeoGebra ───────────── */
  var GGB_JS = window.SIGMA_GGB_DEPLOY || 'https://www.geogebra.org/apps/deployggb.js';
  var ggbLoading = null;
  function loadGGB() {
    if (window.GGBApplet) return Promise.resolve();
    if (ggbLoading) return ggbLoading;
    ggbLoading = new Promise(function (ok, ko) {
      var s = document.createElement('script'); s.src = GGB_JS; s.async = true;
      s.onload = ok; s.onerror = function () { ggbLoading = null; ko(new Error('GeoGebra')); };
      document.head.appendChild(s);
    });
    return ggbLoading;
  }
  function GgbBox(root) {
    this.root = root;
    this.cfg = JSON.parse(root.querySelector('script[type="application/json"]').textContent);
    this.host = root.querySelector('[data-ggb-host]');
    this.state = root.querySelector('[data-ggb-state]');
    var self = this;
    root.querySelectorAll('[data-ggb-act]').forEach(function (b) {
      b.addEventListener('click', function () { self[b.getAttribute('data-ggb-act')](); });
    });
    this.start();
  }
  GgbBox.prototype.size = function () {
    var w = Math.max(300, Math.floor(this.host.clientWidth));
    var h = Math.round(Math.min(Math.max(window.innerHeight * 0.72, 440), 680));
    if (w < 600) h = Math.round(Math.max(window.innerHeight * 0.78, 480));
    return [w, h];
  };
  GgbBox.prototype.say = function (t, cls) { if (this.state) { this.state.textContent = t; this.state.className = 'ggb-state' + (cls ? ' ggb-state--' + cls : ''); } };
  GgbBox.prototype.prepare = function () {
    var api = this.api, c = this.cfg, n = 0;
    (c.commandes || []).forEach(function (cmd) { if (api.evalCommand(cmd)) n++; });
    if (c.cacher) c.cacher.forEach(function (o) { api.setVisible(o, false); });
    this.cadrer();
    /* la disposition (surtout sur téléphone) se fixe après le chargement : on recadre ensuite */
    var self = this; setTimeout(function () { self.cadrer(); }, 700); setTimeout(function () { self.cadrer(); }, 2000);
    this.ok = n === (c.commandes || []).length;
    return this.ok;
  };
  GgbBox.prototype.cadrer = function () {
    if (this.api && this.cfg.fenetre) this.api.evalCommand('ZoomIn(' + this.cfg.fenetre.join(',') + ')');
  };
  GgbBox.prototype.start = function () {
    var self = this, c = this.cfg, wh = this.size();
    this.say('Chargement de GeoGebra…', 'wait');
    loadGGB().then(function () {
      var params = {
        appName: c.app || 'classic', width: wh[0], height: wh[1], language: 'fr', country: 'FR',
        showToolBar: c.barre !== false, showAlgebraInput: true, showMenuBar: false, showResetIcon: false,
        enableShiftDragZoom: true, enableRightClick: true, showZoomButtons: true, useBrowserForJS: false,
        showLogging: false, allowStyleBar: true, errorDialogsActive: true, preventFocus: true,
        appletOnLoad: function (api) {
          self.api = api; self.prepare();
          self.say('GeoGebra est prêt : à toi de jouer.', 'ok');
          self.root.classList.add('is-ready');
        }
      };
      if (c.perspective) params.perspective = c.perspective;
      if (window.SIGMA_GGB_PARAMS) Object.assign(params, window.SIGMA_GGB_PARAMS); /* réservé aux tests automatiques */
      var applet = new window.GGBApplet(params, true);
      if (window.SIGMA_GGB_CODEBASE) applet.setHTML5Codebase(window.SIGMA_GGB_CODEBASE);
      applet.inject(self.host.id);
    }).catch(function () {
      self.say('GeoGebra n’a pas pu se charger (connexion ?). Réessaie, ou ouvre GeoGebra dans un nouvel onglet avec le lien ci-dessous.', 'err');
    });
    var t = null;
    window.addEventListener('resize', function () {
      clearTimeout(t); t = setTimeout(function () { if (self.api && self.api.setSize) { var s = self.size(); self.api.setSize(s[0], s[1]); setTimeout(function () { self.cadrer(); }, 400); } }, 250);
    });
  };
  GgbBox.prototype.reset = function () {
    if (!this.api) return;
    this.api.newConstruction(); this.prepare();
    this.say('Figure de départ rétablie.', 'ok');
  };

  function init() {
    document.querySelectorAll('[data-py]').forEach(function (r, i) { r.__py = new PyBox(r, i); });
    document.querySelectorAll('[data-ggb]').forEach(function (r) { r.__ggb = new GgbBox(r); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
