# -*- coding: utf-8 -*-
"""
Картинки для ссылок в мессенджерах и соцсетях (Open Graph, 1200×630) и иконки сайта.
Вызывается из build.py. Нужен Pillow:  pip install pillow
Шрифты — те же, что на сайте: fonts/PlayfairDisplay.ttf и fonts/Inter.ttf (лицензия OFL).
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(HERE, 'fonts', 'PlayfairDisplay.ttf')
SANS = os.path.join(HERE, 'fonts', 'Inter.ttf')

INK = (13, 19, 32)
WHITE = (255, 253, 248)
GOLD = (180, 143, 85)
GOLD_LIGHT = (212, 181, 130)
MUTED = (169, 175, 187)
BURGUNDY = (125, 31, 44)

W, H = 1200, 630


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(weight)
    return f


def tracked(draw, xy, text, fnt, fill, spacing):
    """Текст с разрядкой (как text-transform: uppercase + letter-spacing на сайте)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing
    return x


def wrap(text, fnt, width):
    lines, line = [], ''
    for word in text.split():
        test = f'{line} {word}'.strip()
        if fnt.getlength(test) <= width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def mark(draw, cx, cy, r, ring=1.5):
    """Круглый знак «ИВ» — как в шапке сайта и в favicon.svg."""
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)
    k = r / 31
    draw.ellipse((cx - 27 * k, cy - 27 * k, cx + 27 * k, cy + 27 * k), outline=GOLD, width=max(1, round(ring * k)))
    f = font(SERIF, round(25 * k), b'Bold')
    draw.text((cx, cy + 1.5 * k), 'ИВ', font=f, fill=GOLD_LIGHT, anchor='mm')


def og_card(out, title, kicker, photo, focus=(0.5, 0.3)):
    img = Image.new('RGB', (W, H), INK)

    # фото справа, плавно уходящее в тёмный фон
    pw = 560
    ph = Image.open(photo).convert('RGB')
    ph = ImageOps.fit(ph, (pw, H), Image.LANCZOS, centering=focus)
    img.paste(ph, (W - pw, 0))
    # маска: 255 — тёмный фон, 0 — фото; на стыке плавный переход в 300px, фото чуть притушено
    fade = Image.new('L', (W, H), 255)
    fd = ImageDraw.Draw(fade)
    for x in range(W - pw, W):
        t = min(1, (x - (W - pw)) / 300)
        fd.line([(x, 0), (x, H)], fill=max(40, int(255 * (1 - t) ** 1.6)))
    img = Image.composite(Image.new('RGB', (W, H), INK), img, fade)

    d = ImageDraw.Draw(img)
    d.rectangle((22, 22, W - 23, H - 23), outline=(97, 81, 58), width=1)

    # шапка: знак + имя
    mark(d, 96, 98, 34)
    d.text((148, 72), 'Игорь Вышегородцев', font=font(SERIF, 30, b'SemiBold'), fill=WHITE)
    tracked(d, (149, 112), 'ОСОБО РАЗЫСКИВАЕМЫЙ УПРАВЛЯЮЩИЙ', font(SANS, 14, b'Medium'), MUTED, 2.2)

    # надзаголовок с золотой чертой
    y = 222
    if kicker:
        d.line([(64, y + 10), (104, y + 10)], fill=GOLD_LIGHT, width=2)
        tracked(d, (120, y), kicker.upper(), font(SANS, 17, b'SemiBold'), GOLD_LIGHT, 3)
        y += 52

    # заголовок: подбираем размер, чтобы влез в 4 строки
    for size in (66, 60, 54, 48, 44, 40, 36):
        f = font(SERIF, size, b'SemiBold')
        lines = wrap(title, f, 560)
        if len(lines) <= 4 and (y + len(lines) * size * 1.16) < 515:
            break
    for line in lines:
        d.text((62, y), line, font=f, fill=WHITE)
        y += round(size * 1.16)

    # низ: адрес сайта
    d.rectangle((64, 560, 100, 563), fill=BURGUNDY)
    d.text((114, 548), 'mostwanted.consulting', font=font(SANS, 21, b'Medium'), fill=MUTED)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, 'JPEG', quality=86, optimize=True, progressive=True)


def icons(outdir):
    """favicon.ico, PNG-иконки для Android/Google и apple-touch-icon."""
    os.makedirs(outdir, exist_ok=True)

    def round_icon(size):
        s = size * 4
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        mark(ImageDraw.Draw(im), s / 2, s / 2, s / 2 - 1, ring=1.5)
        return im.resize((size, size), Image.LANCZOS)

    def square_icon(size, scale):
        s = size * 4
        im = Image.new('RGB', (s, s), INK)
        mark(ImageDraw.Draw(im), s / 2, s / 2, s / 2 * scale, ring=1.5)
        return im.resize((size, size), Image.LANCZOS)

    big = round_icon(256)
    big.save(os.path.join(outdir, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    round_icon(96).save(os.path.join(outdir, 'favicon-96.png'), optimize=True)
    square_icon(180, 0.86).save(os.path.join(outdir, 'apple-touch-icon.png'), optimize=True)
    square_icon(192, 0.8).save(os.path.join(outdir, 'icon-192.png'), optimize=True)
    square_icon(512, 0.8).save(os.path.join(outdir, 'icon-512.png'), optimize=True)
