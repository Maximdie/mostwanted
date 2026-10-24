# -*- coding: utf-8 -*-
"""
Сборка сайта «Особо разыскиваемый управляющий».

Все тексты лежат здесь. После правки запустите:  python build.py
Готовый сайт — в папке site/ (её целиком и заливать на хостинг).
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')

TG_PERSONAL = 'https://t.me/AllegatorSnap'
TG_CHANNEL = 'https://t.me/mostwantedmanager'
EMAIL = 'AllegatorSnap@protonmail.com'
WHATSAPP = 'https://wa.me/5491164113517'
WHATSAPP_PHONE = '+54 9 11 6411-3517'
FILM_ROUTE = 'https://filmfreeway.com/THEROUTEISSETATrusteesCase'
SITE_NAME = 'Особо разыскиваемый управляющий'
DOMAIN = 'https://mostwanted.consulting'
PAGES = []  # для sitemap.xml
VERSION = __import__('time').strftime('%Y%m%d%H%M')  # сбрасывает кэш браузера при каждой сборке

ICON_TG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3c.3-1.2-.9-2.2-2-1.7L2.8 9.4c-1.2.5-1.1 2.2.1 2.6l4.3 1.3 1.7 5.3c.3 1 1.6 1.3 2.3.5l2.4-2.4 4.4 3.2c.9.7 2.2.2 2.5-.9l3.4-14.7zM9.6 14.1l8.2-7.4-6.5 8.6-.3 3.1-1.4-4.3z"/></svg>')
ICON_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.5-.3z"/></svg>')
ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
             '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/></svg>')
ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW = '<span aria-hidden="true">→</span>'

NAV = [
    ('about.html', 'Обо мне'),
    ('services.html', 'Чем могу помочь'),
    ('advice.html', 'Советы'),
    ('news.php', 'Новости'),
]


def yt(video_id, label):
    return (f'<div class="yt" data-id="{video_id}"><button type="button" aria-label="{label}">'
            f'<span class="yt__play">{ICON_PLAY}</span></button></div>')


# ------------------------------------------------------------------ layout

def page(*, path, title, description, body, active=None, solid=True, og_image='assets/img/echr-desk.jpg',
         prelude='', canonical=None, og_image_url=None):
    depth = path.count('/')
    r = '../' * depth
    nav = ''.join(
        f'<a class="nav__link" href="{r}{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV)
    full_title = title if title == SITE_NAME else f'{title} — {SITE_NAME}'
    url = DOMAIN + '/' + ('' if path == 'index.html' else path)
    PAGES.append(url)
    canonical = canonical or url
    og_image_url = og_image_url or f'{DOMAIN}/{og_image}'
    html = prelude + f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d1320">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css?v={VERSION}">
</head>
<body>
<a class="skip-link" href="#main">К содержанию</a>

<header class="header{' header--solid' if solid else ''}">
  <div class="wrap header__inner">
    <a class="brand" href="{r}index.html" aria-label="На главную">
      <span class="brand__mark">ИВ</span>
      <span class="brand__text">
        <span class="brand__name">Игорь Вышегородцев</span>
        <span class="brand__sub">Особо разыскиваемый управляющий</span>
      </span>
    </a>
    <a class="header-tg" href="{TG_PERSONAL}" target="_blank" rel="noopener" aria-label="Написать в Telegram">{ICON_TG}</a>
    <button class="burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Основная навигация">
      {nav}
      <a class="nav__link" href="#contacts">Контакты</a>
      <a class="btn btn--primary nav__cta" href="{TG_PERSONAL}" target="_blank" rel="noopener">{ICON_TG}Написать</a>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="footer" id="contacts">
  <div class="wrap">
    <div class="contact-head reveal">
      <div class="eyebrow">Контакты</div>
      <h2>Расскажите о своей ситуации</h2>
      <p>Пишите в Telegram или WhatsApp, а если удобнее — на почту. Чем раньше вы начнёте защищаться, тем больше у вас вариантов.</p>
    </div>
    <div class="contacts">
      <a class="contact reveal" href="{TG_PERSONAL}" target="_blank" rel="noopener">
        <span class="contact__icon">{ICON_TG}</span>
        <span><small>Связь в Telegram</small><strong>@AllegatorSnap</strong><em>Личные сообщения</em></span>
      </a>
      <a class="contact reveal" href="{TG_CHANNEL}" target="_blank" rel="noopener">
        <span class="contact__icon">{ICON_TG}</span>
        <span><small>Telegram-канал</small><strong>@mostwantedmanager</strong><em>Новости и обратная связь — подписывайтесь</em></span>
      </a>
      <a class="contact reveal" href="{WHATSAPP}" target="_blank" rel="noopener">
        <span class="contact__icon">{ICON_WA}</span>
        <span><small>WhatsApp</small><strong>{WHATSAPP_PHONE}</strong><em>Или найдите по нику @AllegatorSnap</em></span>
      </a>
      <a class="contact contact--email reveal" href="mailto:{EMAIL}">
        <span class="contact__icon">{ICON_MAIL}</span>
        <span><small>Электронная почта</small><strong>{EMAIL.replace('@', '@<wbr>')}</strong><em>Для документов и подробных писем</em></span>
      </a>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Игорь Вышегородцев · {SITE_NAME}</span>
      <nav class="footer__nav" aria-label="Нижняя навигация">
        <a href="{r}index.html">Главная</a>{''.join(f'<a href="{r}{h}">{l}</a>' for h, l in NAV)}
      </nav>
    </div>
  </div>
</footer>

<a class="fab" href="{TG_PERSONAL}" target="_blank" rel="noopener" aria-label="Написать в Telegram">{ICON_TG}</a>
<script src="{r}assets/js/main.js?v={VERSION}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, *path.split('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('  ', path)


def page_head(title, lead, crumbs, eyebrow=None, bg=None, r='', mod=''):
    cr = f'<a href="{r}index.html">Главная</a>'
    for href, label in crumbs:
        cr += '<span aria-hidden="true">/</span>' + (f'<a href="{r}{href}">{label}</a>' if href else f'<span>{label}</span>')
    bg_html = f'<img class="page-head__bg" src="{r}{bg}" alt="">' if bg else ''
    eb = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''
    lead_html = f'<p class="lead">{lead}</p>' if lead else ''
    return f'''<section class="page-head{' ' + mod if mod else ''}">
  {bg_html}
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигационная цепочка">{cr}</nav>
    {eb}
    <h1>{title}</h1>
    {lead_html}
  </div>
</section>'''


# ------------------------------------------------------------------ services

SERVICES = [
    dict(
        slug='red-notice', title='Снять Red Notice',
        short='Дважды меня объявляли в розыск через Интерпол — и дважды Red Notice был снят. Знаю процедуру изнутри.',
        tg='https://t.me/mostwantedmanager/69',
        lead='Дважды меня объявляли в международный розыск по линии Интерпола. Дважды Red Notice был снят. Я знаю эту процедуру не по учебникам, а по собственному делу.',
        body=f'''
<h2>Что такое Red Notice</h2>
<p>Red Notice («красное уведомление») — это запрос правоохранительных органов одной страны к полиции других стран: найти человека и временно задержать его до решения вопроса об экстрадиции. Это не ордер на арест и не приговор. Это версия обвинения, которая обязана выдержать проверку на соответствие правилам самого Интерпола.</p>

<h2>Как его снимают</h2>
<p>Окончательное решение об удалении данных принимает Комиссия по контролю за файлами Интерпола (CCF) — независимый орган внутри организации. Устав Интерпола запрещает любое вмешательство в дела политического, военного, религиозного или расового характера, а сама работа организации должна соответствовать духу Всеобщей декларации прав человека.</p>
<p>Значит, задача защиты — документально показать, что запрос нарушает эти правила: содержит противоречия и неточные данные, имеет признаки политического заказа или нарушает права человека.</p>

<blockquote>«В 2024 году Интерпол рассмотрел возражения Игоря и снял с него Red Notice, признав, что нет оснований для розыска, задержания и депортации в Россию».<br><small>— «100 самых влиятельных персон банкротства 2024–2025», PROбанкротство</small></blockquote>

<h2>Как я могу помочь</h2>
<ul>
  <li>Оценить, на каком основании выставлено уведомление и есть ли в нём уязвимости.</li>
  <li>Подготовить возражения и комплект документов для CCF.</li>
  <li>Сопровождать процедуру до решения Комиссии.</li>
  <li>Подсказать, как вести себя, пока уведомление действует: куда можно ездить, а куда нельзя.</li>
</ul>

<h2>Моя история — в интервью</h2>
{yt('qr02aXK6TLQ', 'Интервью: Дважды в розыске Интерпола')}
<p class="muted">«Дважды в розыске Интерпола: как так?» — интервью каналу ARGA. Без взяток. Без побега. Только грамотная стратегия и поддержка команды.</p>
'''),
    dict(
        slug='extradition', title='Защитить от экстрадиции',
        short='Розыск через Интерпол — не приговор. Это возможность для защиты и юридического оспаривания.',
        tg='https://t.me/mostwantedmanager/67',
        lead='Розыск через Интерпол — мощный инструмент, но он работает по чётким правилам, которые должны предотвращать его политическое использование. Если уведомление нарушает эти правила, это не приговор, а возможность для защиты.',
        body='''
<p>Я прошёл через задержания и тюрьмы России, Хорватии, Бельгии и Испании. Я знаю, как выглядит экстрадиционный процесс глазами того, кого пытаются выдать, — и что нужно делать в первые часы и дни.</p>

<h2>На что обращать внимание</h2>
<h3>Процедуры CCF</h3>
<p>Именно Комиссия по контролю за файлами Интерпола (CCF) принимает окончательное решение об отмене уведомлений. Подготовка материалов для CCF требует знания процедур, международных стандартов прав человека и практики рассмотрения жалоб.</p>

<h3>Документируйте любые нарушения</h3>
<p>Если удаётся документально показать, что запрос содержит противоречия, неточные данные или нарушает права человека, это существенно усиливает позицию — и в CCF, и в суде, который решает вопрос о выдаче.</p>

<h3>Следите за практикой</h3>
<p>Интерпол периодически публикует отчёты о том, какие уведомления были отменены и по каким причинам. Это даёт представление о текущих стандартах и аргументах, которые работают.</p>

<div class="note"><strong>Вывод.</strong> Утечки данных показывают, что отдельные запросы вызывали серьёзные вопросы у независимых органов Интерпола. Если есть основания полагать, что уведомление нарушает правила, — его можно и нужно оспаривать.</div>
'''),
    dict(
        slug='relocation', title='Подобрать страну для релокации',
        short='Аргентина, Эквадор, страны Евросоюза — где вы будете в безопасности и сможете жить нормальной жизнью.',
        tg='https://t.me/argentinaforrussian',
        tg_label='Канал «Аргентина для русских»',
        lead='Аргентина, Эквадор, страны Евросоюза. Помогу выбрать страну, где вы будете в безопасности и сможете жить нормальной жизнью — а не просто пересидеть.',
        body='''
<h2>Что важно при выборе страны</h2>
<ul>
  <li><strong>Правовая защита.</strong> Есть ли у страны договор об экстрадиции с Россией, как её суды относятся к запросам о выдаче и к уведомлениям Интерпола.</li>
  <li><strong>Легализация.</strong> Насколько реально получить визу, ВНЖ, а затем и гражданство — и в какие сроки.</li>
  <li><strong>Жизнь.</strong> Язык, стоимость жизни, климат, школы для детей, медицина.</li>
  <li><strong>Сообщество.</strong> Есть ли русскоязычная диаспора, которая поможет на первых порах.</li>
  <li><strong>Деньги.</strong> Можно ли открыть счёт, работать удалённо, вести бизнес.</li>
</ul>

<h2>Направления</h2>
<p><strong>Аргентина и Эквадор</strong> — страны, которые я знаю изнутри. О жизни в Аргентине для русскоязычных — в отдельном Telegram-канале.</p>
<p><strong>Европейский союз</strong> — с учётом того, что требования к россиянам постоянно меняются и маршрут нужно выстраивать индивидуально.</p>
'''),
    dict(
        slug='adaptation', title='Адаптация в стране релокации',
        short='Жильё, работа, водительские права, языковые курсы, русскоязычные сообщества.',
        tg='https://t.me/argentinaforrussian/2116',
        lead='Переезд — это только начало. Самое трудное — первые месяцы на новом месте. Помогаю пройти их быстрее и без лишних ошибок.',
        body='''
<h2>С чем помогаю</h2>
<ul>
  <li><strong>Жильё</strong> — как снять квартиру без местной кредитной истории и не попасть на мошенников.</li>
  <li><strong>Работа</strong> — легальные варианты заработка для иностранца, удалённая работа, свой бизнес.</li>
  <li><strong>Водительские права</strong> — замена или получение местных прав.</li>
  <li><strong>Языковые курсы</strong> — где и как учить язык страны.</li>
  <li><strong>Русскоязычные сообщества</strong> — люди, которые уже прошли этот путь и помогут советом.</li>
</ul>

<h2>Это работает: пример</h2>
<p>В стриме «Погружение в банкротство» мы разговаривали с Дмитрием Шишкиным — бывшим арбитражным управляющим с Сахалина. Бывший моряк, арбитражный управляющий в России, а теперь — нотариус и владелец бизнеса во Флориде. Он рассказал, как учился в США, как живёт его семья и как найти своё дело на новом месте. Учиться никогда не поздно.</p>
'''),
    dict(
        slug='second-passport', title='Подобрать второй паспорт',
        short='Южная Америка, Африка, Евросоюз, США — «запасной аэродром», который нужно готовить заранее.',
        tg='https://t.me/argentinaforrussian/2618',
        lead='«Я бы посоветовал себе иметь „запасной аэродром“ на случай уголовного преследования». Второй паспорт — и есть такой аэродром.',
        body='''
<h2>Зачем нужен второй паспорт</h2>
<p>Второе гражданство даёт свободу передвижения, возможность открыть счёт за рубежом и — главное — дополнительную защиту, если на родине начнётся уголовное преследование. Готовить его нужно заранее: когда дело уже возбуждено, вариантов становится гораздо меньше.</p>

<h2>Направления</h2>
<ul>
  <li><strong>Южная Америка</strong> — страны с относительно быстрым путём к гражданству через ВНЖ.</li>
  <li><strong>Африка</strong> — новые программы гражданства за инвестиции. Например, Ботсвана объявила о запуске такой программы, чтобы диверсифицировать экономику, зависящую от экспорта алмазов.</li>
  <li><strong>Евросоюз</strong> — по происхождению или через натурализацию.</li>
  <li><strong>США</strong> — через долгосрочный статус и натурализацию.</li>
</ul>
<p>Подходящий вариант зависит от ваших корней, бюджета и сроков. Подберём реалистичный путь именно для вас.</p>
'''),
    dict(
        slug='judge-ai', title='Альтернативный приговор от JudgeAI',
        short='Мнение электронного судьи с искусственным интеллектом по вашему делу — как экспертный документ.',
        tg='https://t.me/mostwantedmanager/87',
        lead='У вас уголовное преследование? Вы получили обвинительное заключение и не согласны с ним? Или вам уже вынесли несправедливый приговор?',
        body='''
<p>Вы можете узнать мнение специализированного искусственного интеллекта — электронного судьи <strong>JudgeAI</strong>, который работает по алгоритму судебной коллегии.</p>
<p>Результат — альтернативный приговор, который затем можно использовать как экспертное мнение: в жалобах, обращениях и публичной защите.</p>

<h2>Для кого</h2>
<ul>
  <li>Вы не согласны с обвинительным заключением.</li>
  <li>Вам вынесли приговор, который вы считаете несправедливым.</li>
  <li>Вам нужна независимая оценка дела до суда.</li>
</ul>

<div class="note">Я лично протестировал этот сервис. Подробно — в моей колонке для «Абирега»: <a href="https://abireg.ru/newsitem/103963/" target="_blank" rel="noopener">«Искусственный интеллект в мантии: „тест-драйв“ сервиса неподкупного судьи»</a>.</div>
'''),
    dict(
        slug='expert-opinion', title='Экспертное заключение по уголовному делу',
        short='Взгляд человека, который сам прошёл уголовное преследование и 25 лет работал в банкротстве.',
        tg='https://t.me/mostwantedmanager/99',
        lead='Взгляд на ваше дело от человека, который сам прошёл уголовное преследование и четверть века работал арбитражным управляющим.',
        body='''
<h2>Что входит</h2>
<ul>
  <li>Анализ обвинения и материалов уголовного дела.</li>
  <li>Особое внимание — делам, связанным с банкротством, работой арбитражных управляющих и бизнесом.</li>
  <li>Слабые места обвинения и процессуальные нарушения.</li>
  <li>Письменное заключение с аргументами для защиты.</li>
</ul>

<h2>Почему это работает</h2>
<p>За плечами — более 130 процедур банкротства, в том числе на стратегических предприятиях, 20 лет руководства региональным филиалом СРО, обучение в Совете Европы по подготовке жалоб в ЕСПЧ и собственное уголовное дело, пройденное от начала до снятия Red Notice.</p>
<blockquote>Его работа — это сплав юриспруденции, оперативной психологии и кибербезопасности.<br><small>— из независимого анализа Telegram-канала</small></blockquote>
'''),
    dict(
        slug='us-company', title='Открыть счёт и компанию в США',
        short='LLC во Флориде удалённо, банковский счёт и карта, юридический адрес, почта и отчётность.',
        tg='https://t.me/argentinaforrussian/2108',
        lead='Хотите хранить деньги в одной из самых надёжных юрисдикций? Планируете инвестировать в США или открыть там бизнес? Откладываете на учёбу детей в американском университете?',
        body='''
<p>Открыть личный счёт в американском банке без визита в отделение невозможно. А вот учредить компанию с банковским счётом — можно удалённо.</p>

<h2>Что это даёт</h2>
<ol>
  <li>Доступ к надёжной банковской системе США.</li>
  <li>Управление финансами удалённо из любой точки мира.</li>
  <li>Сохранность ваших средств.</li>
  <li>Банковскую карту для расчётов и снятия наличных.</li>
</ol>

<h2>Под ключ</h2>
<ul>
  <li>Учреждение LLC (аналог ООО) во Флориде — удалённо.</li>
  <li>Открытие бизнес-счёта и карты для использования по всему миру.</li>
  <li>Юридический адрес и получение почты.</li>
  <li>Сдача отчётности.</li>
</ul>
<p>Работаем вместе с IMM Consulting — зарегистрированным агентом во Флориде.</p>
'''),
    dict(
        slug='publicity', title='Вывести ситуацию из забвения в публичную плоскость',
        short='Публикации, колонки, интервью и стримы. Когда о деле знают, его труднее решить «тихо».',
        tg='https://t.me/mostwantedmanager/86',
        lead='Когда о вашем деле молчат, его проще решить не в вашу пользу. Публичность — тоже инструмент защиты.',
        body=f'''
<h2>Как это работает</h2>
<ul>
  <li>Публикации и экспертные колонки в профильных СМИ.</li>
  <li>Интервью на YouTube-каналах.</li>
  <li>Стримы и посты в Telegram-каналах с профессиональной аудиторией.</li>
  <li>Подготовка позиции так, чтобы её услышали — и юристы, и журналисты, и широкая аудитория.</li>
</ul>

<h2>Примеры</h2>
<ul>
  <li>Колонка в «Абиреге»: <a href="https://abireg.ru/newsitem/103963/" target="_blank" rel="noopener">«Искусственный интеллект в мантии: „тест-драйв“ сервиса неподкупного судьи»</a>.</li>
  <li>Профиль в информационном агентстве <a href="https://probankrotstvo.ru/persons/igor-vysegorodcev-244" target="_blank" rel="noopener">PROбанкротство</a> и в рейтинге «100 самых влиятельных персон банкротства 2024–2025».</li>
  <li>Еженедельный стрим «Погружение в банкротство» в канале <a href="https://t.me/bankrotorg2" target="_blank" rel="noopener">«Банкротство. the other side»</a>.</li>
  <li>Интервью о двух розысках через Интерпол — ниже.</li>
</ul>
{yt('1SsDqryk6t0', 'Интервью: как из «Абордажного управляющего» я стал «Особо разыскиваемым управляющим»')}
'''),
    dict(
        slug='notary-online', title='Нотариальная доверенность онлайн',
        short='Доверенность от нотариуса Флориды с апостилем, действующая в России. Без визита в консульство.',
        tg='https://t.me/mostwantedmanager/111',
        lead='Доверенность для России — дистанционно, без визита в консульство РФ. И без необходимости сообщать, где вы находитесь.',
        body='''
<h2>Что входит</h2>
<ul>
  <li>Подготовка текста доверенности.</li>
  <li>Онлайн-заверение у нотариуса штата Флорида.</li>
  <li>Получение апостиля через государственный орган.</li>
  <li>Отправка оригинала в Россию международной почтой.</li>
</ul>

<h2>Кому подходит</h2>
<p>Релокантам, которые не могут или не хотят идти в консульство РФ. Или не хотят, чтобы их местонахождение стало известно в России.</p>

<div class="note">Для организации процедуры можно обращаться к американскому нотариусу напрямую — <a href="https://t.me/immconsult" target="_blank" rel="noopener">@immconsult</a>. Можно писать и говорить по-русски.</div>
'''),
    dict(
        slug='online-wedding', title='Свадьба онлайн из любой страны мира',
        short='Официальный брак штата Юта по видеосвязи. Жених, невеста и регистратор — в разных странах.',
        tg='https://t.me/mostwantedmanager/233',
        lead='Онлайн-брак в штате Юта — это не «виртуальная церемония», а официальная государственная регистрация. Регистратор находится в Юте, а молодожёны и свидетели — в любой точке мира.',
        body='''
<h2>Как это работает</h2>
<p>Законодательство штата Юта (округ Юта) позволяет проводить бракосочетание в формате видеоконференции (Zoom).</p>

<h2>Законность и международное признание</h2>
<p>Ключ к легальности такого брака — апостиль. По Гаагской конвенции 1961 года документ с апостилем, выданный официальным органом США, принимается другими странами-участницами.</p>
<ul>
  <li><strong>Израиль.</strong> В марте 2023 года Верховный суд Израиля обязал МВД признавать «ютские браки». Теперь это основной способ гражданской регистрации для тех, кто не хочет или не может заключать религиозный брак. Подходит и для легализации супруга-иностранца.</li>
  <li><strong>Евросоюз.</strong> Большинство стран ЕС (Германия, Франция и др.) признают такие браки при наличии апостиля. В некоторых странах (например, в Австрии) возможны сложности, если закон требует физического присутствия сторон. В целом для иммиграции в ЕС такой брак считается действительным.</li>
  <li><strong>Россия.</strong> Браки, заключённые за границей по местному законодательству, признаются, если нет препятствий из ст. 14 СК РФ (близкое родство, нерасторгнутый прошлый брак). Нужно свидетельство с апостилем и нотариально заверенным переводом.</li>
</ul>

<h2>Сроки и стоимость</h2>
<p><strong>Сроки:</strong> от подачи заявки до церемонии — от 24 часов до нескольких дней. Электронное свидетельство доступно сразу, бумажный оригинал с апостилем приходит почтой за 2–6 недель.</p>
<p><strong>Стоимость:</strong> госпошлина за лицензию — около 100–110 долларов. Услуги «под ключ» (с апостилем и пересылкой) — от 500 до 1000 долларов.</p>

<h2>Порядок</h2>
<ol>
  <li><strong>Заявка</strong> — данные паспортов подаются на сайте округа.</li>
  <li><strong>Лицензия</strong> — разрешение на брак, действует 32 дня.</li>
  <li><strong>Церемония</strong> — онлайн-встреча в Zoom с регистратором и двумя свидетелями.</li>
  <li><strong>Легализация</strong> — апостиль в офисе секретаря штата Юта.</li>
  <li><strong>Доставка</strong> — оригинал документа курьерской службой (FedEx/DHL).</li>
</ol>

<h2>Нюансы</h2>
<ul>
  <li><strong>Технический сбой.</strong> Если связь прервётся в момент «I do», церемонию придётся начинать заново.</li>
  <li><strong>Иммиграция в США.</strong> Для консульства США (виза невесты/жены) такой брак считается завершённым только после физической встречи супругов после свадьбы.</li>
  <li><strong>Возраст.</strong> Обоим участникам должно быть больше 18 лет.</li>
</ul>
<p>Это самый быстрый и легальный путь для интернациональных пар обрести статус семьи без лишних перелётов и бюрократии.</p>
'''),
    dict(
        slug='allegation', title='Обвиняют вас? Проверим, кто дал им на это право',
        short='Проверяем легитимность самого преследования и предъявляем встречные претензии.',
        tg='https://t.me/mostwantedmanager/531',
        lead='Следствие расследует. Прокуратура обвиняет. Суд оценивает. Интерпол разыскивает. Каждое из этих утверждений — allegation: версия, которая ещё не доказана и обязана выдержать проверку на законность.',
        body='''
<p>Мы не оправдываем — мы проверяем легитимность самого преследования. Там, где обвинение построено на политическом заказе, процессуальном нарушении или злоупотреблении международным розыском, мы предъявляем встречные претензии: Интерполу, прокуратуре, следственным органам, суду, международным структурам.</p>

<h2>Через какие органы работаем</h2>
<ul>
  <li>Комиссия по контролю за файлами Интерпола (CCF)</li>
  <li>Комитет ООН по правам человека</li>
  <li>Рабочая группа ООН по произвольным задержаниям</li>
  <li>Специальные докладчики ООН</li>
  <li>Европейский суд по правам человека</li>
</ul>
'''),
]

ADVICE = [
    'Сделайте <strong>два загранпаспорта</strong> для всех членов семьи — со сдвигом во времени начала и окончания действия.',
    'По возможности оформите <strong>международные водительские права</strong>.',
    'Получите свежую <strong>справку об отсутствии судимости</strong>. Берите её регулярно.',
    'Заберите с собой <strong>все личные документы</strong>: права на все виды транспорта, свидетельства о рождении всех членов семьи, свидетельство о браке, дипломы, справку 2-НДФЛ. Сделайте их перевод с апостилем на английский или на язык страны, где у вас есть второй паспорт.',
    'Не храните все эти документы <strong>дома</strong> — ни по месту прописки, ни по месту реального проживания (часто это два разных места).',
    'Отсканируйте все необходимые документы и сохраните <strong>электронные копии</strong> на ноутбуке, в облаке или на частном сервере.',
    'При покупке наличной или безналичной валюты <strong>берите справку о покупке</strong>. Происхождение валюты придётся доказывать. Происхождение доходов — отдельная тема.',
    '<strong>Полечите зубы</strong> и пройдите медицинское обследование. Купите лекарства, которые принимаете регулярно: за границей другие правила их покупки.',
    'Оформите <strong>карту иностранного банка</strong>. Или две.',
    'Переоформите всё движимое имущество — машины, лодки, яхты, акции, доли в компаниях — <strong>на родственников или близких людей</strong>.',
    'Сделайте <strong>генеральную доверенность</strong> от всех уезжающих на нескольких родственников или доверенных людей. Помимо стандартного набора (получение денег и документов) в ней должно быть право получать и восстанавливать SIM-карты на ваше имя, запрашивать и получать справки об отсутствии судимости, открывать и закрывать банковские карты. Срок действия — максимально возможный.',
    'Копите <strong>подушку безопасности</strong> — в долларах, евро, криптовалюте, на счёте в иностранном банке.',
    'Получите <strong>второе гражданство</strong> (второй паспорт).',
    'Оформите <strong>шенгенскую визу, визу в США</strong> и в другую страну, куда можно выехать и попросить убежища (например, в Южную Корею).',
    'Обязательно <strong>учите иностранный язык</strong>. Английский — универсальный. Если есть второй паспорт Испании или Аргентины — учите испанский. Если есть длительная виза во Францию (например, виза талантов) — французский.',
    '<strong>Закройте</strong> в России ненужные карты и банковские счета.',
    '<strong>Оставьте</strong> карты для онлайн-банкинга.',
    'Заведите <strong>две-три электронные почты</strong> на доменах gmail.com и proton.me.',
    'Договоритесь, чтобы кто-то <strong>проверял почтовый ящик</strong> по адресу прописки и пересылал вам письма. А также ходил на почту и по доверенности забирал письма с уведомлением и другую заказную корреспонденцию.',
    'Договоритесь, чтобы кто-то <strong>присылал квитанции</strong> за квартиру или дом, консьержа — или платил за вас.',
    'Личные <strong>машины продайте или сдайте в аренду</strong>, чтобы их не угнали, пока вас нет.',
    '<strong>Наличные вывозите по частям</strong> и храните на счёте в банке, в банковской ячейке, в сейфе в вашей зарубежной квартире или у адвоката.',
    'Если вы ожидаете проблем с Интерполом — заключите <strong>контракт с иностранным адвокатом</strong>.',
    'Купите <strong>иностранный телефон с местной SIM-картой</strong>. Не ввозите его в Россию.',
    'Запишите <strong>все пароли</strong> — к почтам, Госуслугам, картам, SIM-картам и всему остальному — на бумаге и в файле на сервере.',
    'Соберите <strong>«тревожный чемоданчик»</strong>: бельё, носки, наличные, лекарства, зарядки, пауэрбанк, дорожный телефон (оформленный не на вас и выключенный до пересечения границы) — чтобы просто взять и уехать. Это должна быть ручная кладь, не багаж.',
]


# ------------------------------------------------------------------ pages

def build_index():
    svc_items = ''.join(
        f'<li><a href="services/{s["slug"]}.html"><span class="svc-list__num">{i:02d}</span>'
        f'<span class="svc-list__title">{s["title"]}</span><span class="svc-list__arrow">→</span></a></li>'
        for i, s in enumerate(SERVICES, 1))
    preview = ''.join(f'<li><span>{t}</span></li>' for t in ADVICE[:4])
    body = f'''
<section class="hero">
  <picture>
    <source media="(max-width: 760px)" srcset="assets/img/hero-mobile.jpg">
    <img class="hero__bg" src="assets/img/echr-desk.jpg" alt="Игорь Вышегородцев в зале Европейского суда по правам человека, Страсбург" fetchpriority="high">
  </picture>
  <div class="wrap hero__content">
    <div class="hero__text">
    <div class="hero__kicker">Игорь Вышегородцев</div>
    <h1 class="hero__title">Особо разыскиваемый управляющий</h1>
    <p class="hero__slogan">Жизнь нужно прожить так, чтобы тебя разыскивал Интерпол. <em>Дважды…</em></p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="services.html">Чем я могу помочь</a>
      <a class="btn btn--ghost" href="{TG_PERSONAL}" target="_blank" rel="noopener">{ICON_TG}Написать в Telegram</a>
    </div>
    </div>
    <div class="facts">
      <div class="fact"><span class="fact__num">2 раза</span><span class="fact__label">снят Red Notice Интерпола</span></div>
      <div class="fact"><span class="fact__num">25 лет</span><span class="fact__label">арбитражным управляющим</span></div>
      <div class="fact"><span class="fact__num">4 страны</span><span class="fact__label">опыт тюрем: Россия, Хорватия, Бельгия, Испания</span></div>
      <div class="fact"><span class="fact__num">2 высших</span><span class="fact__label">техническое и юридическое образование</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap intro">
    <figure class="portrait reveal">
      <img src="assets/img/portrait.jpg" alt="Портрет Игоря Вышегородцева" loading="lazy" width="426" height="576">
    </figure>
    <div class="reveal">
      <div class="eyebrow">Кто я такой</div>
      <h2>Меня зовут Игорь Вышегородцев</h2>
      <p class="statement">Два раза меня разыскивал Интерпол. <strong>Два раза я доказал, что не виновен.</strong></p>
      <ul class="creds">
        <li>Опыт тюрем России, Хорватии, Бельгии, Испании</li>
        <li>Два высших образования — техническое и юридическое</li>
        <li>Четверть века — арбитражный управляющий, более 130 процедур банкротства</li>
        <li>Обучение в Совете Европы: обращение в Европейский суд по правам человека</li>
      </ul>
      <p class="signature">Я смогу вас защитить.</p>
      <a class="link-arrow" href="about.html">Подробнее обо мне: фильмы, интервью и рассказ {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--paper2" data-latest-news hidden>
  <div class="wrap">
    <div class="news-latest__head">
      <div>
        <div class="eyebrow">Новости</div>
        <h2>Что нового</h2>
      </div>
      <a class="link-arrow" href="news.php">Все новости {ARROW}</a>
    </div>
    <div class="news-grid" data-latest-list></div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow">Услуги</div>
      <h2>Чем я могу вам помочь</h2>
      <p class="lead">Двенадцать направлений — от снятия Red Notice до онлайн-свадьбы из любой страны мира. Нажмите на пункт, чтобы узнать подробности.</p>
    </div>
    <ul class="svc-list reveal">{svc_items}</ul>
  </div>
</section>

<section class="section section--dark2">
  <div class="wrap">
    <div class="section-head section-head--center reveal">
      <div class="eyebrow">Без иллюзий</div>
      <h2>Так выглядит «возвращение на Родину»</h2>
    </div>
    <figure class="cinema reveal">
      <button class="cinema__btn" type="button" data-full="assets/img/rodina.jpg">
        <img src="assets/img/rodina.jpg" alt="«Родина ждёт вас, сволочи!» — экстрадиция в Россию: самолёт, сотрудники ФСБ и Интерпола, дело «Враг народа»" width="960" height="640">
      </button>
      <figcaption>«Родина ждёт вас, сволочи!» — Игорь Вышегородцев</figcaption>
    </figure>
    <div class="cinema__text reveal">
      <p class="lead">Если на вас уже завели дело — или вот-вот заведут, — времени на раздумья мало. Лучше подготовиться заранее, чем объяснять потом из камеры, почему не успели.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="advice.html">Как подготовиться</a>
        <a class="btn btn--ghost" href="{TG_PERSONAL}" target="_blank" rel="noopener">Обсудить ситуацию</a>
      </div>
    </div>
  </div>
</section>

<dialog class="lightbox" aria-label="Просмотр изображения">
  <div class="lightbox__inner">
    <button class="lightbox__close" type="button" aria-label="Закрыть">×</button>
    <img src="" alt="">
  </div>
</dialog>

<section class="section">
  <div class="wrap band">
    <div class="reveal">
      <div class="eyebrow">Советы от особо разыскиваемого управляющего</div>
      <h2>Как подготовиться к релокации, если грозит уголовное дело</h2>
      <p class="lead">Список, проверенный на себе. Видео и полный чек-лист — отмечайте, что уже сделано.</p>
      <ol class="preview-list">{preview}</ol>
      <a class="btn btn--primary" href="advice.html">Открыть все советы</a>
    </div>
    <div class="band__card reveal">
      <div class="band__big">26</div>
      <p>пунктов, которые нужно сделать до того, как за вами придут. Документы, деньги, связь, здоровье, «тревожный чемоданчик».</p>
    </div>
  </div>
</section>
'''
    page(path='index.html', title=SITE_NAME, solid=False,
         description='Игорь Вышегородцев — дважды снял с себя Red Notice Интерпола. Защита от экстрадиции, релокация, второй паспорт, экспертиза уголовных дел.',
         body=body)


def build_about():
    certs = [
        ('cert-echr-ru.jpg', 'Сертификат Совета Европы: «Успешное обращение в ЕСПЧ: от теории к практике», Страсбург, 2019, 40 часов', None),
        ('cert-echr-en.jpg', 'Certificate of attendance, Council of Europe, Strasbourg, 14–18 October 2019', None),
        ('letter-rlt.jpg', 'Благодарственное письмо арбитру Российского юридического турнира 2020, секция «Субсидиарная ответственность. Банкротство»', None),
        ('unodc-intro.jpg', 'UNODC (ООН): Introduction to Anti-Corruption, 2026', 'assets/docs/unodc-intro.pdf'),
        ('unodc-advanced.jpg', 'UNODC (ООН): Advanced Anti-Corruption — Prevention of Corruption, 2026', 'assets/docs/unodc-advanced.pdf'),
        ('unodc-judicial.jpg', 'UNODC (ООН): Судебные нормы поведения и этики, 2026', 'assets/docs/unodc-judicial.pdf'),
        ('top100-cover.jpg', 'PROбанкротство: «100 самых влиятельных персон банкротства 2024–2025»', None),
        ('top100-page.jpg', 'Страница об Игоре Вышегородцеве в рейтинге PROбанкротство', None),
    ]
    gal = ''.join(
        f'<figure class="gallery__item reveal"><button class="gallery__btn" type="button" data-full="assets/img/{img}">'
        f'<img src="assets/img/{img}" alt="{cap}" loading="lazy"></button>'
        f'<figcaption>{cap}{f" · <a href=\"{pdf}\" target=\"_blank\">PDF</a>" if pdf else ""}</figcaption></figure>'
        for img, cap, pdf in certs)

    body = f'''
{page_head('Обо мне', 'Арбитражный управляющий с 1999 года. Дважды в международном розыске — и дважды доказал, что не виновен. Теперь помогаю тем, кто оказался в похожей ситуации.', [(None, 'Обо мне')], eyebrow='Игорь Вышегородцев', bg='assets/img/hero-echr.jpg')}

<section class="section">
  <div class="wrap intro">
    <figure class="portrait reveal">
      <img src="assets/img/portrait.jpg" alt="Портрет Игоря Вышегородцева" width="426" height="576">
    </figure>
    <div class="reveal">
      <div class="eyebrow">Мои компетенции</div>
      <h2>Меня зовут Игорь Вышегородцев</h2>
      <p class="statement">Два раза меня разыскивал Интерпол. <strong>Два раза я доказал, что не виновен.</strong></p>
      <ul class="creds">
        <li>Опыт тюрем России, Хорватии, Бельгии, Испании</li>
        <li>Два высших образования — техническое и юридическое</li>
        <li>Опыт работы арбитражным управляющим — четверть века</li>
        <li>Обучение в Совете Европы и курсы ООН (UNODC) по противодействию коррупции и судебной этике</li>
      </ul>
      <p class="signature">Я смогу вас защитить.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="{TG_PERSONAL}" target="_blank" rel="noopener">{ICON_TG}@AllegatorSnap</a>
        <a class="btn btn--ghost" href="services.html">Чем я могу помочь</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><span class="stat__num">25 лет</span><span class="stat__label">арбитражным управляющим, 1999–2022</span></div>
      <div class="stat"><span class="stat__num">130+</span><span class="stat__label">процедур банкротства, в том числе на стратегических предприятиях</span></div>
      <div class="stat"><span class="stat__num">20 лет</span><span class="stat__label">директор Воронежского филиала СРО «Авангард»</span></div>
      <div class="stat"><span class="stat__num">ТОП-100</span><span class="stat__label">самых влиятельных персон банкротства 2024–2025 по версии PROбанкротство</span></div>
    </div>
  </div>
</section>

<section class="section" id="story">
  <div class="wrap story">
    <div class="reveal">
      <div class="eyebrow">Рассказ</div>
      <h2>«Особо разыскиваемый управляющий»</h2>
      <p class="lead">Реальная история о том, как меня искал Интерпол и нашёл в первый раз. И как я в первый раз снял с себя Red Notice.</p>
      <p>Когда прочитаете, напишите мне: верите вы в эту историю или нет?</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="https://author.today/work/489198" target="_blank" rel="noopener">Читать на Author.Today</a>
        <a class="btn btn--ghost" href="https://www.wattpad.com/story/403067516" target="_blank" rel="noopener">Читать на Wattpad</a>
      </div>
    </div>
    <blockquote class="epigraph reveal">
      Искусство лжи состоит не в том, чтобы лгать так, чтобы тебе верили. Искусство лжи состоит в том, чтобы говорить правду так, чтобы тебе не верили.
      <cite>Из рассказа</cite>
    </blockquote>
  </div>
</section>

<section class="section section--dark" id="films">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow">Кино</div>
      <h2>Фильмы обо мне</h2>
    </div>
    <div class="videos">
      <div class="video-card reveal">
        {yt('n9QGtc2pb-E', 'Фильм «Управляющий» (The Manager)')}
        <h3>«Управляющий» (The Manager)</h3>
        <p>Фильм об арбитражном управляющем из России: о работе по закону в стране беззакония и о человеке, которого хотят посадить в тюрьму вопреки закону. Участник трёх кинофестивалей, два приза.</p>
      </div>
      <div class="video-card reveal">
        <a class="film-link" href="{FILM_ROUTE}" target="_blank" rel="noopener">
          <span class="film-link__en">The Route Is Set. A Trustee’s Case</span>
          <strong>Путь определён</strong>
          <span class="film-link__sub">Дело доверительного управляющего</span>
          <span class="film-link__go">Страница фильма на FilmFreeway {ARROW}</span>
        </a>
        <h3>«Путь определён. Дело доверительного управляющего»</h3>
        <p>Второй фильм обо мне. Страница фильма — на FilmFreeway, международной платформе кинофестивалей.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark2" id="video">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow">Интервью</div>
      <h2>Видео</h2>
    </div>
    <div class="videos">
      <div class="video-card reveal">
        {yt('qr02aXK6TLQ', 'Интервью: Дважды в розыске Интерполом')}
        <h3>«Дважды в розыске Интерполом»</h3>
        <p>Интервью каналу ARGA. Дважды в международном розыске — и оба раза вышел из этого списка. Без взяток. Без побега.</p>
      </div>
      <div class="video-card reveal">
        {yt('1SsDqryk6t0', 'Интервью: как из Абордажного управляющего я стал Особо разыскиваемым управляющим')}
        <h3>Как из «Абордажного управляющего» я стал «Особо разыскиваемым управляющим»</h3>
        <p>О профессии, уголовном деле и о том, что происходит, когда система начинает охоту на арбитражного управляющего.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow">Профессиональное резюме</div>
      <h2>Путь</h2>
      <p>Полное профессиональное резюме — на сайте информационного агентства <a href="https://probankrotstvo.ru/persons/igor-vysegorodcev-244" target="_blank" rel="noopener">PROбанкротство</a>.</p>
    </div>
    <ol class="timeline reveal">
      <li><span class="timeline__year">1993</span><div><h3>Инженер-строитель</h3><p>Воронежский инженерно-строительный институт.</p></div></li>
      <li><span class="timeline__year">1999–2022</span><div><h3>Арбитражный управляющий</h3><p>Более 130 процедур банкротства, в том числе на стратегических предприятиях, среди них АО «Группа Е4». Опыт восстановления платёжеспособности предприятий.</p></div></li>
      <li><span class="timeline__year">2002–2022</span><div><h3>Директор Воронежского филиала СРО «Авангард»</h3><p>Двадцать лет руководства региональным филиалом саморегулируемой организации арбитражных управляющих.</p></div></li>
      <li><span class="timeline__year">2005</span><div><h3>Юрист</h3><p>Воронежский экономико-правовой институт.</p></div></li>
      <li><span class="timeline__year">2019</span><div><h3>Совет Европы, Страсбург</h3><p>Международный семинар «Успешное обращение в Европейский суд по правам человека: от теории к практике», 40 часов, лекторы — юристы и судьи ЕСПЧ.</p></div></li>
      <li><span class="timeline__year">2020</span><div><h3>Арбитр Российского юридического турнира</h3><p>Секция «Субсидиарная ответственность. Банкротство».</p></div></li>
      <li><span class="timeline__year">2023–2024</span><div><h3>Международный розыск — и снятие Red Notice</h3><p>Розыск в рамках уголовного дела, связанного с профессиональной деятельностью. В 2024 году Интерпол рассмотрел возражения и снял Red Notice, признав, что нет оснований для розыска, задержания и депортации в Россию.</p></div></li>
      <li><span class="timeline__year">2024</span><div><h3>Фильм «Управляющий»</h3><p>Фильм о работе арбитражного управляющего и несправедливом уголовном преследовании. Три кинофестиваля, два приза. <a href="#films">Смотреть</a></p></div></li>
      <li><span class="timeline__year">2024</span><div><h3>Стрим «Погружение в банкротство»</h3><p>Еженедельный международный стрим в Telegram-канале <a href="https://t.me/bankrotorg2" target="_blank" rel="noopener">«Банкротство. the other side»</a>. Консультирую арбитражных управляющих в сложных и уголовных ситуациях.</p></div></li>
      <li><span class="timeline__year">2026</span><div><h3>Курсы ООН (UNODC)</h3><p>Противодействие коррупции и судебные нормы поведения и этики.</p></div></li>
      <li><span class="timeline__year">2026</span><div><h3>XIV Уральский форум арбитражных управляющих</h3><p>Выступление на форуме перед коллегами — арбитражными управляющими.</p></div></li>
    </ol>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow">Документы</div>
      <h2>Сертификаты и признание</h2>
    </div>
    <div class="gallery">{gal}</div>

    <div class="section-head reveal mt-l">
      <div class="eyebrow">Страсбург</div>
      <h2>Европейский суд по правам человека</h2>
    </div>
    <div class="photos">
      <figure class="gallery__item reveal"><button class="gallery__btn" type="button" data-full="assets/img/hero-echr.jpg"><img src="assets/img/hero-echr.jpg" alt="В зале заседаний Большой палаты ЕСПЧ" loading="lazy"></button></figure>
      <figure class="gallery__item reveal"><button class="gallery__btn" type="button" data-full="assets/img/echr-desk.jpg"><img src="assets/img/echr-desk.jpg" alt="В зале ЕСПЧ, Страсбург" loading="lazy"></button></figure>
      <figure class="gallery__item reveal"><button class="gallery__btn" type="button" data-full="assets/img/echr-bench.jpg"><img src="assets/img/echr-bench.jpg" alt="У судейской скамьи ЕСПЧ" loading="lazy"></button></figure>
    </div>
  </div>
</section>

<dialog class="lightbox" aria-label="Просмотр изображения">
  <div class="lightbox__inner">
    <button class="lightbox__close" type="button" aria-label="Закрыть">×</button>
    <img src="" alt="">
  </div>
</dialog>
'''
    page(path='about.html', title='Обо мне', active='about.html',
         description='Игорь Вышегородцев: 25 лет арбитражным управляющим, дважды в розыске Интерпола и дважды доказал невиновность. Интервью, рассказ, резюме, сертификаты.',
         body=body)


def build_services():
    cards = ''.join(
        f'<a class="service reveal" href="services/{s["slug"]}.html"><span class="service__num">{i:02d}</span>'
        f'<h2 class="service__title">{s["title"]}</h2><p class="service__text">{s["short"]}</p>'
        f'<span class="service__more">Подробнее {ARROW}</span></a>'
        for i, s in enumerate(SERVICES, 1))
    body = f'''
{page_head('Чем я могу вам помочь', 'Двенадцать направлений, в каждом из которых у меня есть личный опыт или проверенные партнёры. Выберите, что вам нужно, — или просто напишите, и разберёмся вместе.', [(None, 'Чем могу помочь')], eyebrow='Услуги', bg='assets/img/echr-bench.jpg')}
<section class="section">
  <div class="wrap">
    <div class="services">{cards}</div>
  </div>
</section>
'''
    page(path='services.html', title='Чем я могу помочь', active='services.html',
         description='Снятие Red Notice, защита от экстрадиции, релокация и адаптация, второй паспорт, счёт и компания в США, онлайн-доверенность, онлайн-свадьба.',
         body=body)

    for i, s in enumerate(SERVICES):
        prev_s = SERVICES[i - 1]
        next_s = SERVICES[(i + 1) % len(SERVICES)]
        tg_label = s.get('tg_label', 'Оригинальный пост в Telegram')
        body = f'''
{page_head(s['title'], s['lead'], [('services.html', 'Чем могу помочь'), (None, f'{i + 1:02d}')], eyebrow=f'Услуга {i + 1:02d} из {len(SERVICES)}', bg=('assets/img/echr-desk.jpg', 'assets/img/echr-bench.jpg')[i % 2], r='../')}
<section class="section">
  <div class="wrap service-layout">
    <article class="article">
      {s['body'].replace('href="services/', 'href="../services/')}
      <p class="sign">Искренне ваш,<br>Особо разыскиваемый управляющий</p>
      <nav class="pager" aria-label="Другие услуги">
        <a href="{prev_s['slug']}.html"><small>← Предыдущая</small><span>{prev_s['title']}</span></a>
        <a href="{next_s['slug']}.html"><small>Следующая →</small><span>{next_s['title']}</span></a>
      </nav>
    </article>
    <aside class="aside">
      <div class="aside-card">
        <h3>Обсудить вашу ситуацию</h3>
        <p>Напишите в Telegram — коротко опишите, что происходит. Отвечу лично.</p>
        <a class="btn btn--gold" href="{TG_PERSONAL}" target="_blank" rel="noopener">{ICON_TG}@AllegatorSnap</a>
      </div>
      <div class="aside-card aside-card--light">
        <h3>Источник</h3>
        <p>Этот материал опубликован в Telegram — там же можно задать вопрос в комментариях.</p>
        <a class="btn btn--ghost" href="{s['tg']}" target="_blank" rel="noopener">{tg_label}</a>
      </div>
    </aside>
  </div>
</section>
'''
        page(path=f'services/{s["slug"]}.html', title=s['title'], active='services.html',
             description=s['short'], body=body)


def build_advice():
    items = ''.join(
        f'<li class="check"><span class="check__num">{i:02d}</span><p class="check__text">{t}</p>'
        f'<label class="check__box"><input type="checkbox" value="{i}" aria-label="Пункт {i} выполнен"><span>{ICON_CHECK}</span></label></li>'
        for i, t in enumerate(ADVICE, 1))
    body = f'''
{page_head('Как подготовиться к релокации в случае угрозы уголовного дела и задержания', 'Советы от особо разыскиваемого управляющего. Проверено на себе — в четырёх странах и двух розысках.', [(None, 'Советы')], eyebrow='Советы', bg='assets/img/echr-desk.jpg')}

<section class="section section--tight section--dark2">
  <div class="wrap wrap--narrow">
    <div class="player reveal">
      <video controls preload="metadata" playsinline>
        <source src="assets/video/sovety.mp4" type="video/mp4">
      </video>
      <a class="player__fallback" href="https://t.me/mostwantedmanager/141" target="_blank" rel="noopener">
        <span class="yt__play">{ICON_PLAY}</span>
        <strong>Советы от Особо разыскиваемого управляющего</strong>
        <span>Смотреть видео в Telegram-канале</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap wrap--narrow">
    <div class="checklist-tools">
      <div class="progress" aria-live="polite">
        <span>Сделано <b data-progress-count>0</b> из {len(ADVICE)}</span>
        <span class="progress__bar"><i data-progress-bar></i></span>
      </div>
      <div class="btn-row" style="margin:0">
        <button class="tool-btn" type="button" data-print>Распечатать</button>
        <button class="tool-btn" type="button" data-reset>Сбросить отметки</button>
      </div>
    </div>
    <ol class="checklist">{items}</ol>
    <p class="muted mt-l">Отметки сохраняются только в вашем браузере и никуда не отправляются.</p>
  </div>
</section>
'''
    page(path='advice.html', title='Советы: как подготовиться к релокации', active='advice.html',
         description='26 пунктов: как подготовиться к релокации при угрозе уголовного дела и задержания. Видео и чек-лист от особо разыскиваемого управляющего.',
         body=body)


# Новости хранятся на хостинге (их пишут через /admin/), поэтому news.php собирается
# как шаблон: шапка и подвал — общие, а список и сама новость — из PHP.
NEWS_PRELUDE = '''<?php
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
$metaDesc = $item ? news_excerpt($item, 160) : '%LIST_DESC%';
$canonical = '%DOMAIN%/news.php' . ($item ? '?id=' . $item['id'] : ($p > 1 ? '?page=' . $p : ''));
$ogImage = $cover ? ($cover[0] === '/' ? '%DOMAIN%' . $cover : $cover) : '%DOMAIN%/assets/img/echr-desk.jpg';
?>
'''


def build_news():
    list_desc = 'Новости Игоря Вышегородцева: выступления, интервью, публикации и события.'
    prelude = NEWS_PRELUDE.replace('%DOMAIN%', DOMAIN).replace('%LIST_DESC%', list_desc)
    date = "<?= h(news_date_ru($item['date'])) ?>"
    item_head = page_head("<?= h($item['title']) ?>", '', [('news.php', 'Новости'), (None, 'Новость')],
                          eyebrow=date, bg='assets/img/echr-desk.jpg', mod='page-head--news')
    list_head = page_head('Новости', 'Выступления, интервью, публикации и события. Обсуждение — в Telegram-канале.',
                          [(None, 'Новости')], eyebrow='Игорь Вышегородцев', bg='assets/img/hero-echr.jpg')
    missing_head = page_head('Новость не найдена', 'Возможно, её удалили или в адресе ошибка.',
                             [('news.php', 'Новости'), (None, 'Не найдено')], bg='assets/img/echr-bench.jpg')
    body = f'''
<?php if ($item): ?>
{item_head}
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
        <a class="btn btn--gold" href="{TG_PERSONAL}" target="_blank" rel="noopener">{ICON_TG}@AllegatorSnap</a>
      </div>
      <div class="aside-card aside-card--light">
        <h3>Telegram-канал</h3>
        <p>Новости выходят и в канале — там можно задать вопрос в комментариях.</p>
        <a class="btn btn--ghost" href="{TG_CHANNEL}" target="_blank" rel="noopener">@mostwantedmanager</a>
      </div>
    </aside>
  </div>
</section>
<?php elseif ($id): ?>
{missing_head}
<section class="section section--tight">
  <div class="wrap"><a class="btn btn--primary" href="news.php">Все новости</a></div>
</section>
<?php else: ?>
{list_head}
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
      <a class="btn btn--primary" href="{TG_CHANNEL}" target="_blank" rel="noopener">{ICON_TG}@mostwantedmanager</a>
    </div>
<?php endif; ?>
  </div>
</section>
<?php endif; ?>
'''
    page(path='news.php', title='<?= h($metaTitle) ?>', active='news.php',
         description='<?= h($metaDesc) ?>', body=body, prelude=prelude,
         canonical='<?= h($canonical) ?>', og_image_url='<?= h($ogImage) ?>')


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print('Сборка сайта в', ROOT)
    build_index()
    build_about()
    build_services()
    build_advice()
    build_news()
    sitemap = ''.join(f'  <url><loc>{u}</loc></url>\n' for u in PAGES)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sitemap + '</urlset>\n')
    print('   sitemap.xml')
    print('Готово.')
