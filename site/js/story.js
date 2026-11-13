// A viagem da gotícula: o começo da página é uma tela fixa em que o scroll
// comanda o vídeo da onda, a gotícula 3D, as legendas e o painel r/T/m.
// Depois dela, o fundo vira o mar por dentro e a gotícula segue as seções.

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile = () => window.innerWidth <= 860;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const lerp = (a, b, t) => a + (b - a) * t;
const smooth = (t) => t * t * (3 - 2 * t);
const ss = (a, b, x) => smooth(clamp01((x - a) / (b - a)));

// Interpolação por trechos: P são os pontos do scroll, V os valores
function piecewise(P, V, p, ease = (t) => t) {
  if (p <= P[0]) return V[0];
  for (let i = 1; i < P.length; i++) {
    if (p <= P[i]) return lerp(V[i - 1], V[i], ease((p - P[i - 1]) / (P[i] - P[i - 1])));
  }
  return V[V.length - 1];
}

/* --------------------------- Tempo do vídeo ----------------------------- */
// O arquivo começa em 129,5 s do vídeo original. A câmera lenta fica no spray.
const VID_P = [0, 0.12, 0.30, 0.60, 0.80, 1];
const VID_T = [0, 6.5, 10.0, 11.5, 15.5, 20.4];

/* -------------------------- Caminho da gotícula ------------------------- */
// x e y em frações da tela, r em frações do menor lado. A primeira chave
// é a crista da onda (calculada a partir do vídeo, ver crest()).
const PATH = [
  // p      x      y      r      alpha
  [0.12,  null,  null,  0.012, 0],
  [0.16,  null,  null,  0.035, 1],
  [0.26,  0.64,  0.30,  0.12,  1],
  [0.34,  0.66,  0.42,  0.20,  1],
  [0.58,  0.645, 0.44,  0.215, 1],
  [0.66,  0.60,  0.56,  0.18,  1],
  [0.792, 0.52,  1.30,  0.14,  1],
  [0.80,  0.50, -0.30,  0.14,  1],   // corte: a câmera agora está debaixo d'água
  [0.87,  0.50,  0.40,  0.15,  1],
  [0.94,  0.50,  0.58,  0.135, 1],
  [1.00,  0.50,  0.66,  0.12,  0],
];
const PATH_MOBILE_Y = (y) => (y === null ? null : y < 0 || y > 1 ? y : 0.2 + y * 0.52);
const PATH_MOBILE_X = (x) => (x === null ? null : lerp(0.5, x, 0.35));

/* -------------------------- Números do painel --------------------------- */
// Referência SCONTROL do TCC, gotícula de 500 µm (legendas dos gráficos em
// manim/imagens/). As curvas quase não mudam no começo e aceleram no fim.
const REF = { tau: 0.72, r0: 500, r1: 499.987, T0: 19.80, T1: 19.37, m0: 6.500, m1: 6.560 };

/* --------------------- Quadros da onda (celular) ------------------------ */
// No celular, pular de um ponto a outro de um vídeo é lento e o scroll engasga.
// Por isso lá a onda vem de 150 imagens em retrato (site/media/frames/), uma para
// cada passo do scroll (já com a câmera lenta embutida), desenhadas num canvas.
const FRAMES = { n: 150, w: 406, h: 720, src: (i) => `site/media/frames/m${String(i).padStart(3, '0')}.webp` };
const fmt = (v, d) => v.toFixed(d).replace('.', ',');

