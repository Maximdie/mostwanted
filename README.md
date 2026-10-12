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

## Видео советов
Положить файл как `site/assets/video/sovety.mp4` (до 100 МБ — ограничение GitHub; больше — загружать через File Manager).
