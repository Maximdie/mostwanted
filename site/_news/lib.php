<?php
/*
 * Новости: хранение, очистка HTML, вывод на сайт и вход в админку.
 * Подключается из news.php и admin/index.php. Совместимо с PHP 7.4+.
 *
 * Данные живут только на хостинге (в git их нет):
 *   _news/data/news.json   — сами новости (+ news.bak.json — предыдущая версия)
 *   _news/data/auth.json   — пароль, если его меняли из админки
 *   uploads/news/ГГГГ/ММ/  — загруженные фото
 */

define('NEWS_DATA', __DIR__ . '/data');
define('NEWS_FILE', NEWS_DATA . '/news.json');
define('NEWS_UPLOAD_DIR', dirname(__DIR__) . '/uploads/news');
define('NEWS_UPLOAD_URL', '/uploads/news');
define('NEWS_PER_PAGE', 12);
define('NEWS_MAX_IMAGE', 15 * 1024 * 1024);

function h($s)
{
    return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
}

function news_mkdir($dir)
{
    if (!is_dir($dir)) {
        @mkdir($dir, 0755, true);
    }
}

// ------------------------------------------------------------------ storage

function news_all()
{
    if (!is_file(NEWS_FILE)) {
        return [];
    }
    $items = json_decode((string)file_get_contents(NEWS_FILE), true);
    return is_array($items) ? $items : [];
}