export function initStory({ onDrop } = {}) {
  const stageEl = $('#viagem');
  const video = $('#waveVideo');
  const caps = $$('.cap', stageEl);
  const hud = $('#hud');
  const tag = $('#co2tag');
  const bar = $('#stageBar');
  const fallbackDrop = $('#stageDrop');
  const deepVideo = $('#deepVideo');
  const pin = $('.stage__pin', stageEl);
  const html = document.documentElement;
  let drop = null;
  let lenis = null;
  const useFrames = !reduced && window.matchMedia('(max-width: 860px), (pointer: coarse)').matches;
  // altura da tela fixa: estável mesmo quando a barra do navegador do celular some
  const pinH = () => pin.offsetHeight || window.innerHeight;

  /* ------------------------- Rolagem suave ------------------------------ */
  if (!reduced && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.09, wheelMultiplier: 0.95, touchMultiplier: 1.4 });
    html.classList.add('has-lenis');
    // links internos também passam pelo Lenis
    $$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      lenis.scrollTo(el, { offset: id === '#viagem' ? 0 : -64, duration: 1.6 });
      history.replaceState(null, '', id);
    }));
  }
  const scrollTo = (target, opts) => (lenis ? lenis.scrollTo(target, opts) : (typeof target === 'number' ? window.scrollTo({ top: target, behavior: reduced ? 'auto' : 'smooth' }) : target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' })));
  $$('[data-to-top]').forEach((b) => b.addEventListener('click', () => scrollTo(0, { duration: 2.2 })));

  /* ---------------------- Vídeo da onda (scrub) ------------------------- */
  let seeking = false;
  let wantT = 0;
  let videoOk = false;
  function seekTo(t) {
    wantT = t;
    if (!videoOk || seeking) return;
    if (Math.abs(video.currentTime - t) < 0.025) return;
    seeking = true;
    video.currentTime = t;
  }
  video.addEventListener('seeked', () => { seeking = false; if (Math.abs(video.currentTime - wantT) >= 0.025) seekTo(wantT); });

  if (!reduced && !useFrames) {
    // Baixa o vídeo inteiro antes: assim pular de um quadro para outro é imediato
    const src = video.dataset.src;
    fetch(src)
      .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.blob(); })
      .then((blob) => { video.src = URL.createObjectURL(blob); })
      .catch(() => { video.src = src; })
      .finally(() => {
        video.addEventListener('loadeddata', () => { videoOk = true; html.classList.add('wave-ready'); seekTo(wantT); }, { once: true });
        video.load();
      });
    // iOS só libera a busca de quadros depois de um toque
    window.addEventListener('touchstart', () => { video.play().then(() => video.pause()).catch(() => {}); }, { once: true, passive: true });
  }

  /* ------------------- Quadros num canvas (celular) --------------------- */
  let framesCanvas = null, fctx = null, bgCanvas = null, bgCtx = null;
  const imgs = new Array(FRAMES.n).fill(null);
  let drawnKey = '';
  if (useFrames) {
    html.classList.add('frames-mode');
    framesCanvas = document.createElement('canvas');
    framesCanvas.className = 'stage__frames';
    framesCanvas.setAttribute('aria-hidden', 'true');
    video.after(framesCanvas);
    fctx = framesCanvas.getContext('2d', { alpha: false });
    // cópia pequena só para a refração da gota: subir a tela inteira para a placa
    // de vídeo a cada quadro pesaria no celular, e dentro da gota ninguém nota a diferença
    bgCanvas = document.createElement('canvas');
    bgCtx = bgCanvas.getContext('2d', { alpha: false });
    // carrega em passadas: primeiro um quadro a cada 16, depois preenche os buracos,
    // assim a viagem já funciona inteira (mais "pulada") enquanto o resto chega
    const order = [];
    for (const step of [16, 8, 4, 2, 1]) for (let i = 0; i < FRAMES.n; i += step) if (!order.includes(i)) order.push(i);
    let next = 0;
    const load = () => {
      if (next >= order.length) return;
      const i = order[next++];
      const im = new Image();
      im.decoding = 'async';
      im.src = FRAMES.src(i);
      im.decode().then(() => { imgs[i] = im; drawnKey = ''; if (i === 0) html.classList.add('wave-ready'); }).catch(() => {}).finally(load);
    };
    for (let k = 0; k < 6; k++) load();   // seis downloads em paralelo
  }
  const nearest = (i, dir) => { for (let k = i; k >= 0 && k < FRAMES.n; k += dir) if (imgs[k]) return k; return -1; };
  function drawFrames(p) {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = window.innerWidth, H = pinH();
    const cw = Math.round(W * dpr), ch = Math.round(H * dpr);
    if (framesCanvas.width !== cw || framesCanvas.height !== ch) { framesCanvas.width = cw; framesCanvas.height = ch; drawnKey = ''; }
    const f = p * (FRAMES.n - 1);
    let a = nearest(Math.floor(f), -1), b = nearest(Math.ceil(f), 1);
    if (a < 0) a = b; if (b < 0) b = a;
    if (a < 0) return;
    const t = b === a ? 0 : clamp01((f - a) / (b - a));
    const key = `${a}|${b}|${t.toFixed(3)}|${cw}x${ch}`;
    if (key === drawnKey) return;
    drawnKey = key;
    // "cover": preenche a tela inteira sem distorcer
    const s = Math.max(cw / FRAMES.w, ch / FRAMES.h);
    const dw = FRAMES.w * s, dh = FRAMES.h * s, dx = (cw - dw) / 2, dy = (ch - dh) / 2;
    fctx.globalAlpha = 1;
    fctx.drawImage(imgs[a], dx, dy, dw, dh);
    // mistura com o quadro seguinte: o movimento fica contínuo entre um e outro
    if (t > 0.02 && b !== a) { fctx.globalAlpha = t; fctx.drawImage(imgs[b], dx, dy, dw, dh); }
    const bw = 240, bh = Math.round(240 * ch / cw);
    if (bgCanvas.width !== bw || bgCanvas.height !== bh) { bgCanvas.width = bw; bgCanvas.height = bh; }
    bgCtx.drawImage(framesCanvas, 0, 0, bw, bh);
    bgCanvas.dataset.ready = '1';
    drop?.bgDirty?.();
  }

  /* ------------------------- Mar por dentro ----------------------------- */
  let deepOn = false;
  function wakeDeep() {
    if (deepOn || !deepVideo) return;
    deepOn = true;
    deepVideo.src = deepVideo.dataset.src;
    deepVideo.play().catch(() => {});
  }
  // bolhas subindo
  const bubbles = $('.deep__bubbles');
  if (bubbles && !reduced) {
    const n = mobile() ? 14 : 26;
    for (let i = 0; i < n; i++) {
      const b = document.createElement('i');
      const size = 3 + Math.random() * 9;
      b.style.cssText = `left:${Math.random() * 100}%;width:${size}px;height:${size}px;animation-duration:${9 + Math.random() * 14}s;animation-delay:${-Math.random() * 20}s;--sway:${(Math.random() * 2 - 1) * 40}px`;
      bubbles.append(b);
    }
  }

  /* ------------------------------ Trilho -------------------------------- */
  const railName = $('#railName');
  const railDots = $$('.rail__dots button');
  const chapters = $$('[data-chapter]');
  railDots.forEach((b, i) => b.addEventListener('click', () => {
    const el = chapters[i];
    if (el) scrollTo(el, { offset: i === 0 ? 0 : -64, duration: 1.6 });
  }));
  const foot = $('.foot');
  const chapterObs = new IntersectionObserver((entries) => {
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      // o rodapé conta como parte da última seção (Materiais)
      const i = en.target === foot ? chapters.length - 1 : chapters.indexOf(en.target);
      if (en.target === foot && railName) railName.textContent = chapters[i].dataset.chapter;
      railDots.forEach((b, k) => b.classList.toggle('is-on', k === i));
      if (i > 0 && railName) railName.textContent = en.target.dataset.chapter;
      $$('.nav__links a').forEach((a) => a.classList.toggle('is-on', a.getAttribute('href') === `#${en.target.id}`));
    }
  }, { rootMargin: '-45% 0px -50% 0px' });
  chapters.forEach((c) => chapterObs.observe(c));
  if (foot) chapterObs.observe(foot);

  /* --------------------------- Crista da onda --------------------------- */
  // Onde fica, na tela, o ponto da crista em que a gota nasce (no quadro do vídeo)
  function crest() {
    const W = window.innerWidth, H = pinH();
    const vw = useFrames ? FRAMES.w : video.videoWidth || 1280, vh = useFrames ? FRAMES.h : video.videoHeight || 720;
    const s = Math.max(W / vw, H / vh);
    const ox = (W - vw * s) / 2, oy = (H - vh * s) / 2;
    const u = mobile() ? 0.5 : 0.56, v = 0.46;
    return [(ox + u * vw * s) / W, (oy + v * vh * s) / H];
  }

  function dropAt(p) {
    const W = window.innerWidth, H = pinH(), mn = Math.min(W, H);
    const [cxF, cyF] = crest();
    const keys = PATH.map(([kp, x, y, r, a]) => {
      let X = x ?? cxF, Y = y ?? cyF;
      if (mobile()) { X = x === null ? cxF : PATH_MOBILE_X(x); Y = y === null ? cyF : PATH_MOBILE_Y(y); }
      // nasce na crista e sobe um pouco
      if (x === null && kp > 0.12) Y -= 0.04;
      return [kp, X, Y, mobile() ? r * 1.45 : r, a];
    });
    const P = keys.map((k) => k[0]);
    const pick = (j) => keys.map((k) => k[j]);
    const x = piecewise(P, pick(1), p, smooth) * W;
    const y = piecewise(P, pick(2), p, smooth) * H;
    const r = piecewise(P, pick(3), p, smooth) * mn;
    const alpha = p < 0.12 ? 0 : piecewise(P, pick(4), p);
    return { x, y, r, alpha };
  }

  /* ------------------- Botões da animação (passos) ---------------------- */
  const stepBtns = $$('.stage__step', stageEl);
  const playBtn = $('#stagePlay');
  const yAt = (p) => stageEl.offsetTop + (stageEl.offsetHeight - pinH()) * p;
  const pNow = () => clamp01((window.scrollY - stageEl.offsetTop) / Math.max(1, stageEl.offsetHeight - pinH()));
  let playing = false;
  let manual = 0;   // animação de reserva, sem o Lenis
  function stopPlay() {
    if (!playing) return;
    playing = false;
    cancelAnimationFrame(manual);
    if (lenis) lenis.scrollTo(window.scrollY, { immediate: true, force: true });
    playBtn?.classList.remove('is-playing');
    playBtn?.setAttribute('aria-label', 'Ver a animação inteira');
  }
  function glide(y, duration, done) {
    if (lenis) { lenis.scrollTo(y, { duration, easing: (t) => t, force: true, onComplete: done }); return; }
    const y0 = window.scrollY, t0 = performance.now();
    const step = (now) => {
      const k = Math.min(1, (now - t0) / (duration * 1000));
      window.scrollTo(0, y0 + (y - y0) * k);
      if (k < 1) manual = requestAnimationFrame(step); else done?.();
    };
    manual = requestAnimationFrame(step);
  }
  // "Ver tudo": percorre a viagem sozinha, do ponto atual até o fim
  playBtn?.addEventListener('click', () => {
    if (playing) { stopPlay(); return; }
    let p = pNow();
    if (p > 0.97 || stageEl.getBoundingClientRect().top > 1) {
      window.scrollTo(0, yAt(0)); lenis?.scrollTo(yAt(0), { immediate: true, force: true }); p = 0;
    }
    playing = true;
    playBtn.classList.add('is-playing');
    playBtn.setAttribute('aria-label', 'Pausar a animação');
    glide(yAt(1), Math.max(2, (1 - p) * 18), () => { playing = false; playBtn.classList.remove('is-playing'); playBtn.setAttribute('aria-label', 'Ver a animação inteira'); });
  });
  // cada passo leva direto àquele momento
  stepBtns.forEach((b) => b.addEventListener('click', () => {
    stopPlay();
    const target = +b.dataset.p;
    const dist = Math.abs(target - pNow());
    scrollTo(yAt(target), { duration: 0.8 + dist * 2.2, force: true });
  }));
  // mexer na página por conta própria interrompe o "Ver tudo"
  for (const ev of ['wheel', 'touchstart', 'keydown']) window.addEventListener(ev, (e) => { if (playing && !(e.target instanceof Element && e.target.closest('.stage__bar'))) stopPlay(); }, { passive: true });

  /* ------------------------------ Painel -------------------------------- */
  const hudT = $('#hudT'), hudR = $('#hudR'), hudTemp = $('#hudTemp'), hudM = $('#hudM'), hudFill = $('#hudFill');
  function updateHud(p) {
    const s = clamp01((p - 0.16) / (0.79 - 0.16));
    const g = Math.pow(s, 2.3);
    hudT.textContent = fmt(REF.tau * s, 3);
    hudR.textContent = fmt(lerp(REF.r0, REF.r1, g), 3);
    hudTemp.textContent = fmt(lerp(REF.T0, REF.T1, g), 2);
    hudM.textContent = fmt(lerp(REF.m0, REF.m1, g), 3);
    hudFill.style.transform = `scaleX(${s.toFixed(4)})`;
    hud.classList.toggle('is-on', p > 0.3 && p < 0.8);
  }

  /* ------------------------------ Quadro -------------------------------- */
  let lastP = -1;
  function frame() {
    requestAnimationFrame(frame);
    const rect = stageEl.getBoundingClientRect();
    const H = pinH();
    const total = Math.max(1, stageEl.offsetHeight - H);
    const p = clamp01(-rect.top / total);
    const inStage = rect.bottom > 1 && rect.top < H;

    if (rect.bottom < H * 1.6) wakeDeep();
    html.classList.toggle('in-stage', rect.bottom > 56);
    // o mar escurece conforme se desce na página
    const below = Math.max(0, -rect.bottom) / Math.max(1, document.documentElement.scrollHeight - stageEl.offsetHeight - H);
    html.style.setProperty('--depth', clamp01(below).toFixed(3));

    if (!inStage) {
      if (lastP !== -2) { drop?.setStage(null); tag?.classList.remove('is-on'); lastP = -2; }
      return;
    }
    if (railName) {
      const phase = p < 0.12 ? 'A viagem' : p < 0.3 ? 'Na crista' : p < 0.6 ? 'No ar' : p < 0.8 ? 'A queda' : 'No oceano';
      if (railName.textContent !== phase) railName.textContent = phase;
    }

    if (useFrames) drawFrames(p);
    else seekTo(piecewise(VID_P, VID_T, p));

    // legendas
    for (const c of caps) {
      const a = +c.dataset.from, b = +c.dataset.to;
      const v = (a <= 0 ? 1 : ss(a, a + 0.035, p)) * (b >= 1 ? 1 : 1 - ss(b - 0.035, b, p));
      c.style.opacity = v.toFixed(3);
      c.style.transform = `translate3d(0, ${((1 - v) * (p < a + 0.04 ? 30 : -30)).toFixed(1)}px, 0)`;
      c.classList.toggle('is-on', v > 0.5);
    }
    updateHud(p);
    if (bar) bar.style.transform = `scaleX(${p.toFixed(4)})`;
    const phaseIdx = p < 0.12 ? -1 : p < 0.3 ? 0 : p < 0.6 ? 1 : p < 0.8 ? 2 : 3;
    stepBtns.forEach((b, i) => { b.classList.toggle('is-on', i === phaseIdx); b.toggleAttribute('aria-current', i === phaseIdx); });

    // gotícula
    const d = dropAt(p);
    const st = {
      ...d,
      temp: clamp01((p - 0.16) / 0.63),
      absorb: ss(0.30, 0.58, p),
      release: ss(0.82, 0.97, p),
      air: ss(0.19, 0.29, p),
      video: useFrames ? bgCanvas : video,
      gain: useFrames ? 0.72 : 0.62,
    };
    if (drop) drop.setStage(st);
    if (fallbackDrop) {
      fallbackDrop.style.transform = `translate3d(${d.x - d.r}px, ${d.y - d.r}px, 0)`;
      fallbackDrop.style.width = fallbackDrop.style.height = `${(d.r * 2).toFixed(1)}px`;
      fallbackDrop.style.opacity = d.alpha.toFixed(3);
      fallbackDrop.style.setProperty('--fill', st.absorb.toFixed(3));
    }

    // rótulo "CO₂" preso numa molécula que ainda está no ar
    if (tag && drop) {
      const showTag = p > 0.22 && p < 0.42;
      const m = showTag ? drop.nearestAirMolecule() : null;
      if (m) { tag.style.transform = `translate3d(${m.x.toFixed(1)}px, ${m.y.toFixed(1)}px, 0)`; }
      tag.classList.toggle('is-on', !!m);
    }
    lastP = p;
  }

  if (!reduced) requestAnimationFrame(frame);
  else {
    // movimento reduzido: cada legenda vira um quadro fixo com a cena por trás
    for (const c of caps) c.style.backgroundImage = `linear-gradient(180deg, rgba(1, 14, 26, 0.2), rgba(1, 14, 26, 0.85)), url("${c.dataset.poster}")`;
    const watch = () => document.documentElement.classList.toggle('in-stage', stageEl.getBoundingClientRect().bottom > 56);
    window.addEventListener('scroll', watch, { passive: true });
    watch();
    wakeDeep();
  }

  function raf(t) { lenis?.raf(t); requestAnimationFrame(raf); }
  if (lenis) requestAnimationFrame(raf);

  /* ---------------------------- Gotícula 3D ----------------------------- */
  import('./droplet.js?v=12')
    .then(({ initDroplet }) => {
      drop = initDroplet({ canvas: $('#drop'), reducedMotion: reduced });
      if (!drop) throw new Error('sem gotícula');
      onDrop?.(drop);
    })
    .catch((err) => {
      console.warn('Gotícula 3D indisponível:', err);
      html.classList.add('no-webgl');
    });

  /* ------------- Rótulos r(t), T(t), m(t) e a gota ilustrada ------------- */
  // passar o mouse ou o dedo num rótulo destaca a parte correspondente da gota
  const ring = $('.stage-ring');
  $$('.callout').forEach((c) => {
    const on = () => { ring?.classList.add(`hl-${c.dataset.hl}`); c.classList.add('is-on'); };
    const off = () => { ring?.classList.remove(`hl-${c.dataset.hl}`); c.classList.remove('is-on'); };
    c.addEventListener('pointerenter', on);
    c.addEventListener('pointerleave', off);
    c.addEventListener('focus', on);
    c.addEventListener('blur', off);
  });

  return { scrollTo };
}
