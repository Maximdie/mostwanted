<?php
/*
 * Админка новостей: /admin/
 * Логин и хеш пароля — в _news/config.php, всё остальное — в _news/lib.php.
 */
require dirname(__DIR__) . '/_news/lib.php';

header('X-Robots-Tag: noindex, nofollow');
header('X-Frame-Options: DENY');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header('Cache-Control: no-store');

admin_session_start();

$a = isset($_GET['a']) ? (string)$_GET['a'] : '';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';
$logged = !empty($_SESSION['admin']);

function go($query = '')
{
    header('Location: ./' . ($query !== '' ? '?' . $query : ''));
    exit;
}

function csrf_ok()
{
    $t = isset($_POST['csrf']) ? $_POST['csrf'] : (isset($_SERVER['HTTP_X_CSRF']) ? $_SERVER['HTTP_X_CSRF'] : '');
    return is_string($t) && hash_equals($_SESSION['csrf'], $t);
}

function json_out($data, $code = 200)
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function field($name, $default = '')
{
    $v = isset($_POST[$name]) && is_string($_POST[$name]) ? $_POST[$name] : $default;
    return mb_check_encoding($v, 'UTF-8') ? $v : mb_convert_encoding($v, 'UTF-8', 'Windows-1251');
}

// Запрос больше post_max_size: PHP молча отдаёт пустые $_POST и $_FILES
$too_big = $post && empty($_POST) && empty($_FILES) && (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 0;

// ------------------------------------------------------------------ actions

if ($a === 'upload') {
    if ($too_big) {
        json_out(['error' => 'Файл слишком большой.'], 413);
    }
    if (!$post || !$logged || !csrf_ok()) {
        json_out(['error' => 'Нет доступа. Обновите страницу и войдите снова.'], 403);
    }
    $f = isset($_FILES['file']) ? $_FILES['file'] : null;
    if (!$f || $f['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($f['tmp_name'])) {
        $big = $f && in_array($f['error'], [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true);
        json_out(['error' => $big ? 'Файл слишком большой.' : 'Файл не загрузился, попробуйте ещё раз.'], 400);
    }
    $url = news_store_image((string)file_get_contents($f['tmp_name']));
    if (!$url) {
        json_out(['error' => 'Это не фото. Подходят JPG, PNG, GIF и WEBP.'], 400);
    }
    json_out(['url' => $url]);
}

$error = '';

if ($a === 'login' && $post) {
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
    if (!csrf_ok()) {
        $error = 'Страница устарела — попробуйте ещё раз.';
    } elseif (admin_login_blocked($ip)) {
        $error = 'Слишком много неудачных попыток. Подождите 15 минут.';
    } else {
        $cfg = admin_credentials();
        $user = mb_strtolower(trim(field('user')), 'UTF-8');
        if (hash_equals(mb_strtolower($cfg['user'], 'UTF-8'), $user) && password_verify(field('pass'), $cfg['hash'])) {
            session_regenerate_id(true);
            $_SESSION['admin'] = 1;
            go();
        }
        admin_login_blocked($ip, true);
        sleep(1);
        $error = 'Неверный логин или пароль.';
    }
}

if (!$logged) {
    view_login($error);
    exit;
}

if ($post && !csrf_ok()) {
    view_layout('Ошибка', '<div class="notice notice--error">Страница устарела или сессия закончилась. '
        . ($too_big ? 'Похоже, текст или фото слишком большие. ' : '')
        . 'Вернитесь назад, обновите страницу и попробуйте снова.</div><p><a href="./">← К списку новостей</a></p>');
    exit;
}

if ($a === 'logout' && $post) {
    $_SESSION = [];
    session_destroy();
    setcookie('mwadmin', '', time() - 3600, '/');
    go();
}

if ($a === 'delete' && $post) {
    $id = (int)field('id');
    news_update(function (array &$items) use ($id) {
        $items = array_values(array_filter($items, function ($n) use ($id) {
            return (int)$n['id'] !== $id;
        }));
    });
    go('deleted=1');
}

if ($a === 'save' && $post) {
    $id = (int)field('id');
    $title = trim(preg_replace('/\s+/u', ' ', field('title')));
    $date = field('date');
    if (!preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $date, $m) || !checkdate((int)$m[2], (int)$m[3], (int)$m[1])) {
        $date = date('Y-m-d');
    }
    $html = news_clean_html(field('html'));
    if ($title === '' && $html !== '') {
        list($title, $html) = news_title_from_html($html);
    }
    $item = [
        'id' => $id,
        'title' => mb_substr($title, 0, 300, 'UTF-8'),
        'date' => $date,
        'html' => $html,
        'published' => field('published') === '1',
    ];
    if ($title === '') {
        view_edit($item, 'Добавьте текст новости — или хотя бы заголовок.');
        exit;
    }
    $id = news_update(function (array &$items) use ($item) {
        $now = date('c');
        foreach ($items as $i => $n) {
            if ((int)$n['id'] === $item['id'] && $item['id'] > 0) {
                $items[$i] = array_merge($n, $item, ['updated' => $now]);
                return $item['id'];
            }
        }
        $max = 0;
        foreach ($items as $n) {
            $max = max($max, (int)$n['id']);
        }
        $items[] = array_merge($item, ['id' => $max + 1, 'created' => $now, 'updated' => $now]);
        return $max + 1;
    });
    go('saved=' . $id);
}

if ($a === 'password') {
    $msg = '';
    if ($post) {
        $cfg = admin_credentials();
        $new = field('new');
        if (!password_verify(field('current'), $cfg['hash'])) {
            $msg = 'Текущий пароль введён неверно.';
        } elseif (mb_strlen($new, 'UTF-8') < 8) {
            $msg = 'Новый пароль должен быть не короче 8 символов.';
        } elseif ($new !== field('repeat')) {
            $msg = 'Пароли не совпадают.';
        } else {
            news_mkdir(NEWS_DATA);
            file_put_contents(NEWS_DATA . '/auth.json', json_encode(['hash' => password_hash($new, PASSWORD_DEFAULT), 'changed' => date('c')]));
            go('password=1');
        }
    }
    view_password($msg);
    exit;
}

if ($a === 'edit') {
    $id = (int)(isset($_GET['id']) ? $_GET['id'] : 0);
    $item = $id ? news_find($id) : null;
    if ($id && !$item) {
        go();
    }
    view_edit($item ?: ['id' => 0, 'title' => '', 'date' => date('Y-m-d'), 'html' => '', 'published' => true]);
    exit;
}

view_list();

// ------------------------------------------------------------------ views

function view_layout($title, $content, $editor = false)
{
    $css = 'admin.css?v=' . filemtime(__DIR__ . '/admin.css');
    $js = 'admin.js?v=' . filemtime(__DIR__ . '/admin.js');
    $logged = !empty($_SESSION['admin']);
    ?><!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title><?= h($title) ?> — админка сайта</title>
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<?php if ($editor): ?>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css">
<?php endif; ?>
<link rel="stylesheet" href="<?= h($css) ?>">
</head>
<body>
<header class="bar">
  <a class="bar__brand" href="./"><span class="bar__mark">ИВ</span><span>Новости сайта</span></a>
  <?php if ($logged): ?>
  <nav class="bar__nav">
    <a href="/news.php" target="_blank" rel="noopener">Открыть сайт</a>
    <a href="?a=password">Пароль</a>
    <form method="post" action="?a=logout"><input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>"><button type="submit">Выйти</button></form>
  </nav>
  <?php endif; ?>
</header>
<main class="box">
<?= $content ?>
</main>
<?php if ($editor): ?>
<script src="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.js"></script>
<script src="<?= h($js) ?>"></script>
<?php endif; ?>
</body>
</html>
<?php
}

function view_login($error)
{
    ob_start(); ?>
<form class="card login" method="post" action="?a=login">
  <h1>Вход</h1>
  <p class="muted">Управление новостями на сайте mostwanted.consulting</p>
  <?php if ($error): ?><div class="notice notice--error"><?= h($error) ?></div><?php endif; ?>
  <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
  <label class="field"><span>Логин</span>
    <input name="user" autocomplete="username" autocapitalize="off" autocorrect="off" spellcheck="false" required autofocus></label>
  <label class="field"><span>Пароль</span>
    <input name="pass" type="password" autocomplete="current-password" required></label>
  <button class="btn btn--primary btn--wide" type="submit">Войти</button>
</form>
<?php
    view_layout('Вход', ob_get_clean());
}

function view_list()
{
    $items = news_sort(news_all());
    $csrf = $_SESSION['csrf'];
    ob_start();
    if (isset($_GET['saved'])) {
        $n = news_find((int)$_GET['saved']);
        if ($n) {
            echo '<div class="notice notice--ok">Сохранено: «' . h($n['title']) . '». '
                . ($n['published'] ? 'Новость уже на сайте.' : 'Это черновик — на сайте его не видно.')
                . ' <a href="' . h(news_url($n)) . '" target="_blank" rel="noopener">Посмотреть →</a></div>';
        }
    }
    if (isset($_GET['deleted'])) {
        echo '<div class="notice notice--ok">Новость удалена.</div>';
    }
    if (isset($_GET['password'])) {
        echo '<div class="notice notice--ok">Пароль изменён. В следующий раз входите с новым.</div>';
    }
    ?>
<div class="head">
  <h1>Новости</h1>
  <a class="btn btn--primary" href="?a=edit">+ Добавить новость</a>
</div>
<?php if (!$items): ?>
<div class="card empty">
  <p><strong>Пока нет ни одной новости.</strong></p>
  <p>Нажмите «Добавить новость», вставьте текст (например, скопированный из Telegram), добавьте фото или видео — и сохраните. Новость сразу появится в разделе «Новости» на сайте.</p>
</div>
<?php else: ?>
<ul class="items">
  <?php foreach ($items as $n): $cover = news_cover($n); ?>
  <li class="item">
    <a class="item__thumb" href="?a=edit&amp;id=<?= (int)$n['id'] ?>"><?php if ($cover): ?><img src="<?= h($cover) ?>" alt="" loading="lazy"><?php endif; ?></a>
    <div class="item__body">
      <a class="item__title" href="?a=edit&amp;id=<?= (int)$n['id'] ?>"><?= h($n['title']) ?></a>
      <div class="item__meta"><?= h(news_date_ru($n['date'])) ?>
        <?= $n['published'] ? '<span class="badge badge--on">На сайте</span>' : '<span class="badge">Черновик</span>' ?></div>
    </div>
    <div class="item__actions">
      <a class="btn btn--small" href="?a=edit&amp;id=<?= (int)$n['id'] ?>">Изменить</a>
      <a class="btn btn--small btn--ghost" href="<?= h(news_url($n)) ?>" target="_blank" rel="noopener">Смотреть</a>
      <form method="post" action="?a=delete" onsubmit="return confirm('Удалить новость «<?= h(addslashes(news_cut($n['title'], 60))) ?>»? Вернуть её будет нельзя.')">
        <input type="hidden" name="csrf" value="<?= h($csrf) ?>"><input type="hidden" name="id" value="<?= (int)$n['id'] ?>">
        <button class="btn btn--small btn--danger" type="submit">Удалить</button>
      </form>
    </div>
  </li>
  <?php endforeach; ?>
</ul>
<?php endif;
    view_layout('Новости', ob_get_clean());
}

function view_edit(array $n, $error = '')
{
    $isNew = empty($n['id']);
    ob_start(); ?>
<p class="back"><a href="./">← Все новости</a></p>
<h1><?= $isNew ? 'Новая новость' : 'Редактирование' ?></h1>
<?php if ($error): ?><div class="notice notice--error"><?= h($error) ?></div><?php endif; ?>
<form class="card editor-form" id="news-form" method="post" action="?a=save"
      data-csrf="<?= h($_SESSION['csrf']) ?>" data-new="<?= $isNew ? '1' : '0' ?>">
  <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
  <input type="hidden" name="id" value="<?= (int)$n['id'] ?>">

  <label class="field"><span>Заголовок</span>
    <input name="title" value="<?= h($n['title']) ?>" maxlength="300" placeholder="Можно оставить пустым — возьмём первую строку текста"></label>

  <div class="row">
    <label class="field field--date"><span>Дата</span>
      <input type="date" name="date" value="<?= h($n['date']) ?>" required></label>
    <label class="switch"><input type="checkbox" name="published" value="1"<?= $n['published'] ? ' checked' : '' ?>>
      <span>Показывать на сайте</span></label>
  </div>

  <div class="field">
    <span>Текст</span>
    <div class="quick">
      <button class="btn btn--small btn--ghost" type="button" data-act="photo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M21 17l-5-5-8 7"/></svg>Добавить фото</button>
      <button class="btn btn--small btn--ghost" type="button" data-act="video">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>Видео с YouTube</button>
    </div>
    <div id="editor" class="editor"></div>
    <textarea name="html" id="html" hidden><?= h($n['html']) ?></textarea>
    <p class="status" id="status" aria-live="polite"></p>
  </div>

  <details class="help">
    <summary>Как перенести пост из Telegram</summary>
    <ol>
      <li>В Telegram выделите текст поста и скопируйте его (Ctrl+C или «Копировать»).</li>
      <li>Нажмите в поле «Текст» и вставьте (Ctrl+V или «Вставить»). Жирный текст, ссылки и списки сохранятся.</li>
      <li>Фото из Telegram так не переносятся: сохраните фото на компьютер или телефон и добавьте кнопкой «Добавить фото». Можно выбрать сразу несколько.</li>
      <li>Ссылка на YouTube отдельной строкой сама превратится в видео. Или нажмите «Видео с YouTube».</li>
      <li>Заголовок можно не писать — первая строка поста станет заголовком.</li>
    </ol>
  </details>

  <div class="actions">
    <button class="btn btn--primary" type="submit" id="save">Сохранить</button>
    <a class="btn btn--ghost" href="./">Отмена</a>
    <?php if (!$isNew): ?>
    <a class="actions__link" href="<?= h(news_url($n)) ?>" target="_blank" rel="noopener">Посмотреть на сайте →</a>
    <?php endif; ?>
  </div>
</form>
<noscript><div class="notice notice--error">Для редактора нужен включённый JavaScript.</div></noscript>
<?php
    view_layout($isNew ? 'Новая новость' : 'Редактирование', ob_get_clean(), true);
}

function view_password($msg)
{
    ob_start(); ?>
<p class="back"><a href="./">← Все новости</a></p>
<form class="card login" method="post" action="?a=password">
  <h1>Сменить пароль</h1>
  <?php if ($msg): ?><div class="notice notice--error"><?= h($msg) ?></div><?php endif; ?>
  <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
  <label class="field"><span>Текущий пароль</span><input name="current" type="password" autocomplete="current-password" required></label>
  <label class="field"><span>Новый пароль (от 8 символов)</span><input name="new" type="password" autocomplete="new-password" minlength="8" required></label>
  <label class="field"><span>Новый пароль ещё раз</span><input name="repeat" type="password" autocomplete="new-password" minlength="8" required></label>
  <button class="btn btn--primary btn--wide" type="submit">Сохранить пароль</button>
</form>
<?php
    view_layout('Пароль', ob_get_clean());
}