/** Читает, меняет и атомарно сохраняет список. $fn получает массив по ссылке. */
function news_update(callable $fn)
{
    news_mkdir(NEWS_DATA);
    $lock = fopen(NEWS_DATA . '/.lock', 'c');
    flock($lock, LOCK_EX);
    try {
        $items = news_all();
        $result = $fn($items);
        $json = json_encode(array_values($items), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
        $tmp = NEWS_FILE . '.tmp';
        if ($json === false || file_put_contents($tmp, $json) === false) {
            throw new RuntimeException('Не удалось записать файл новостей');
        }
        if (is_file(NEWS_FILE)) {
            @copy(NEWS_FILE, NEWS_DATA . '/news.bak.json');
        }
        rename($tmp, NEWS_FILE);
        return $result;
    } finally {
        flock($lock, LOCK_UN);
        fclose($lock);
    }
}

function news_sort(array $items)
{
    usort($items, function ($a, $b) {
        return [$b['date'], $b['id']] <=> [$a['date'], $a['id']];
    });
    return $items;
}

function news_published()
{
    return news_sort(array_values(array_filter(news_all(), function ($n) {
        return !empty($n['published']);
    })));
}

function news_find($id)
{
    foreach (news_all() as $n) {
        if ((int)$n['id'] === (int)$id) {
            return $n;
        }
    }
    return null;
}

/** Сохраняет картинку из байтов. Возвращает URL или null, если это не картинка. */
function news_store_image($bytes)
{
    if ($bytes === '' || strlen($bytes) > NEWS_MAX_IMAGE) {
        return null;
    }
    $info = @getimagesizefromstring($bytes);
    $types = [IMAGETYPE_JPEG => 'jpg', IMAGETYPE_PNG => 'png', IMAGETYPE_GIF => 'gif', IMAGETYPE_WEBP => 'webp'];
    if (!$info || !isset($types[$info[2]])) {
        return null;
    }
    $sub = date('Y/m');
    news_mkdir(NEWS_UPLOAD_DIR . '/' . $sub);
    $name = bin2hex(random_bytes(8)) . '.' . $types[$info[2]];
    if (file_put_contents(NEWS_UPLOAD_DIR . '/' . $sub . '/' . $name, $bytes) === false) {
        return null;
    }
    return NEWS_UPLOAD_URL . '/' . $sub . '/' . $name;
}

// ------------------------------------------------------------------ text helpers

function news_youtube_id($url)
{
    if (preg_match('~^(?:https?://)?(?:www\.|m\.)?(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:[^#\s]*&)?v=|embed/|shorts/|live/|v/)|youtu\.be/)([A-Za-z0-9_-]{11})~i', trim($url), $m)) {
        return $m[1];
    }
    return null;
}

function news_cut($text, $max)
{
    $text = trim(preg_replace('/\s+/u', ' ', $text));
    if (mb_strlen($text, 'UTF-8') <= $max) {
        return $text;
    }
    $cut = mb_substr($text, 0, $max, 'UTF-8');
    $space = mb_strrpos($cut, ' ', 0, 'UTF-8');
    if ($space !== false && $space > $max * 0.6) {
        $cut = mb_substr($cut, 0, $space, 'UTF-8');
    }
    return rtrim($cut, " ,.;:—–-") . '…';
}

function news_date_ru($ymd)
{
    $months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
    $t = strtotime($ymd);
    if (!$t) {
        return '';
    }
    return (int)date('j', $t) . ' ' . $months[(int)date('n', $t) - 1] . ' ' . date('Y', $t);
}

function news_text($html)
{
    $text = preg_replace('~</(p|h2|h3|li|blockquote)>|<br\s*/?>~i', ' ', $html);
    return trim(html_entity_decode(strip_tags($text), ENT_QUOTES | ENT_HTML5, 'UTF-8'));
}

function news_excerpt(array $n, $max = 220)
{
    return news_cut(news_text($n['html']), $max);
}

/** Обложка для карточки: первое фото, иначе превью первого видео. */
function news_cover(array $n)
{
    if (preg_match('~<img[^>]+src="([^"]+)"~', $n['html'], $m)) {
        return $m[1];
    }
    if (preg_match('~<iframe[^>]+src="[^"]*/embed/([A-Za-z0-9_-]{11})~', $n['html'], $m)) {
        return 'https://i.ytimg.com/vi/' . $m[1] . '/hqdefault.jpg';
    }
    return null;
}

function news_url(array $n)
{
    return '/news.php?id=' . (int)$n['id'];
}

// ------------------------------------------------------------------ HTML cleaning

/*
 * Пропускаем только то, что умеет редактор: абзацы, заголовки, жирный/курсив,
 * списки, цитаты, ссылки, наши фото и видео YouTube. Остальное — вырезаем
 * (скрипты, стили) или разворачиваем (span, div и прочая обёртка из Telegram).
 */
const NEWS_TAGS = ['p', 'br', 'strong', 'em', 'u', 's', 'a', 'h2', 'h3', 'blockquote', 'ul', 'ol', 'li', 'img', 'iframe'];
const NEWS_RENAME = ['b' => 'strong', 'i' => 'em', 'strike' => 's', 'del' => 's', 'h1' => 'h2', 'h4' => 'h3', 'h5' => 'h3', 'h6' => 'h3', 'div' => 'p'];
const NEWS_DROP = ['script', 'style', 'noscript', 'template', 'object', 'embed', 'form', 'input', 'button', 'select', 'textarea', 'svg', 'math', 'head', 'title', 'meta', 'link', 'video', 'audio', 'canvas'];

function news_clean_html($html)
{
    $html = trim((string)$html);
    if ($html === '') {
        return '';
    }
    $doc = new DOMDocument('1.0', 'UTF-8');
    $prev = libxml_use_internal_errors(true);
    $doc->loadHTML('<?xml encoding="UTF-8"?><div id="news-root">' . $html . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD | LIBXML_NONET);
    libxml_clear_errors();
    libxml_use_internal_errors($prev);
    $root = (new DOMXPath($doc))->query('//div[@id="news-root"]')->item(0);
    if (!$root) {
        return '';
    }

    news_clean_children($root);
    news_split_lists($root);
    news_autolink($doc, $root);
    news_embed_youtube_lines($doc, $root);

    // пустые строки в начале и в конце не нужны
    foreach (['firstChild', 'lastChild'] as $edge) {
        while ($root->$edge && news_is_blank($root->$edge)) {
            $root->removeChild($root->$edge);
        }
    }

    $out = '';
    foreach ($root->childNodes as $child) {
        $out .= $doc->saveHTML($child);
    }
    return trim($out);
}

function news_is_blank(DOMNode $node)
{
    if ($node instanceof DOMText) {
        return trim($node->textContent, " \t\n\r\0\x0B\xC2\xA0") === '';
    }
    if (!($node instanceof DOMElement)) {
        return true;
    }
    if (in_array($node->nodeName, ['img', 'iframe'], true)) {
        return false;
    }
    if ($node->getElementsByTagName('img')->length || $node->getElementsByTagName('iframe')->length) {
        return false;
    }
    return trim($node->textContent, " \t\n\r\0\x0B\xC2\xA0") === '';
}

function news_clean_children(DOMNode $parent)
{
    $children = [];
    foreach ($parent->childNodes as $c) {
        $children[] = $c;
    }
    foreach ($children as $node) {
        if ($node instanceof DOMText) {
            continue;
        }
        if (!($node instanceof DOMElement)) {
            $parent->removeChild($node);
            continue;
        }
        $tag = strtolower($node->nodeName);
        if (in_array($tag, NEWS_DROP, true)) {
            $parent->removeChild($node);
            continue;
        }
        if (isset(NEWS_RENAME[$tag])) {
            $node = news_rename($node, NEWS_RENAME[$tag]);
            $tag = NEWS_RENAME[$tag];
        }
        // ссылка без нормального адреса остаётся просто текстом
        $badLink = $tag === 'a' && !preg_match('~^(https?://|mailto:|tel:|/)~i', trim($node->getAttribute('href')));
        if ($badLink || !in_array($tag, NEWS_TAGS, true)) {
            news_clean_children($node);
            while ($node->firstChild) {
                $parent->insertBefore($node->firstChild, $node);
            }
            $parent->removeChild($node);
            continue;
        }
        if (!news_clean_attributes($node, $tag)) {
            $parent->removeChild($node);
            continue;
        }
        news_clean_children($node);
    }
}

function news_rename(DOMElement $node, $tag)
{
    $new = $node->ownerDocument->createElement($tag);
    foreach ($node->attributes as $attr) {
        $new->setAttribute($attr->name, $attr->value);
    }
    while ($node->firstChild) {
        $new->appendChild($node->firstChild);
    }
    $node->parentNode->replaceChild($new, $node);
    return $new;
}

/** Оставляет разрешённые атрибуты. false — элемент надо удалить целиком. */
function news_clean_attributes(DOMElement $node, $tag)
{
    $keep = [];
    $get = function ($name) use ($node) {
        return trim($node->getAttribute($name));
    };

    if ($tag === 'a') {
        $keep['href'] = $get('href');
        if (preg_match('~^https?://~i', $keep['href'])) {
            $keep['target'] = '_blank';
            $keep['rel'] = 'noopener';
        }
    } elseif ($tag === 'img') {
        $src = $get('src');
        if (preg_match('~^data:image/(?:png|jpe?g|gif|webp);base64,~i', $src)) {
            $src = news_store_image((string)base64_decode(substr($src, strpos($src, ',') + 1), true));
        } elseif (preg_match('~^(?:https?://[^/]+)?(/uploads/news/\d{4}/\d{2}/[a-f0-9]{16}\.(?:jpg|png|gif|webp))$~', $src, $m)) {
            $src = $m[1];
        } else {
            $src = null;
        }
        if (!$src) {
            return false;
        }
        $keep['src'] = $src;
        $alt = $get('alt');
        if ($alt !== '') {
            $keep['alt'] = mb_substr($alt, 0, 200, 'UTF-8');
        }
    } elseif ($tag === 'iframe') {
        $id = news_youtube_id($get('src'));
        if (!$id) {
            return false;
        }
        $keep = ['class' => 'ql-video', 'frameborder' => '0', 'allowfullscreen' => 'true', 'src' => 'https://www.youtube-nocookie.com/embed/' . $id];
    } elseif ($tag === 'li') {
        $list = $get('data-list');
        if ($list !== '') {
            $keep['data-list'] = $list === 'ordered' ? 'ordered' : 'bullet';
        }
    }

    if (in_array($tag, ['p', 'h2', 'h3', 'li', 'blockquote'], true)) {
        $classes = array_filter(preg_split('/\s+/', $get('class')), function ($c) {
            return preg_match('/^ql-(align-(center|right|justify)|indent-[1-8])$/', $c);
        });
        if ($classes) {
            $keep['class'] = implode(' ', $classes);
        }
    }

    while ($node->attributes->length) {
        $node->removeAttribute($node->attributes->item(0)->name);
    }
    foreach ($keep as $name => $value) {
        $node->setAttribute($name, $value);
    }
    return true;
}

/*
 * Quill 2 кладёт любой список в <ol>, а тип пишет в li[data-list].
 * Превращаем это в нормальные <ul>/<ol>, чтобы маркеры и нумерация были верными.
 */
function news_split_lists(DOMElement $root)
{
    $lists = [];
    foreach (['ol', 'ul'] as $t) {
        foreach ($root->getElementsByTagName($t) as $l) {
            $lists[] = $l;
        }
    }
    foreach ($lists as $list) {
        $default = $list->nodeName === 'ul' ? 'bullet' : 'ordered';
        $current = null;
        $currentType = null;
        $children = [];
        foreach ($list->childNodes as $c) {
            $children[] = $c;
        }
        foreach ($children as $li) {
            if (!($li instanceof DOMElement) || $li->nodeName !== 'li') {
                $list->removeChild($li);
                continue;
            }
            $type = $li->getAttribute('data-list') ?: $default;
            $li->removeAttribute('data-list');
            if ($type !== $currentType) {
                $current = $root->ownerDocument->createElement($type === 'bullet' ? 'ul' : 'ol');
                $list->parentNode->insertBefore($current, $list);
                $currentType = $type;
            }
            $current->appendChild($li);
        }
        $list->parentNode->removeChild($list);
    }
}

/** Голые адреса в тексте (как их копирует Telegram) превращаем в ссылки. */
function news_autolink(DOMDocument $doc, DOMElement $root)
{
    $texts = [];
    foreach ((new DOMXPath($doc))->query('.//text()[not(ancestor::a)]', $root) as $t) {
        $texts[] = $t;
    }
    foreach ($texts as $t) {
        $parts = preg_split('~(https?://[^\s<>"«»]+)~u', $t->nodeValue, -1, PREG_SPLIT_DELIM_CAPTURE);
        if (count($parts) < 2) {
            continue;
        }
        $frag = $doc->createDocumentFragment();
        foreach ($parts as $i => $part) {
            if ($i % 2 === 0) {
                if ($part !== '') {
                    $frag->appendChild($doc->createTextNode($part));
                }
                continue;
            }
            // точку или скобку в конце предложения в ссылку не берём
            $tail = '';
            if (preg_match('~[.,;:!?)\]]+$~u', $part, $m)) {
                $tail = $m[0];
                $part = substr($part, 0, -strlen($tail));
            }
            $a = $doc->createElement('a');
            $a->setAttribute('href', $part);
            $a->setAttribute('target', '_blank');
            $a->setAttribute('rel', 'noopener');
            $a->appendChild($doc->createTextNode($part));
            $frag->appendChild($a);
            if ($tail !== '') {
                $frag->appendChild($doc->createTextNode($tail));
            }
        }
        $t->parentNode->replaceChild($frag, $t);
    }
}

/** Строка, где нет ничего, кроме ссылки на YouTube, становится встроенным видео. */
function news_embed_youtube_lines(DOMDocument $doc, DOMElement $root)
{
    $paras = [];
    foreach ($root->childNodes as $c) {
        if ($c instanceof DOMElement && $c->nodeName === 'p') {
            $paras[] = $c;
        }
    }
    foreach ($paras as $p) {
        $text = trim($p->textContent, " \t\n\r\0\x0B\xC2\xA0");
        if (!preg_match('~^\S+$~u', $text) || $p->getElementsByTagName('img')->length) {
            continue;
        }
        $id = news_youtube_id($text);
        if (!$id) {
            continue;
        }
        $f = $doc->createElement('iframe');
        foreach (['class' => 'ql-video', 'frameborder' => '0', 'allowfullscreen' => 'true', 'src' => 'https://www.youtube-nocookie.com/embed/' . $id] as $k => $v) {
            $f->setAttribute($k, $v);
        }
        $root->replaceChild($f, $p);
    }
}

/**
 * Пустой заголовок — берём первую строку текста (как в постах Telegram).
 * Если строка короткая, она становится заголовком и из текста убирается.
 */
function news_title_from_html($html)
{
    if (!preg_match('~^\s*<(p|h2|h3|blockquote)[^>]*>(.*?)</\1>~s', $html, $m)) {
        return [news_cut(news_text($html), 100), $html];
    }
    $first = trim(html_entity_decode(strip_tags($m[2]), ENT_QUOTES | ENT_HTML5, 'UTF-8'));
    if ($first !== '' && mb_strlen($first, 'UTF-8') <= 140 && strpos($m[2], '<img') === false && strpos($m[2], '<iframe') === false) {
        $rest = substr($html, strlen($m[0]));
        $rest = preg_replace('~^(\s*<p[^>]*>\s*(<br>)?\s*</p>)+~', '', $rest); // пустые строки после заголовка
        return [$first, trim($rest)];
    }
    return [news_cut(news_text($html), 100), $html];
}

// ------------------------------------------------------------------ public output

const NEWS_ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>';

/** HTML новости для сайта: видео — лёгким плеером сайта (грузится по клику), фото — лениво. */
function news_render(array $n)
{
    $html = preg_replace_callback('~<iframe[^>]*src="[^"]*/embed/([A-Za-z0-9_-]{11})[^"]*"[^>]*></iframe>~', function ($m) {
        return '<div class="yt" data-id="' . $m[1] . '"><button type="button" aria-label="Смотреть видео">'
            . '<span class="yt__play">' . NEWS_ICON_PLAY . '</span></button></div>';
    }, $n['html']);
    return str_replace('<img ', '<img loading="lazy" ', $html);
}

function news_card(array $n)
{
    $cover = news_cover($n);
    $media = $cover
        ? '<span class="news-card__media"><img src="' . h($cover) . '" alt="" loading="lazy"></span>'
        : '';
    return '<a class="news-card reveal' . ($cover ? '' : ' news-card--text') . '" href="' . h(news_url($n)) . '">' . $media
        . '<span class="news-card__body"><time datetime="' . h($n['date']) . '">' . h(news_date_ru($n['date'])) . '</time>'
        . '<span class="news-card__title">' . h($n['title']) . '</span>'
        . '<span class="news-card__text">' . h(news_excerpt($n, 180)) . '</span>'
        . '<span class="news-card__more">Читать <span aria-hidden="true">→</span></span></span></a>';
}

// ------------------------------------------------------------------ admin session

function news_https()
{
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https');
}

function admin_session_start()
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    $dir = NEWS_DATA . '/sessions';
    news_mkdir($dir);
    session_save_path($dir);
    ini_set('session.gc_maxlifetime', '2592000');
    ini_set('session.use_strict_mode', '1');
    session_name('mwadmin');
    session_set_cookie_params([
        'lifetime' => 2592000, // 30 дней — чтобы не вводить пароль каждый раз
        'path' => '/',
        'secure' => news_https(),
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(16));
    }
}

