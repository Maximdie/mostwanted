/* Редактор новости: Quill + загрузка фото + видео YouTube */
(function () {
  'use strict';
  var form = document.getElementById('news-form');
  if (!form) return;
  var status = document.getElementById('status');

  function setStatus(text, isError) {
    status.textContent = text || '';
    status.classList.toggle('status--error', !!isError);
  }

  if (!window.Quill) {
    setStatus('Редактор не загрузился. Проверьте интернет и обновите страницу.', true);
    return;
  }

  var csrf = form.getAttribute('data-csrf');
  var htmlField = document.getElementById('html');
  var Delta = Quill.import('delta');
  var pending = 0;
  var dirty = false;
  var skippedImages = 0;

  var quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: 'Вставьте сюда текст из Telegram или напишите новость…',
    modules: {
      toolbar: {
        container: [
          [{ header: [2, 3, false] }],
          ['bold', 'italic', 'underline', 'strike'],
          [{ list: 'ordered' }, { list: 'bullet' }],
          ['blockquote', 'link'],
          ['image', 'video'],
          ['clean']
        ],
        handlers: { image: pickPhotos, video: addVideo }
      },
      uploader: {
        mimetypes: ['image/png', 'image/jpeg', 'image/gif', 'image/webp'],
        handler: function (range, files) { uploadFiles(files, range.index); }
      }
    }
  });

  // Подсказки к кнопкам панели
  var titles = {
    'ql-header': 'Заголовок', 'ql-bold': 'Жирный', 'ql-italic': 'Курсив', 'ql-underline': 'Подчёркнутый',
    'ql-strike': 'Зачёркнутый', 'ql-list[value=ordered]': 'Нумерованный список', 'ql-list[value=bullet]': 'Список',
    'ql-blockquote': 'Цитата', 'ql-link': 'Ссылка', 'ql-image': 'Добавить фото', 'ql-video': 'Видео с YouTube',
    'ql-clean': 'Убрать оформление'
  };
  Object.keys(titles).forEach(function (sel) {
    var parts = sel.split('[');
    var el = document.querySelector('.ql-toolbar .' + parts[0] + (parts[1] ? '[' + parts[1] : ''));
    if (el) el.setAttribute('title', titles[sel]);
  });

  // Картинки при вставке: наши и встроенные (data:) оставляем, эмодзи-картинки
  // превращаем в символ, чужие (например, с серверов Telegram) пропускаем.
  quill.clipboard.addMatcher('IMG', function (node, delta) {
    var src = node.getAttribute('src') || '';
    if (/^data:image\//.test(src) || src.indexOf('/uploads/news/') === 0 || src.indexOf(location.origin + '/uploads/news/') === 0) {
      return delta;
    }
    var alt = node.getAttribute('alt') || '';
    if (alt && alt.length <= 8) return new Delta().insert(alt);
    skippedImages++;
    return new Delta();
  });

  if (htmlField.value.trim()) {
    quill.setContents(quill.clipboard.convert({ html: htmlField.value }), 'silent');
  }

  quill.on('text-change', function (delta, old, source) {
    if (source !== 'user') return;
    dirty = true;
    if (skippedImages) {
      setStatus('Фото из Telegram не копируются вместе с текстом — добавьте их кнопкой «Добавить фото».', true);
      skippedImages = 0;
    }
  });
  form.addEventListener('input', function () { dirty = true; });

  // Для новой новости — сегодняшняя дата по часам этого устройства
  if (form.getAttribute('data-new') === '1') {
    var d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    form.elements.date.value = d.toISOString().slice(0, 10);
  }

  form.querySelectorAll('[data-act]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.getAttribute('data-act') === 'photo') pickPhotos(); else addVideo();
    });
  });

  // ------------------------------------------------------------------ фото

  function pickPhotos() {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.multiple = true;
    input.addEventListener('change', function () {
      if (input.files.length) uploadFiles(input.files, quill.getSelection(true).index);
    });
    input.click();
  }

  /** Большие фото с телефона уменьшаем до 2000px — грузятся быстрее и весят меньше. */
  function shrink(file) {
    return new Promise(function (resolve) {
      if (!/^image\/(jpeg|png|webp)$/.test(file.type)) return resolve(file);
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var max = 2000;
        var k = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
        if (k === 1 && file.size < 1.5e6) return resolve(file);
        var c = document.createElement('canvas');
        c.width = Math.round(img.naturalWidth * k);
        c.height = Math.round(img.naturalHeight * k);
        var ctx = c.getContext('2d');
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.drawImage(img, 0, 0, c.width, c.height);
        c.toBlob(function (b) { resolve(b && b.size < file.size ? b : file); }, 'image/jpeg', 0.86);
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
      img.src = url;
    });
  }

  function upload(blob, name) {
    var fd = new FormData();
    fd.append('file', blob, name);
    return fetch('?a=upload', {
      method: 'POST', body: fd, credentials: 'same-origin', headers: { 'X-CSRF': csrf }
    }).then(function (r) {
      return r.json().catch(function () { return { error: 'Сервер ответил ошибкой (' + r.status + ').' }; });
    });
  }

  /** Вставляет блок (фото или видео) отдельной строкой. Возвращает позицию после него. */
  function insertBlock(index, embed) {
    var d = new Delta().retain(index);
    var added = 0;
    if (index > 0 && quill.getText(index - 1, 1) !== '\n') { d = d.insert('\n'); added++; }
    d = d.insert(embed);
    added++;
    if (quill.getText(index, 1) !== '\n') { d = d.insert('\n'); added++; }
    quill.updateContents(d, 'user');
    return index + added;
  }

  async function uploadFiles(files, index) {
    files = Array.prototype.slice.call(files);
    pending++;
    var failed = [];
    for (var i = 0; i < files.length; i++) {
      setStatus('Загружаю фото' + (files.length > 1 ? ' ' + (i + 1) + ' из ' + files.length : '') + '…');
      try {
        var blob = await shrink(files[i]);
        var res = await upload(blob, files[i].name || 'photo.jpg');
        if (res.url) index = insertBlock(index, { image: res.url });
        else failed.push((files[i].name || 'фото') + ': ' + (res.error || 'ошибка'));
      } catch (e) {
        failed.push((files[i].name || 'фото') + ': нет связи с сервером');
      }
    }
    pending--;
    quill.setSelection(index, 0, 'silent');
    setStatus(failed.length ? 'Не загрузилось — ' + failed.join('; ') : 'Фото добавлено.', failed.length > 0);
  }

  // ------------------------------------------------------------------ видео

  function youtubeId(url) {
    var m = String(url).trim().match(/^(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:[^#\s]*&)?v=|embed\/|shorts\/|live\/|v\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/i);
    return m ? m[1] : null;
  }

  function addVideo() {
    var range = quill.getSelection(true);
    var url = window.prompt('Вставьте ссылку на видео YouTube:');
    if (!url) return;
    var id = youtubeId(url);
    if (!id) {
      window.alert('Это не похоже на ссылку YouTube. Скопируйте адрес видео — например, https://www.youtube.com/watch?v=…');
      return;
    }
    var index = insertBlock(range ? range.index : quill.getLength() - 1, { video: 'https://www.youtube-nocookie.com/embed/' + id });
    quill.setSelection(index, 0, 'silent');
    setStatus('Видео добавлено.');
  }

  // ------------------------------------------------------------------ сохранение

  form.addEventListener('submit', function (e) {
    if (pending) {
      e.preventDefault();
      window.alert('Подождите, фото ещё загружаются.');
      return;
    }
    var empty = quill.getLength() <= 1 && !quill.root.querySelector('img, iframe');
    htmlField.value = empty ? '' : quill.root.innerHTML;
    dirty = false;
    document.getElementById('save').disabled = true;
    document.getElementById('save').textContent = 'Сохраняю…';
  });

  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'ы')) {
      e.preventDefault();
      if (form.requestSubmit) form.requestSubmit(); else form.submit();
    }
  });

  window.addEventListener('beforeunload', function (e) {
    if (dirty) { e.preventDefault(); e.returnValue = ''; }
  });
})();
