# mostwanted.consulting — сайт «Особо разыскиваемый управляющий»

Статический сайт Игоря Вышегородцева.

- `build.py` — все тексты и шаблоны. После правки: `python build.py` (нужен Pillow: `pip install pillow`)
- `seo_images.py` + `fonts/` — рисуют картинки-превью для мессенджеров и иконки сайта
- `site/` — готовый сайт (именно он попадает на хостинг)
- `.cpanel.yml` — автодеплой из cPanel → Git Version Control в `public_html`

## Локально
```
python serve.py
```
Открыть http://localhost:8080/ (понимает чистые адреса; новости — только на хостинге, там PHP).

## Обновить сайт на хостинге
1. `python build.py`
2. `git add -A && git commit -m "..." && git push`
3. Дальше всё само: GitHub Actions (`.github/workflows/deploy.yml`) заливает `site/` на хостинг по FTP.
   Статус — вкладка **Actions** в репозитории.

Настройка автозаливки (один раз): секреты `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
(и при необходимости `FTP_DIR`) в Settings → Secrets and variables → Actions.

Запасной путь без Actions: cPanel → Git Version Control → Manage → Pull or Deploy →
**Update from Remote** → **Deploy HEAD Commit** (использует `.cpanel.yml`).

## Новости и админка
- Раздел: https://mostwanted.consulting/news/, админка: https://mostwanted.consulting/admin/
- `site/news.php` собирается из `build.py` (шапка/подвал общие), список и новость выводит PHP.
- Код — `site/_news/lib.php` и `site/admin/`. Логин и хеш пароля — `site/_news/config.php`
  (репозиторий публичный, поэтому только хеш; пароль меняется в админке → `_news/data/auth.json`).
- Сами новости (`site/_news/data/`) и фото (`site/uploads/news/`) живут **только на хостинге**,
  в git их нет — деплой их не трогает. Бэкап: скачивать эти две папки через File Manager.

## SEO
- Адреса без `.html`: `/about`, `/services/`, `/services/red-notice`, `/news/12-zagolovok-novosti`.
  Правила — в `site/.htaccess`; старые адреса с `.html` и `news.php?id=` ведут на новые через 301.
- В ссылках внутри `build.py` можно писать как раньше (`about.html`) — сборка сама делает чистые адреса.
- Для каждой страницы при сборке рисуется превью 1200×630: `site/assets/img/og/`
  (заголовок и фото задаются параметром `og=` у `page()`). У новости превью — её первое фото.
- Разметка schema.org (Person, WebSite, Service, VideoObject, NewsArticle, хлебные крошки) — в `page()`
  и `news_jsonld()` в `site/_news/lib.php`.
- Карты сайта: `/sitemap.xml` (страницы) и `/news/sitemap.xml` (новости, обновляется сама).

## Видео советов
Положить файл как `site/assets/video/sovety.mp4` (до 100 МБ — ограничение GitHub; больше — загружать через File Manager).
