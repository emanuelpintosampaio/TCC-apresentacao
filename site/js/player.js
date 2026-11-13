// Player dos slides do Manim.
//
// A lista de vídeos é lida do HTML gerado pelo manim-slides, então basta gerar
// os slides de novo para o player acompanhar. Se a ordem ou a quantidade de
// slides mudar, ajuste só os capítulos abaixo ("slide" começa em 0).

const SOURCE = 'apresentacao(2).html';

const CHAPTERS = [
  { title: 'Capa', slide: 1 },
  { title: 'Estrutura', slide: 3 },
  { title: 'Motivação', slide: 5 },
  { title: 'A gotícula', slide: 9 },
  { title: 'Modelos', slide: 10 },
  { title: 'Métodos numéricos', slide: 26 },
  { title: '1º objetivo', slide: 32 },
  { title: 'Passo de tempo', slide: 40 },
  { title: '2º objetivo', slide: 53 },
  { title: 'Encerramento', slide: 59 },
];

// O primeiro vídeo é um quadro em branco; a capa é o segundo
const START = 1;

async function loadSlides() {
  const res = await fetch(SOURCE);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const doc = new DOMParser().parseFromString(await res.text(), 'text/html');
  const slides = [...doc.querySelectorAll('section[data-background-video]')].map((s) => ({
    src: s.getAttribute('data-background-video'),
    bg: s.getAttribute('data-background-color') || 'white',
    muted: s.hasAttribute('data-background-video-muted'),
  }));
  if (!slides.length) throw new Error('nenhum slide encontrado');
  return slides;
}

