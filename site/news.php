<?php
require __DIR__ . '/_news/lib.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$item = $id ? news_find($id) : null;
if ($item && empty($item['published']) && !admin_logged_in()) {
    $item = null;
}

// Три свежие новости для главной страницы
if (isset($_GET['format']) && $_GET['format'] === 'json') {
    header('Content-Type: application/json; charset=utf-8');
    $out = [];
    foreach (array_slice(news_published(), 0, 3) as $n) {
        $out[] = ['title' => $n['title'], 'date' => news_date_ru($n['date']), 'url' => news_url($n),
                  'cover' => news_cover($n), 'text' => news_excerpt($n, 160)];
    }
    echo json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

if ($id && !$item) {
    http_response_code(404);
}
$all = $id ? [] : news_published();
$pages = max(1, (int)ceil(count($all) / NEWS_PER_PAGE));
$p = min($pages, max(1, (int)(isset($_GET['page']) ? $_GET['page'] : 1)));
$list = array_slice($all, ($p - 1) * NEWS_PER_PAGE, NEWS_PER_PAGE);

$cover = $item ? news_cover($item) : null;
$metaTitle = $item ? $item['title'] : ($id ? 'Новость не найдена' : 'Новости');
$metaDesc = $item ? news_excerpt($item, 160) : 'Новости Игоря Вышегородцева: выступления, интервью, публикации и события.';
$canonical = 'https://mostwanted.consulting/news.php' . ($item ? '?id=' . $item['id'] : ($p > 1 ? '?page=' . $p : ''));
$ogImage = $cover ? ($cover[0] === '/' ? 'https://mostwanted.consulting' . $cover : $cover) : 'https://mostwanted.consulting/assets/img/echr-desk.jpg';
?>
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= h($metaTitle) ?> — Особо разыскиваемый управляющий</title>
<meta name="description" content="<?= h($metaDesc) ?>">
<link rel="canonical" href="<?= h($canonical) ?>">
<meta property="og:type" content="website">
<meta property="og:url" content="<?= h($canonical) ?>">
<meta property="og:site_name" content="Особо разыскиваемый управляющий">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="<?= h($metaTitle) ?> — Особо разыскиваемый управляющий">
<meta property="og:description" content="<?= h($metaDesc) ?>">
<meta property="og:image" content="<?= h($ogImage) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d1320">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=202610242107">
</head>
<body>
<a class="skip-link" href="#main">К содержанию</a>

<header class="header header--solid">
  <div class="wrap header__inner">
    <a class="brand" href="index.html" aria-label="На главную">
      <span class="brand__mark">ИВ</span>
      <span class="brand__text">
        <span class="brand__name">Игорь Вышегородцев</span>
        <span class="brand__sub">Особо разыскиваемый управляющий</span>
      </span>
    </a>
    <a class="header-tg" href="https://t.me/AllegatorSnap" target="_blank" rel="noopener" aria-label="Написать в Telegram"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg></a>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Основная навигация">
      <a class="nav__link" href="about.html">Обо мне</a><a class="nav__link" href="services.html">Чем могу помочь</a><a class="nav__link" href="advice.html">Советы</a><a class="nav__link" href="news.php" aria-current="page">Новости</a>
      <a class="nav__link" href="#contacts">Контакты</a>
      <a class="btn btn--primary nav__cta" href="https://t.me/AllegatorSnap" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg>Написать</a>
    </nav>
  </div>
</header>

<main id="main">

<?php if ($item): ?>
<section class="page-head page-head--news">
  <img class="page-head__bg" src="assets/img/echr-desk.jpg" alt="">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигационная цепочка"><a href="index.html">Главная</a><span aria-hidden="true">/</span><a href="news.php">Новости</a><span aria-hidden="true">/</span><span>Новость</span></nav>
    <div class="eyebrow"><?= h(news_date_ru($item['date'])) ?></div>
    <h1><?= h($item['title']) ?></h1>
    
  </div>
</section>
<?php if (empty($item['published'])): ?>
<div class="draft-note">Черновик — посетители сайта его не видят</div>
<?php endif; ?>
<section class="section">
  <div class="wrap service-layout">
    <article class="article news-article">
      <?= news_render($item) ?>
      <p class="news-back"><a class="link-arrow" href="news.php"><span aria-hidden="true">←</span> Все новости</a></p>
    </article>
    <aside class="aside">
      <div class="aside-card">
        <h3>Обсудить вашу ситуацию</h3>
        <p>Напишите в Telegram — коротко опишите, что происходит. Отвечу лично.</p>
        <a class="btn btn--gold" href="https://t.me/AllegatorSnap" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg>@AllegatorSnap</a>
      </div>
      <div class="aside-card aside-card--light">
        <h3>Telegram-канал</h3>
        <p>Новости выходят и в канале — там можно задать вопрос в комментариях.</p>
        <a class="btn btn--ghost" href="https://t.me/mostwantedmanager" target="_blank" rel="noopener">@mostwantedmanager</a>
      </div>
    </aside>
  </div>
</section>
<?php elseif ($id): ?>
<section class="page-head">
  <img class="page-head__bg" src="assets/img/echr-bench.jpg" alt="">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигационная цепочка"><a href="index.html">Главная</a><span aria-hidden="true">/</span><a href="news.php">Новости</a><span aria-hidden="true">/</span><span>Не найдено</span></nav>
    
    <h1>Новость не найдена</h1>
    <p class="lead">Возможно, её удалили или в адресе ошибка.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap"><a class="btn btn--primary" href="news.php">Все новости</a></div>
</section>
<?php else: ?>
<section class="page-head">
  <img class="page-head__bg" src="assets/img/hero-echr.jpg" alt="">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигационная цепочка"><a href="index.html">Главная</a><span aria-hidden="true">/</span><span>Новости</span></nav>
    <div class="eyebrow">Игорь Вышегородцев</div>
    <h1>Новости</h1>
    <p class="lead">Выступления, интервью, публикации и события. Обсуждение — в Telegram-канале.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
<?php if ($list): ?>
    <div class="news-grid"><?php foreach ($list as $n) echo news_card($n); ?></div>
<?php if ($pages > 1): ?>
    <nav class="news-pages" aria-label="Страницы новостей">
<?php for ($i = 1; $i <= $pages; $i++): ?>
      <a href="news.php<?= $i > 1 ? '?page=' . $i : '' ?>"<?= $i === $p ? ' aria-current="page"' : '' ?>><?= $i ?></a>
<?php endfor; ?>
    </nav>
<?php endif; ?>
<?php else: ?>
    <div class="news-empty">
      <p class="lead">Скоро здесь появятся новости.</p>
      <p>А пока — свежие события в Telegram-канале.</p>
      <a class="btn btn--primary" href="https://t.me/mostwantedmanager" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg>@mostwantedmanager</a>
    </div>
<?php endif; ?>
  </div>
</section>
<?php endif; ?>

</main>

<footer class="footer" id="contacts">
  <div class="wrap">
    <div class="contact-head reveal">
      <div class="eyebrow">Контакты</div>
      <h2>Расскажите о своей ситуации</h2>
      <p>Пишите в Telegram или WhatsApp, а если удобнее — на почту. Чем раньше вы начнёте защищаться, тем больше у вас вариантов.</p>
    </div>
    <div class="contacts">
      <a class="contact reveal" href="https://t.me/AllegatorSnap" target="_blank" rel="noopener">
        <span class="contact__icon"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg></span>
        <span><small>Связь в Telegram</small><strong>@AllegatorSnap</strong><em>Личные сообщения</em></span>
      </a>
      <a class="contact reveal" href="https://t.me/mostwantedmanager" target="_blank" rel="noopener">
        <span class="contact__icon"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg></span>
        <span><small>Telegram-канал</small><strong>@mostwantedmanager</strong><em>Новости и обратная связь — подписывайтесь</em></span>
      </a>
      <a class="contact reveal" href="https://wa.me/5491164113517" target="_blank" rel="noopener">
        <span class="contact__icon"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.5-.3z"/></svg></span>
        <span><small>WhatsApp</small><strong>+54 9 11 6411-3517</strong><em>Или найдите по нику @AllegatorSnap</em></span>
      </a>
      <a class="contact contact--email reveal" href="mailto:AllegatorSnap@protonmail.com">
        <span class="contact__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/></svg></span>
        <span><small>Электронная почта</small><strong>AllegatorSnap@<wbr>protonmail.com</strong><em>Для документов и подробных писем</em></span>
      </a>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Игорь Вышегородцев · Особо разыскиваемый управляющий</span>
      <nav class="footer__nav" aria-label="Нижняя навигация">
        <a href="index.html">Главная</a><a href="about.html">Обо мне</a><a href="services.html">Чем могу помочь</a><a href="advice.html">Советы</a><a href="news.php">Новости</a>
      </nav>
    </div>
  </div>
</footer>

<a class="fab" href="https://t.me/AllegatorSnap" target="_blank" rel="noopener" aria-label="Написать в Telegram"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg></a>
<script src="assets/js/main.js?v=202610242107" defer></script>
</body>
</html>
