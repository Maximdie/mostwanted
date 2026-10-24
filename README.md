# mostwanted.consulting — сайт «Особо разыскиваемый управляющий»

Статический сайт Игоря Вышегородцева.

- `build.py` — все тексты и шаблоны. После правки: `python build.py`
- `site/` — готовый сайт (именно он попадает на хостинг)
- `.cpanel.yml` — автодеплой из cPanel → Git Version Control в `public_html`

## Локально
```
cd site
python -m http.server 8080
```
Открыть http://localhost:8080/

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
- Раздел: https://mostwanted.consulting/news.php, админка: https://mostwanted.consulting/admin/
- `site/news.php` собирается из `build.py` (шапка/подвал общие), список и новость выводит PHP.
- Код — `site/_news/lib.php` и `site/admin/`. Логин и хеш пароля — `site/_news/config.php`
  (репозиторий публичный, поэтому только хеш; пароль меняется в админке → `_news/data/auth.json`).
- Сами новости (`site/_news/data/`) и фото (`site/uploads/news/`) живут **только на хостинге**,
  в git их нет — деплой их не трогает. Бэкап: скачивать эти две папки через File Manager.

## Видео советов
Положить файл как `site/assets/video/sovety.mp4` (до 100 МБ — ограничение GitHub; больше — загружать через File Manager).
