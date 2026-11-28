/* ═══════════════════════════════════════════════════════════════════
   Σ Sigma — Encouragements (module commun : quiz, Sigma Arcade, épreuves)
   ---------------------------------------------------------------------
   Bonne réponse : petite phrase tirée au hasard, étoile et confettis discrets,
   applaudissements synthétisés (Web Audio, aucun fichier son, aucun droit).
   Série de réussites (3, 5, 10, puis tous les 5) : message spécial, applaudissements nourris.
   Erreur : aucun son, aucune couleur agressive ; phrase de persévérance,
   avec renvoi vers l'indice, la correction ou le conseil quand il y en a un.
   Fin de partie : bilan positif quel que soit le score, progression gardée
   sur l'appareil (localStorage « sigma-encouragements-v1 »).
   Son : bouton 🔊/🔇 (haut-parleur dessiné en SVG), choix mémorisé dans la clé « sigma-fanfare » (la même que
   l'interrupteur « Bruitages » des jeux : un seul réglage pour tout le site).
   Animations désactivées si l'appareil demande moins d'animations
   (prefers-reduced-motion) ; le son, lui, reste réglé par le bouton.
   Aucun pistage, aucune donnée envoyée.

   API (window.SigmaEncourage) :
   ok({after|into, anchor, sound, announce})  -> phrase affichée (série gérée)
   ko({after|into, hint:'indice'|'correction'|'conseil', announce}) -> phrase
   bilan({key, score, total, into|after, sound, noHead}) -> {html, text, head, record, first}
                              (noHead : seulement la phrase de progression)
   reset()                    remet la série à zéro (nouvelle partie)
   soundButton()              renvoie un bouton 🔊/🔇 prêt à placer
   soundOn() / setSound(bool)
   watch({ok:'#win', okAfter:'#winp', ko:'#fb', koAfter:'#fbp'})
                              branche les phrases sur les panneaux d'un jeu
   applause(force 1|2)        applaudissements seuls
   PHRASES                    listes de phrases (lecture)
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  if (window.SigmaEncourage) return;
  var doc = document, NB = ' ';

  /* ── Phrases ─────────────────────────────────────────────────────
     Français simple, « tu », jamais d'adjectif genré (fier/fière…),
     centrées sur l'effort et la méthode ; jamais moqueuses. */
  var OK = [
    'Bien raisonné' + NB + '!',
    'Tu vois, tu en es capable.',
    'Ta méthode est la bonne.',
    'Exact' + NB + ': ton raisonnement tient debout.',
    'Bravo, tu as pris le temps de réfléchir.',
    'C\'est juste' + NB + ': ton travail paie.',
    'Belle réponse, tu progresses.',
    'Tu as appliqué la bonne règle.',
    'Très bien' + NB + ': tu as lu l\'énoncé avec attention.',
    'Oui' + NB + '! Tu sais faire ça maintenant.',
    'C\'est ça' + NB + ': tes efforts portent leurs fruits.',
    'Bien joué' + NB + ': étape par étape, tu y arrives.',
    'Juste' + NB + '! Garde cette méthode, elle fonctionne.',
    'Tu as trouvé' + NB + ': les maths, c\'est aussi pour toi.',
    'Excellent réflexe.',
    'Bravo, c\'est un vrai raisonnement mathématique.',
    'Tu avances bien, continue comme ça.',
    'Réponse juste' + NB + ': tu as eu raison de te faire confiance.',
    'Tu maîtrises ce point.',
    'Calcul propre et réfléchi, bravo.',
    'Bonne réponse' + NB + ': tu comprends ce que tu fais.',
    'Bien vu' + NB + '! Tu as repéré l\'essentiel.',
    'Tu vois que tu sais faire.',
    'Précis et juste, bravo.',
    'C\'est exactement ça.',
    'Ton travail se voit.',
    'Encore une de réussie' + NB + ': ta confiance grandit, et c\'est mérité.',
    'Bravo' + NB + ': tu as fait le lien avec le cours.',
    'Juste' + NB + '! Chaque bonne réponse construit ta réussite.',
    'Tu as bien choisi ta méthode.',
    'Solide' + NB + '! Ton raisonnement est clair.',
    'Bien' + NB + ': tu n\'as pas eu peur de chercher.',
    'Très juste. Tes progrès en maths sont réels.',
    'Parfait' + NB + ': ce résultat, c\'est toi qui l\'as trouvé.',
    'Tu raisonnes avec rigueur' + NB + ': c\'est ça, faire des maths.',
    'Bravo' + NB + ': la persévérance, ça marche.',
    'Réussi' + NB + '! Et ce n\'est pas de la chance.',
    'Tu as compris la logique' + NB + ': bravo.',
    'Exact' + NB + ': tu sais utiliser ce que tu as appris.',
    'Bien raisonné, bien calculé.',
    'Oui' + NB + '! Ta réflexion a payé.',
    'Bonne réponse' + NB + ': tu es sur la bonne voie.',
    'Belle rigueur' + NB + '!',
    'Juste' + NB + ': tu viens de montrer que tu sais.',
    'Super' + NB + ': ton idée était la bonne.'
  ];
  var KO = [
    'Une erreur, c\'est une étape' + NB + ': relis l\'énoncé.',
    'Pas encore, mais tu cherches' + NB + ': c\'est comme ça qu\'on apprend.',
    'On apprend beaucoup de ses erreurs. Regarde où ça coince.',
    'Ce n\'est pas grave' + NB + ': reprends calmement, étape par étape.',
    'Vérifie ton travail ligne par ligne, sans te presser.',
    'Tout le monde se trompe, même les meilleurs. L\'important, c\'est de recommencer.',
    'Respire, relis la question' + NB + ': la réponse est à ta portée.',
    'Chaque erreur te rapproche de la bonne méthode.',
    'Pas tout à fait' + NB + ': compare ta réponse avec la règle du cours.',
    'Ce n\'est qu\'un essai. Le prochain sera meilleur.',
    'Tu as osé répondre' + NB + ': c\'est déjà un pas en avant.',
    'Une erreur repérée aujourd\'hui, c\'est une erreur évitée demain.',
    'Prends ton temps' + NB + ': personne ne te presse.',
    'Pas encore juste, mais tu progresses en cherchant.',
    'Relis chaque mot de l\'énoncé' + NB + ': un détail peut tout changer.',
    'Courage' + NB + ': comprendre une erreur, c\'est apprendre deux fois.',
    'Tu peux y arriver. Reprends tranquillement.',
    'Se tromper fait partie des maths. Continue.',
    'Lis la question à voix basse' + NB + ': ça aide à voir ce qu\'on demande.',
    'Ne lâche rien' + NB + ': la réussite vient avec la pratique.',
    'Bonne tentative. Que dit le cours sur ce point' + NB + '?',
    'Ce n\'est pas un échec, c\'est un entraînement.',
    'Tu as le droit de te tromper' + NB + ': c\'est comme ça qu\'on progresse.',
    'Essaie avec un exemple simple ou un petit schéma' + NB + ': ça aide souvent.',
    'Garde confiance' + NB + ': la méthode va venir.',
    'Une erreur ne dit rien de ta valeur' + NB + ': elle montre seulement quoi revoir.',
    'Reviens à la définition du cours' + NB + ': elle te guidera.',
    'Encore un petit effort, tu es en train d\'apprendre.'
  ];
  var HINT = {
    indice: ['Presque' + NB + '! Regarde l\'indice.', 'L\'indice est là pour toi' + NB + ': utilise-le.', 'Un coup d\'œil à l\'indice, et tu repars.', 'L\'indice te met sur la piste.'],
    correction: ['Lis la correction' + NB + ': elle te montre le chemin.', 'Regarde l\'explication, puis refais-la dans ta tête.', 'La correction est là pour t\'aider' + NB + ': prends le temps de la lire.', 'Compare ta réponse avec l\'explication.'],
    conseil: ['Lis le conseil' + NB + ': il t\'aide à repartir.', 'Le conseil juste au-dessus te donne la piste.', 'Suis le conseil, puis réessaie.', 'Le conseil te montre où regarder.']
  };
  var STREAK = {
    3: ['3 bonnes réponses d\'affilée' + NB + ': tu as trouvé le rythme' + NB + '!', '3 d\'affilée' + NB + '! Ta méthode est solide.', 'Et de 3' + NB + '! Tu prends confiance, et tu as raison.'],
    5: ['5 d\'affilée' + NB + '! Ce n\'est plus de la chance, c\'est de la méthode.', '5 bonnes réponses de suite' + NB + ': tu maîtrises le sujet.', 'Série de 5' + NB + '! Ton travail se voit vraiment.'],
    10: ['10 d\'affilée' + NB + '! Prends un instant pour savourer ce travail.', '10 bonnes réponses de suite' + NB + ': chapeau bas' + NB + '!', 'Série de 10' + NB + '! Tu viens de prouver que les maths sont pour toi.'],
    more: ['{n} d\'affilée' + NB + '! Impressionnant de régularité.', 'Série de {n}' + NB + '! Rien ne t\'arrête.', '{n} de suite' + NB + ': ta concentration est remarquable.']
  };
  var BILAN = {
    full: ['Sans faute' + NB + '! Ton travail régulier paie.', 'Tout juste' + NB + '! Tu maîtrises ces notions.', 'Score parfait' + NB + ': bravo pour ta rigueur.'],
    high: ['Très beau résultat' + NB + ': tu maîtrises l\'essentiel.', 'Bravo' + NB + '! Il ne reste que quelques détails à revoir.', 'Très bien' + NB + ': tes efforts se voient.'],
    mid: ['Tu as déjà une bonne base' + NB + ': les corrections vont t\'aider à aller plus loin.', 'C\'est en bonne voie' + NB + ': chaque essai te fait progresser.', 'Bon travail' + NB + ': regarde les corrections, puis recommence.'],
    low: ['Tu as réussi {s}' + NB + ': c\'est une base sur laquelle construire.', '{s} déjà' + NB + '! Relis les corrections et retente ta chance.', 'Tu as trouvé {s}' + NB + ': le reste viendra avec l\'entraînement.'],
    zero: ['Tu as tout tenté jusqu\'au bout' + NB + ': c\'est déjà du courage. Relis les corrections et retente.', 'Ce premier passage t\'a montré quoi revoir' + NB + ': c\'est utile. La prochaine fois sera meilleure.', 'Chaque essai compte' + NB + ': relis le cours et les corrections, puis recommence.']
  };

  /* ── Outils ─────────────────────────────────────────────────────── */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var bags = {};
  /* tirage sans répétition : on épuise la liste avant de la remélanger */
  function pick(name, list) {
    var b = bags[name];
    if (!b || !b.length) {
      b = bags[name] = list.map(function (_, i) { return i; });
      for (var i = b.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = b[i]; b[i] = b[j]; b[j] = t; }
    }
    return list[b.pop()];
  }
  function plural(n, w) { return n + ' ' + w + (n > 1 ? 's' : ''); }
  var reduce = false;
  try { reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  /* ── Feuille de style (même dossier que le script : …/js → …/css) ─ */
  var src = (doc.currentScript && doc.currentScript.src) || '';
  (function () {
    if (doc.querySelector('link[data-enc-css]')) return;
    var l = doc.createElement('link'); l.rel = 'stylesheet'; l.setAttribute('data-enc-css', '');
    l.href = src ? src.replace(/\/js\/encouragements\.js(\?.*)?$/, '/css/encouragements.css$1') : '/assets/css/encouragements.css';
    (doc.head || doc.documentElement).appendChild(l);
  })();

  /* ── Son ────────────────────────────────────────────────────────── */
  var SKEY = 'sigma-fanfare';
  function soundOn() { try { return localStorage.getItem(SKEY) !== '0'; } catch (e) { return true; } }
  var buttons = [];
  function setSound(on) {
    try { localStorage.setItem(SKEY, on ? '1' : '0'); } catch (e) {}
    paintButtons();
    if (!on && actx) { try { master.gain.cancelScheduledValues(actx.currentTime); master.gain.setValueAtTime(0, actx.currentTime); master.gain.setValueAtTime(VOL, actx.currentTime + 0.25); } catch (e) {} }
  }
  function paintButtons() {
    buttons = buttons.filter(function (b) { return b.isConnected; });
    buttons.forEach(paint);
  }
  function paint(b) {
    var on = soundOn();
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.setAttribute('aria-label', on ? 'Sons activés (applaudissements). Toucher pour couper.' : 'Sons coupés. Toucher pour activer les applaudissements.');
    b.title = on ? 'Couper les sons' : 'Activer les sons';
    b.innerHTML = '<svg class="enc-snd-i" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor" stroke-width="1.5"/>' +
      (on ? '<path d="M15.5 9a4.5 4.5 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>' : '<path d="M16 9.5l5 5M21 9.5l-5 5"/>') + '</svg>' +
      '<span class="enc-snd-t">' + (on ? 'Son' : 'Muet') + '</span>';
  }
  function soundButton(cls) {
    var b = doc.createElement('button'); b.type = 'button'; b.className = 'enc-snd' + (cls ? ' ' + cls : '');
    b.addEventListener('click', function () { var on = !soundOn(); setSound(on); if (on) applause(1); });
    buttons.push(b); paint(b);
    return b;
  }
  window.addEventListener('storage', function (e) { if (e.key === SKEY) paintButtons(); });

  var actx = null, master = null, noise = null, VOL = 0.3;
  function ac() {
    if (!actx) {
      var C = window.AudioContext || window.webkitAudioContext; if (!C) return null;
      try { actx = new C(); } catch (e) { return null; }
      var comp = actx.createDynamicsCompressor();
      master = actx.createGain(); master.gain.value = VOL;
      master.connect(comp); comp.connect(actx.destination);
      var len = Math.floor(actx.sampleRate * 1.5); noise = actx.createBuffer(1, len, actx.sampleRate);
      var d = noise.getChannelData(0); for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    }
    if (actx.state === 'suspended') { try { actx.resume(); } catch (e) {} }
    return actx;
  }
  /* Un claquement de mains : bruit blanc bref, filtré autour de 1 à 2 kHz. */
  function clap(t, amp) {
    var s = actx.createBufferSource(), f = actx.createBiquadFilter(), g = actx.createGain();
    s.buffer = noise; f.type = 'bandpass'; f.frequency.value = 900 + Math.random() * 1400; f.Q.value = 0.9 + Math.random() * 0.8;
    var dec = 0.035 + Math.random() * 0.05;
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(amp, t + 0.002); g.gain.exponentialRampToValueAtTime(0.0001, t + dec);
    s.connect(f); f.connect(g); g.connect(master);
    s.start(t, Math.random() * 1.3, dec + 0.02);
  }
  /* Applaudissements : force 1 = courts (bonne réponse), 2 = nourris (série, record). */
  function applause(force) {
    if (!soundOn()) return;
    var a = ac(); if (!a) return;
    var big = force >= 2, people = big ? 11 : 4, dur = big ? 2.1 : 0.85, t0 = a.currentTime + 0.03;
    for (var p = 0; p < people; p++) {
      var rate = 3.6 + Math.random() * 2.4, t = t0 + Math.random() * 0.12, amp = 0.35 + Math.random() * 0.5;
      while (t < t0 + dur) {
        var x = (t - t0) / dur, env = x < 0.12 ? x / 0.12 : x > 0.6 ? Math.max(0, (1 - x) / 0.4) : 1;
        if (env > 0.03) clap(t, amp * env * (big ? 0.55 : 0.8));
        t += (1 / rate) * (0.85 + Math.random() * 0.3);
      }
    }
  }

  /* ── Animations (étoile, confettis discrets) ────────────────────── */
  var COLORS = ['#f5b301', '#ff7a00', '#5fd27c', '#6c8eff', '#ff8fb1', '#2fc7d6'];
  function burst(anchor, n) {
    if (reduce || !doc.body) return;
    var r = anchor && anchor.getBoundingClientRect ? anchor.getBoundingClientRect() : null;
    var x = r && r.width ? r.left + Math.min(r.width / 2, 60) : window.innerWidth / 2, y = r && r.height ? r.top + 10 : window.innerHeight * 0.3;
    x = Math.max(20, Math.min(window.innerWidth - 20, x)); y = Math.max(20, Math.min(window.innerHeight - 20, y));
    var box = doc.createElement('div'); box.className = 'enc-burst'; box.setAttribute('aria-hidden', 'true');
    box.style.left = x + 'px'; box.style.top = y + 'px';
    var h = '<span class="enc-star">★</span>';
    for (var i = 0; i < n; i++) {
      var ang = (Math.PI * 2 * i) / n + Math.random() * 0.5, dist = 40 + Math.random() * (n > 20 ? 110 : 60);
      h += '<i style="--dx:' + Math.round(Math.cos(ang) * dist) + 'px;--dy:' + Math.round(Math.sin(ang) * dist - 20) + 'px;--r:' + Math.round(Math.random() * 540 - 270) + 'deg;' +
        'background:' + COLORS[i % COLORS.length] + ';animation-delay:' + Math.round(Math.random() * 90) + 'ms"></i>';
    }
    box.innerHTML = h; doc.body.appendChild(box);
    setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, 1500);
  }

  /* ── Affichage des phrases ──────────────────────────────────────── */
  var live = null;
  function announce(t) {
    if (!doc.body) return;
    if (!live) { live = doc.createElement('p'); live.className = 'enc-sr'; live.setAttribute('aria-live', 'polite'); doc.body.appendChild(live); }
    live.textContent = ''; setTimeout(function () { live.textContent = t; }, 60);
  }
  /* place (ou remplace) la ligne de phrase juste après « after », ou à la fin de « into » */
  function place(o, cls, html) {
    var target = o.after || o.into; if (!target) return null;
    var line = null;
    if (o.after) { var nx = o.after.nextElementSibling; if (nx && nx.classList.contains('enc-line')) line = nx; }
    else line = o.into.querySelector(':scope > .enc-line');
    if (!line) {
      line = doc.createElement('p');
      if (o.after) o.after.parentNode.insertBefore(line, o.after.nextSibling); else o.into.appendChild(line);
    }
    line.className = 'enc-line ' + cls + (reduce ? '' : ' enc-pop');
    line.innerHTML = html;
    return line;
  }
  function clear(o) {
    var t = o.after ? o.after.nextElementSibling : o.into && o.into.querySelector(':scope > .enc-line');
    if (t && t.classList.contains('enc-line')) t.parentNode.removeChild(t);
  }

  var streak = 0;
  function ok(o) {
    o = o || {};
    streak++;
    var special = streak === 3 || streak === 5 || streak === 10 || (streak > 10 && streak % 5 === 0);
    var text = special ? pick('s' + (streak <= 10 ? streak : 'more'), STREAK[streak <= 10 ? streak : 'more']).replace('{n}', streak) : pick('ok', OK);
    var line = place(o, special ? 'enc-line--ok enc-line--serie' : 'enc-line--ok',
      '<span class="enc-ic" aria-hidden="true">' + (special ? '🏅' : '★') + '</span><span>' + esc(text) + '</span>');
    burst(o.anchor || line, special ? 28 : 12);
    if (o.sound !== false) applause(special ? 2 : 1);
    if (o.announce !== false) announce(text);
    return text;
  }
  function ko(o) {
    o = o || {};
    streak = 0;
    var text = pick('ko', KO), h = o.hint && HINT[o.hint] ? pick('h' + o.hint, HINT[o.hint]) : '';
    place(o, 'enc-line--ko', '<span class="enc-ic" aria-hidden="true">➜</span><span>' + esc(text) + (h ? ' <b>' + esc(h) + '</b>' : '') + '</span>');
    var full = text + (h ? ' ' + h : '');
    if (o.announce !== false) announce(full);
    return full;
  }
  function reset() { streak = 0; }

  /* ── Bilan de fin de partie (progression personnelle) ───────────── */
  var PKEY = 'sigma-encouragements-v1';
  function pload() { try { var d = JSON.parse(localStorage.getItem(PKEY)); return d && d.k ? d : { v: 1, k: {} }; } catch (e) { return { v: 1, k: {} }; } }
  function psave(d) { try { localStorage.setItem(PKEY, JSON.stringify(d)); } catch (e) {} }
  function frDate(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? p[2] + '/' + p[1] : ''; }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function bilan(o) {
    o = o || {};
    var s = Math.max(0, o.score | 0), n = Math.max(0, o.total | 0), r = n ? s / n : 0;
    var d = pload(), key = String(o.key || 'sans-cle'), prev = d.k[key] || null;
    var sq = plural(s, 'question');
    var tier = n && s === n ? 'full' : r >= 0.7 ? 'high' : r >= 0.4 ? 'mid' : s > 0 ? 'low' : 'zero';
    var head = pick('b' + tier, BILAN[tier]).replace('{s}', sq);
    var prog = '', record = false, first = !prev;
    if (!prev) prog = s > 0 ? 'Tu as réussi ' + sq + NB + ': c\'est ton point de départ. La prochaine fois, essaie de faire au moins aussi bien.' : 'C\'est ton premier essai' + NB + ': il te sert de point de départ.';
    else {
      var pr = prev.lt ? prev.l / prev.lt : 0, when = prev.ld === today() ? 'tout à l\'heure' : prev.ld ? 'la dernière fois (le ' + frDate(prev.ld) + ')' : 'la dernière fois';
      var bestR = prev.bt ? prev.b / prev.bt : 0;
      if (r > bestR) { record = true; prog = 'Nouveau record personnel' + NB + ': ' + s + '/' + n + NB + '! ' + 'Avant, ton meilleur score était ' + prev.b + '/' + prev.bt + '.'; }
      else if (r > pr) prog = 'Tu as réussi ' + sq + NB + ': ' + when + ', c\'était ' + prev.l + '. Tu progresses' + NB + '!';
      else if (r === pr) prog = 'Même score que ' + when + ' (' + s + '/' + n + ')' + NB + ': tu consolides tes acquis.';
      else prog = 'Ton meilleur score reste ' + prev.b + '/' + prev.bt + NB + ': tu l\'as déjà fait, tu peux le refaire.';
    }
    var nb = prev ? (prev.n || 1) + 1 : 1;
    if (nb >= 3 && !record) prog += ' C\'est ton essai n°' + NB + nb + NB + ': ta persévérance compte.';
    var keepBest = prev && (prev.bt ? prev.b / prev.bt : 0) >= r;
    d.k[key] = { b: keepBest ? prev.b : s, bt: keepBest ? prev.bt : n, l: s, lt: n, ld: today(), n: nb };
    psave(d);
    var text = o.noHead ? prog : head + ' ' + prog;
    var html = '<span class="enc-ic" aria-hidden="true">' + (record || tier === 'full' ? '🏅' : '★') + '</span><span>' + (o.noHead ? '' : '<b>' + esc(head) + '</b> ') + esc(prog) + '</span>';
    if (o.into || o.after) {
      var line = place(o, 'enc-line--bilan', html);
      if (record || tier === 'full' || tier === 'high') burst(o.anchor || line, 30);
    }
    if (o.sound !== false) applause(record || tier === 'full' || tier === 'high' ? 2 : 1);
    if (o.announce !== false && (o.into || o.after)) announce(text);
    return { html: html, text: text, head: head, record: record, first: first };
  }

  /* ── Branchement automatique sur les panneaux d'un jeu ──────────────
     #win visible  → bonne réponse ; #fb visible avec un nouveau texte → erreur.
     Les simples rappels (« Remplis toutes les cases… ») ne comptent pas. */
  function watch(o) {
    o = o || {};
    var $ = function (s) { return typeof s === 'string' ? doc.querySelector(s) : s; };
    var win = $(o.ok || '#win'), winAfter = $(o.okAfter || '#winp'), fb = $(o.ko || '#fb'), fbAfter = $(o.koAfter || '#fbp');
    var SKIP = o.skip || /^\s*(Remplis|Complète|Choisis|Sélectionne|Écris|Place|Clique|Touche|Entre)\b/i;
    /* structure standard seulement : #win + #winp, #fb (erreurs) + #fbp ; sinon rien n'est branché
       (certains jeux affichent aussi les réussites dans #fb : on n'y touche pas) */
    if (!winAfter || !win || !win.contains(winAfter)) win = null;
    if (!fbAfter || !fb || !fb.contains(fbAfter)) fb = null;
    if (!win && !fb) return false;
    var visible = function (e) { return e && !e.hidden && e.getAttribute('aria-hidden') !== 'true'; };
    var winWas = visible(win), lastFb = '';
    if (win) new MutationObserver(function () {
      var v = visible(win);
      if (v && !winWas) {
        if (win.classList.contains('fail')) clear({ after: winAfter });   /* réponse montrée, pas trouvée */
        else ok({ after: winAfter, anchor: win });
      }
      winWas = v;
    }).observe(win, { attributes: true, attributeFilter: ['hidden', 'aria-hidden'] });
    if (fb && fbAfter) {
      var check = function () {
        if (!visible(fb) || fb.classList.contains('ok')) { lastFb = ''; return; }
        var t = (fbAfter.textContent || '').trim();
        if (!t || t === lastFb) return;
        lastFb = t;
        if (SKIP.test(t)) { clear({ after: fbAfter }); return; }
        ko({ after: fbAfter, hint: (fb.classList.contains('rv') ? 'correction' : 'conseil') });
      };
      var mo = new MutationObserver(function (ms) {
        for (var i = 0; i < ms.length; i++) {
          var tg = ms[i].target;
          if (tg.nodeType === 1 && tg.classList && tg.classList.contains('enc-line')) continue;
          if (tg.parentNode && tg.parentNode.classList && tg.parentNode.classList.contains('enc-line')) continue;
          check(); return;
        }
      });
      mo.observe(fb, { attributes: true, attributeFilter: ['hidden'] });
      mo.observe(fbAfter, { childList: true, characterData: true, subtree: true });
    }
    return true;
  }

  window.SigmaEncourage = {
    ok: ok, ko: ko, bilan: bilan, reset: reset, applause: applause, burst: burst,
    soundOn: soundOn, setSound: setSound, soundButton: soundButton, watch: watch,
    streak: function () { return streak; },
    PHRASES: { ok: OK, ko: KO, indices: HINT, series: STREAK, bilan: BILAN }
  };
  try { doc.dispatchEvent(new CustomEvent('sigma-encourage-ready')); } catch (e) {}
})();
