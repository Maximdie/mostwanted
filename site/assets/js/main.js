(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');

  /* Header: solid background after scrolling past the hero */
  var header = document.querySelector('.header');
  var fab = document.querySelector('.fab');
  function onScroll() {
    var y = window.scrollY;
    if (header && !header.classList.contains('header--solid')) {
      header.classList.toggle('is-solid', y > 40);
    }
    if (fab) fab.classList.toggle('is-visible', y > window.innerHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile menu */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = doc.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        doc.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* Reveal on scroll */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* YouTube: load the iframe only on click */
  document.querySelectorAll('.yt[data-id]').forEach(function (box) {
    var id = box.getAttribute('data-id');
    var btn = box.querySelector('button');
    box.style.backgroundImage = 'url(https://i.ytimg.com/vi/' + id + '/hqdefault.jpg)';
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      f.title = btn.getAttribute('aria-label') || 'Видео';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      box.classList.add('is-playing');
      box.replaceChildren(f);
    });
  });

  /* Local video: show the Telegram fallback if the file is missing */
  document.querySelectorAll('.player').forEach(function (p) {
    var v = p.querySelector('video');
    if (!v) return;
    var fail = function () { p.classList.add('is-fallback'); };
    v.addEventListener('error', fail, true);
    var src = v.querySelector('source');
    if (src) src.addEventListener('error', fail);
    // the error may fire before this script runs
    if (v.networkState === 3) fail();
    v.addEventListener('emptied', function () { if (v.networkState === 3) fail(); });
    setTimeout(function () { if (v.networkState === 3 || v.readyState === 0 && v.error) fail(); }, 1500);
  });

  /* Image lightbox */
  var lb = document.querySelector('.lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img');
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () {
        lbImg.src = b.getAttribute('data-full');
        lbImg.alt = b.querySelector('img') ? b.querySelector('img').alt : '';
        lb.showModal();
      });
    });
    lb.addEventListener('click', function (e) {
      if (e.target === lb || e.target.classList.contains('lightbox__inner') || e.target.classList.contains('lightbox__close')) lb.close();
    });
  } else {
    document.querySelectorAll('[data-full]').forEach(function (b) {
      b.addEventListener('click', function () { window.open(b.getAttribute('data-full'), '_blank'); });
    });
  }

  /* Relocation checklist: remember ticks in this browser */
  var list = document.querySelector('.checklist');
  if (list) {
    var KEY = 'mwm-checklist-v1';
    var boxes = list.querySelectorAll('input[type=checkbox]');
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { saved = {}; }
    var count = document.querySelector('[data-progress-count]');
    var bar = document.querySelector('[data-progress-bar]');
    function update() {
      var done = 0, state = {};
      boxes.forEach(function (b) {
        b.closest('.check').classList.toggle('is-done', b.checked);
        if (b.checked) { done++; state[b.value] = 1; }
      });
      if (count) count.textContent = done;
      if (bar) bar.style.width = (done / boxes.length * 100) + '%';
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
    }
    boxes.forEach(function (b) {
      if (saved[b.value]) b.checked = true;
      b.addEventListener('change', update);
    });
    update();
    var reset = document.querySelector('[data-reset]');
    if (reset) reset.addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); update(); });
    var print = document.querySelector('[data-print]');
    if (print) print.addEventListener('click', function () { window.print(); });
  }

  /* Home page: latest news (the block stays hidden until there is something to show) */
  var latest = document.querySelector('[data-latest-news]');
  if (latest && window.fetch) {
    fetch('/news/?format=json', { credentials: 'omit' })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (items) {
        if (!Array.isArray(items) || !items.length) return;
        var list = latest.querySelector('[data-latest-list]');
        items.forEach(function (n) {
          var el = function (tag, cls, text) {
            var e = document.createElement(tag);
            if (cls) e.className = cls;
            if (text) e.textContent = text;
            return e;
          };
          var card = el('a', 'news-card' + (n.cover ? '' : ' news-card--text'));
          card.href = n.url;
          if (n.cover) {
            var media = el('span', 'news-card__media');
            var img = el('img');
            img.src = n.cover; img.alt = ''; img.loading = 'lazy';
            media.appendChild(img);
            card.appendChild(media);
          }
          var body = el('span', 'news-card__body');
          body.appendChild(el('time', '', n.date));
          body.appendChild(el('span', 'news-card__title', n.title));
          body.appendChild(el('span', 'news-card__text', n.text));
          body.appendChild(el('span', 'news-card__more', 'Читать →'));
          card.appendChild(body);
          list.appendChild(card);
        });
        latest.hidden = false;
      })
      .catch(function () {});
  }

  /* Year in footer */
  var yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