/** Для news.php: смотрит, вошёл ли админ, не заводя сессию обычным посетителям. */
function admin_logged_in()
{
    if (session_status() !== PHP_SESSION_ACTIVE) {
        if (empty($_COOKIE['mwadmin'])) {
            return false;
        }
        admin_session_start();
    }
    return !empty($_SESSION['admin']);
}

function admin_credentials()
{
    $cfg = require __DIR__ . '/config.php';
    $auth = is_file(NEWS_DATA . '/auth.json') ? json_decode((string)file_get_contents(NEWS_DATA . '/auth.json'), true) : null;
    if (is_array($auth) && !empty($auth['hash'])) {
        $cfg['hash'] = $auth['hash'];
    }
    return $cfg;
}

/** Не больше 8 неудачных попыток входа за 15 минут с одного адреса. */
function admin_login_blocked($ip, $failed = false)
{
    news_mkdir(NEWS_DATA);
    $file = NEWS_DATA . '/login-attempts.json';
    $fp = fopen($file, 'c+');
    flock($fp, LOCK_EX);
    $data = json_decode((string)stream_get_contents($fp), true) ?: [];
    $since = time() - 900;
    foreach ($data as $k => $times) {
        $data[$k] = array_values(array_filter($times, function ($t) use ($since) {
            return $t > $since;
        }));
        if (!$data[$k]) {
            unset($data[$k]);
        }
    }
    if ($failed) {
        $data[$ip][] = time();
    }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data));
    flock($fp, LOCK_UN);
    fclose($fp);
    return isset($data[$ip]) && count($data[$ip]) >= 8;
}
