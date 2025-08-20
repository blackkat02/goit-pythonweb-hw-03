import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = BASE_DIR / 'templates'
STORAGE_DIR = BASE_DIR / 'storage'
DATA_FILE = STORAGE_DIR / 'data.json'


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)

        self.save_to_json(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file(TEMPLATES_DIR / 'index.html')
        elif pr_url.path == '/message':
            self.send_html_file(TEMPLATES_DIR /'message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file(TEMPLATES_DIR / 'error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        print(mt)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def save_to_json(self, data_to_save):
      """Додає дані до JSON-файлу, створюючи його, якщо він не існує."""
      STORAGE_DIR.mkdir(exist_ok=True)

      # Читаємо файл або створюємо порожній словник
      try:
          with open(DATA_FILE, 'r', encoding='utf-8') as f:
              existing_data = json.load(f)
      except (FileNotFoundError, json.JSONDecodeError):
          existing_data = {}

      # Додаємо новий запис з міткою часу
      existing_data[datetime.now().isoformat()] = data_to_save

      # Записуємо назад у файл
      with open(DATA_FILE, 'w', encoding='utf-8') as f:
          json.dump(existing_data, f, indent=4, ensure_ascii=False)



def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