export function initPlayer(root) {
  if (!root) return null;
  const $ = (id) => root.querySelector(id);
  const screen = $('#playerScreen');
  const videos = [...root.querySelectorAll('.player__video')];
  const poster = $('#playerPoster');
  const msg = $('#playerMsg');
  const count = $('#pCount');
  const chapterLabel = $('#pChapter');
  const progress = $('#playerProgress');
  const chaptersBox = $('#pChapters');

  let slides = [];
  let chapters = [];
  let idx = -1;
  let front = 0;
  let token = 0;
  let started = false;
  let idleTimer = 0;

  const ready = loadSlides().then((list) => {
    slides = list;
    chapters = CHAPTERS.filter((c) => c.slide < slides.length);
    buildChapters();
    updateUI();
  }).catch((err) => {
    console.warn('Player: não foi possível ler a lista de slides.', err);
    msg.textContent = 'Não foi possível carregar os slides agora. Recarregue a página para tentar de novo.';
    msg.hidden = false;
    poster.hidden = true;
    throw err;
  });
  ready.catch(() => {});

  function buildChapters() {
    chaptersBox.textContent = '';
    progress.querySelectorAll('i').forEach((el) => el.remove());
    chapters.forEach((c, k) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = c.title;
      b.dataset.k = k;
      b.addEventListener('click', () => { begin(); show(c.slide); });
      chaptersBox.append(b);
      if (k > 0) {
        const mark = document.createElement('i');
        mark.style.left = `${(c.slide / (slides.length - 1)) * 100}%`;
        progress.append(mark);
      }
    });
  }

  function currentChapter() {
    let k = -1;
    chapters.forEach((c, j) => { if (idx >= c.slide) k = j; });
    return k;
  }

  function updateUI() {
    const n = slides.length;
    count.textContent = n ? `${Math.max(idx, 0) + 1} / ${n}` : '0 / 0';
    progress.firstElementChild.style.width = n > 1 && idx >= 0 ? `${(idx / (n - 1)) * 100}%` : '0%';
    const k = currentChapter();
    chapterLabel.textContent = k >= 0 ? chapters[k].title : '';
    chaptersBox.querySelectorAll('button').forEach((b) => b.classList.toggle('is-on', Number(b.dataset.k) === k));
    root.classList.toggle('is-playing', idx >= 0 && !videos[front].paused && !videos[front].ended);
  }

  function setSource(video, slide) {
    if (video.dataset.src === slide.src) return;
    video.dataset.src = slide.src;
    video.preload = 'auto';
    video.src = slide.src;
    video.load();
  }

  // Deixa o próximo slide carregado no vídeo que está escondido.
  // O último (o vídeo longo do encerramento) só é baixado quando chega a vez dele.
  function preloadNext() {
    const next = idx + 1;
    if (next >= slides.length - 1) return;
    setSource(videos[1 - front], slides[next]);
  }

  function show(i, { atEnd = false } = {}) {
    if (!slides.length) return;
    i = Math.min(slides.length - 1, Math.max(0, i));
    const my = ++token;
    const slide = slides[i];
    const back = videos[1 - front];
    setSource(back, slide);
    back.muted = slide.muted;

    const swap = () => {
      if (my !== token) return;
      videos[front].pause();
      videos[front].classList.remove('is-front');
      back.classList.add('is-front');
      front = 1 - front;
      screen.style.background = slide.bg;
      idx = i;
      if (!atEnd) {
        const p = back.play();
        if (p) p.catch(() => { back.muted = true; back.play().catch(() => {}); });
      }
      updateUI();
      preloadNext();
    };

    const prepare = () => {
      if (my !== token) return;
      const end = Number.isFinite(back.duration) ? Math.max(0, back.duration - 0.05) : 0;
      const want = atEnd ? end : 0;
      if (Math.abs(back.currentTime - want) < 0.01) return swap();
      back.addEventListener('seeked', swap, { once: true });
      back.currentTime = want;
    };

    if (back.readyState >= 2) prepare();
    else back.addEventListener('loadeddata', prepare, { once: true });
  }

  function begin() {
    if (started) return;
    started = true;
    root.classList.add('is-started');
    root.focus({ preventScroll: true });
  }

  function start() {
    if (started) return;
    begin();
    ready.then(() => show(START)).catch(() => {});
  }

  const next = () => { if (!started) return start(); if (idx < slides.length - 1) show(idx + 1); };
  const prev = () => { if (started && idx > 0) show(idx - 1, { atEnd: true }); };

  function toggle() {
    if (!started) return start();
    const v = videos[front];
    if (v.ended || (Number.isFinite(v.duration) && v.currentTime >= v.duration - 0.06)) { v.currentTime = 0; v.play().catch(() => {}); }
    else if (v.paused) v.play().catch(() => {});
    else v.pause();
  }

  const isFull = () => (document.fullscreenElement || document.webkitFullscreenElement) === root;
  function fullscreen(on = !isFull()) {
    if (on) (root.requestFullscreen || root.webkitRequestFullscreen)?.call(root)?.catch?.(() => {});
    else if (isFull()) (document.exitFullscreen || document.webkitExitFullscreen)?.call(document);
  }

  function wake() {
    root.classList.remove('is-idle');
    clearTimeout(idleTimer);
    if (isFull()) idleTimer = setTimeout(() => root.classList.add('is-idle'), 2500);
  }

  // ----- Eventos -----
  poster.addEventListener('click', start);
  $('#pPrev').addEventListener('click', prev);
  $('#pNext').addEventListener('click', next);
  $('#pToggle').addEventListener('click', toggle);
  $('#pFull').addEventListener('click', () => fullscreen());

  // Clique no slide: terço esquerdo volta, o resto avança
  screen.addEventListener('click', (e) => {
    if (!started || e.target.closest('button, a')) return;
    const b = screen.getBoundingClientRect();
    if (e.clientX - b.left < b.width / 3) prev(); else next();
  });

  for (const v of videos) {
    for (const ev of ['play', 'pause', 'ended']) v.addEventListener(ev, updateUI);
    v.addEventListener('error', () => {
      if (v !== videos[1 - front] && v !== videos[front]) return;
      if (!v.dataset.src) return;
      console.warn('Player: erro ao carregar', v.dataset.src);
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    if (!(isFull() || root.contains(document.activeElement))) return;
    const onButton = e.target instanceof HTMLButtonElement;
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case 'n': case 'N': e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'PageUp': case 'p': case 'P': e.preventDefault(); prev(); break;
      case ' ': if (!onButton) { e.preventDefault(); toggle(); } break;
      case 'Enter': if (!onButton) { e.preventDefault(); next(); } break;
      case 'f': case 'F': e.preventDefault(); fullscreen(); break;
      case 'Home': if (started) { e.preventDefault(); show(START); } break;
      case 'End': if (started) { e.preventDefault(); show(slides.length - 1); } break;
      default: return;
    }
    wake();
  });

  root.addEventListener('pointermove', wake);
  for (const ev of ['fullscreenchange', 'webkitfullscreenchange']) document.addEventListener(ev, wake);

  return {
    // Usado pelos botões "Ver apresentação": rola até o player e começa
    open({ full = false } = {}) {
      if (full) fullscreen(true);
      root.scrollIntoView({ block: 'center', behavior: full ? 'auto' : 'smooth' });
      start();
      root.focus({ preventScroll: true });
    },
  };
}
