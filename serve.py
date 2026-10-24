# -*- coding: utf-8 -*-
"""
Локальный просмотр сайта с чистыми адресами (/about → about.html), как на хостинге.
    python serve.py      → http://localhost:8080/
Новости (/news/) работают только на хостинге или под PHP — здесь их нет.
"""
import http.server
import os

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE, **kwargs)

    def translate_path(self, path):
        real = super().translate_path(path)
        if not os.path.exists(real) and os.path.isfile(real + '.html'):
            return real + '.html'
        return real

    def send_error(self, code, message=None, explain=None):
        page = os.path.join(SITE, '404.html')
        if code == 404 and os.path.isfile(page):
            body = open(page, 'rb').read()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().send_error(code, message, explain)


if __name__ == '__main__':
    print('http://localhost:8080/')
    http.server.ThreadingHTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
