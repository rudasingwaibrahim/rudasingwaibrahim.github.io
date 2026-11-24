/* Sigma Arcade — musique de fond originale (Web Audio, aucun fichier audio).
   Deux compositions originales :
   - « aventure » : marche héroïque en ré majeur, 4/4, 116 bpm ;
   - « epique »   : saga sombre en ré mineur, 3/4, 126 bpm.
   Démarre au premier geste de l'utilisateur (règle des navigateurs),
   se coupe avec le bouton, mémorise le choix, baisse quand la page est cachée.
   API : SigmaMusic.duck(true|false) baisse le volume (ex. trajets de l'ascenseur). */
(function () {
  'use strict';
  if (window.SigmaMusic) return;
  var STYLE0 = window.SIGMA_MUSIC_STYLE === 'epique' ? 'epique' : 'aventure';
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var on = store.get('sigma-musique', '1') === '1';
  var style = store.get('sigma-musique-style-' + location.pathname, STYLE0);

  /* ---- notes : nom → fréquence ---- */
  var SEMI = { C: -9, D: -7, E: -5, F: -4, G: -2, A: 0, B: 2 };
  function hz(n) { // ex. 'D4', 'F#4', 'Bb3'
    var m = /^([A-G])([#b]?)(\d)$/.exec(n); if (!m) return 0;
    var s = SEMI[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0) + (parseInt(m[3], 10) - 4) * 12;
    return 440 * Math.pow(2, s / 12);
  }
  /* séquence compacte : "note:durée note:durée …" (durée en temps ; '-' = silence) */
  function seq(str) {
    var t = 0, out = [];
    str.trim().split(/\s+/).forEach(function (tok) {
      var p = tok.split(':'), d = parseFloat(p[1]);
      if (p[0] !== '-') out.push({ t: t, d: d, f: hz(p[0]) });
      t += d;
    });
    return { ev: out, len: t };
  }

  /* ================= compositions originales ================= */
  var SONGS = {
    aventure: { bpm: 116, beats: 4, bars: 8,
      lead: seq(
        'D4:1 A4:0.5 F#4:0.5 A4:1 D5:1 ' +
        'C#5:0.75 B4:0.25 A4:1 G4:1 -:1 ' +
        'B4:1 D5:0.5 B4:0.5 G4:1 B4:1 ' +
        'A4:1.5 G4:0.5 F#4:1 E4:1 ' +
        'F#4:1 A4:0.5 D5:0.5 F#5:1 E5:1 ' +
        'D5:0.75 C#5:0.25 B4:1 G4:1 B4:1 ' +
        'A4:1 E4:0.5 G4:0.5 C#5:1 B4:0.5 C#5:0.5 ' +
        'D5:2 A4:1 -:1'),
      bass: seq(
        'D2:1 D3:1 A2:1 D3:1  G2:1 G3:1 D3:1 G3:1  G2:1 G3:1 D3:1 B2:1  A2:1 A3:1 E3:1 A2:1 ' +
        'D2:1 D3:1 A2:1 F#2:1 G2:1 G3:1 B2:1 G2:1  A2:1 A3:1 E3:1 C#3:1 D2:1 A2:1 D3:1 -:1'),
      chords: [['D3','F#3','A3'],['G3','B3','D4'],['G3','B3','D4'],['A3','C#4','E4'],
               ['D3','F#3','A3'],['G3','B3','D4'],['A3','C#4','E4'],['D3','F#3','A3']],
      drums: 'march', leadType: 'brass' },
    epique: { bpm: 126, beats: 3, bars: 8,
      lead: seq(
        'D5:2 C5:1  Bb4:3  A4:2 G4:1  A4:2 -:1 ' +
        'F4:1 G4:1 A4:1  Bb4:2 D5:1  C5:1.5 Bb4:0.5 A4:1  D4:3'),
      bass: seq(
        'D2:1 A2:1 D3:1  Bb1:1 F2:1 Bb2:1  C2:1 G2:1 C3:1  A1:1 E2:1 A2:1 ' +
        'D2:1 A2:1 D3:1  G1:1 D2:1 G2:1  A1:1 E2:1 A2:1  D2:1 A2:1 D3:1'),
      chords: [['D3','F3','A3'],['Bb2','D3','F3'],['C3','E3','G3'],['A2','C#3','E3'],
               ['D3','F3','A3'],['G2','Bb2','D3'],['A2','C#3','E3'],['D3','F3','A3']],
      drums: 'war', leadType: 'strings' }
  };

  /* ================= moteur ================= */
  var ctx = null, master = null, duckG = null, timer = null, nextT = 0, beat = 0, playing = false;
  function audio() {
    if (!ctx) {
      try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; }
      master = ctx.createGain(); master.gain.value = 0;
      duckG = ctx.createGain(); duckG.gain.value = 1;
      var comp = ctx.createDynamicsCompressor();
      master.connect(duckG); duckG.connect(comp); comp.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function env(g, t, a, peak, dur, rel) {
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(peak, t + a);
    g.gain.setValueAtTime(peak, t + Math.max(a, dur - rel));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur + rel);
  }
  function lead(f, t, dur, type) {
    var o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), lp = ctx.createBiquadFilter(), g = ctx.createGain();
    o1.type = 'sawtooth'; o2.type = type === 'brass' ? 'square' : 'sawtooth';
    o1.frequency.value = f; o2.frequency.value = f; o2.detune.value = type === 'brass' ? -6 : 9;
    lp.type = 'lowpass'; lp.Q.value = type === 'brass' ? 2 : 0.7;
    lp.frequency.setValueAtTime(type === 'brass' ? 700 : 900, t);
    lp.frequency.linearRampToValueAtTime(type === 'brass' ? 2200 : 1500, t + Math.min(0.12, dur / 2));
    o1.connect(lp); o2.connect(lp); lp.connect(g); g.connect(master);
    env(g, t, type === 'brass' ? 0.03 : 0.12, type === 'brass' ? 0.11 : 0.09, dur, type === 'brass' ? 0.08 : 0.25);
    o1.start(t); o2.start(t); o1.stop(t + dur + 0.4); o2.stop(t + dur + 0.4);
  }
  function bass(f, t, dur) {
    var o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'triangle'; o.frequency.value = f;
    o.connect(g); g.connect(master); env(g, t, 0.01, 0.16, dur * 0.9, 0.06); o.start(t); o.stop(t + dur + 0.2);
  }
  function pad(notes, t, dur) {
    notes.forEach(function (n) {
      var o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine'; o.frequency.value = hz(n);
      o.connect(g); g.connect(master); env(g, t, 0.25, 0.028, dur, 0.4); o.start(t); o.stop(t + dur + 0.6);
    });
  }
  var noiseBuf = null;
  function noise(t, dur, vol, freq) {
    if (!noiseBuf) { noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.5, ctx.sampleRate); var d = noiseBuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
    var s = ctx.createBufferSource(), bp = ctx.createBiquadFilter(), g = ctx.createGain();
    s.buffer = noiseBuf; bp.type = 'bandpass'; bp.frequency.value = freq; bp.Q.value = 0.8;
    s.connect(bp); bp.connect(g); g.connect(master); env(g, t, 0.002, vol, dur, dur); s.start(t); s.stop(t + dur * 2 + 0.05);
  }
  function drum(t, f0, f1, dur, vol) {
    var o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine';
    o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f1, t + dur);
    o.connect(g); g.connect(master); env(g, t, 0.003, vol, dur, dur * 0.5); o.start(t); o.stop(t + dur + 0.1);
  }
  function drums(kind, b, t, spb, beats) {
    var pos = b % beats;
    if (kind === 'march') {
      if (pos === 0 || pos === 2) drum(t, 130, 45, 0.18, 0.22);
      if (pos === 1 || pos === 3) noise(t, 0.09, 0.07, 1800);
      noise(t + spb / 2, 0.05, 0.03, 2600);                       // roulement léger à la croche
      if (pos === 3) noise(t + spb * 0.75, 0.05, 0.035, 2200);
    } else {
      if (pos === 0) { drum(t, 95, 38, 0.45, 0.3); }
      if (pos === 2) drum(t + spb / 2, 140, 70, 0.2, 0.12);
      if (pos === 1) noise(t, 0.16, 0.035, 900);
    }
  }
  function schedule() {
    var S = SONGS[style], spb = 60 / S.bpm, total = S.beats * S.bars;
    while (nextT < ctx.currentTime + 0.25) {
      var b = beat % total;
      S.lead.ev.forEach(function (e) { if (e.t >= b && e.t < b + 1) lead(e.f, nextT + (e.t - b) * spb, e.d * spb * 0.95, S.leadType); });
      S.bass.ev.forEach(function (e) { if (e.t >= b && e.t < b + 1) bass(e.f, nextT + (e.t - b) * spb, e.d * spb); });
      if (b % S.beats === 0) pad(S.chords[(b / S.beats) % S.chords.length], nextT, S.beats * spb);
      drums(S.drums, b, nextT, spb, S.beats);
      nextT += spb; beat++;
    }
  }
  function start() {
    if (playing || !on || document.hidden) return;
    if (!audio()) return;
    playing = true; beat = 0; nextT = ctx.currentTime + 0.12;
    master.gain.cancelScheduledValues(ctx.currentTime);
    master.gain.setValueAtTime(0, ctx.currentTime); master.gain.linearRampToValueAtTime(0.55, ctx.currentTime + 1.5);
    schedule(); timer = setInterval(schedule, 60);
  }
  function stop() {
    if (!playing) return; playing = false; clearInterval(timer);
    master.gain.cancelScheduledValues(ctx.currentTime);
    master.gain.setValueAtTime(master.gain.value, ctx.currentTime); master.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.4);
  }
  function duck(x) {
    if (!ctx) return; var t = ctx.currentTime;
    duckG.gain.cancelScheduledValues(t); duckG.gain.setValueAtTime(duckG.gain.value, t);
    duckG.gain.linearRampToValueAtTime(x ? 0.18 : 1, t + (x ? 0.25 : 0.8));
  }

  /* ================= bouton flottant ================= */
  var css = '.smus{position:absolute;top:12px;right:max(12px,env(safe-area-inset-right));z-index:9000;display:flex;gap:6px;font:600 14px Outfit,system-ui,sans-serif}' +
    '.smus button{min-height:44px;padding:0 14px;border-radius:999px;border:1.5px solid rgba(120,160,255,.32);background:rgba(10,22,40,.92);color:#f0f4ff;cursor:pointer;box-shadow:0 6px 18px -8px rgba(0,0,0,.35);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);font:inherit}' +
    '.smus button[aria-pressed=true]{background:#6c8eff;color:#071022;border-color:#6c8eff}' +
    '.smus .sty{font-size:13px}.smus button:focus-visible{outline:3px solid #6c8eff;outline-offset:2px}' +
    '@media(max-width:520px){.smus .sty{display:none}.smus button{min-height:44px;padding:0 12px;font-size:13px}}' +
    '@media print{.smus{display:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var box = document.createElement('div'); box.className = 'smus'; box.setAttribute('aria-label', 'Musique de fond');
  var bOn = document.createElement('button'), bSty = document.createElement('button');
  bOn.type = bSty.type = 'button'; bSty.className = 'sty';
  function label() {
    bOn.setAttribute('aria-pressed', on ? 'true' : 'false');
    bOn.textContent = on ? '♪ Musique : oui' : '♪ Musique : non';
    bSty.textContent = style === 'epique' ? 'Style : épique' : 'Style : aventure';
  }
  bOn.addEventListener('click', function (e) {
    e.stopPropagation(); on = !on; store.set('sigma-musique', on ? '1' : '0'); label();
    if (on) start(); else stop();
  });
  bSty.addEventListener('click', function (e) {
    e.stopPropagation(); style = style === 'epique' ? 'aventure' : 'epique';
    store.set('sigma-musique-style-' + location.pathname, style); label();
    if (playing) { stop(); setTimeout(start, 450); }
  });
  box.appendChild(bSty); box.appendChild(bOn);
  function mount() { document.body.appendChild(box); label(); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);

  /* premier geste : la musique peut démarrer */
  function first() { start(); }
  ['pointerdown', 'keydown'].forEach(function (ev) { document.addEventListener(ev, first, { once: true, capture: true }); });
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else if (on && ctx) start(); });

  window.SigmaMusic = { start: start, stop: stop, duck: duck, isOn: function () { return on; } };
})();
