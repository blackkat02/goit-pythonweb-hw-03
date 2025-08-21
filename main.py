import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = BASE_DIR / 'templates'
STORAGE_DIR = BASE_DIR / 'storage'
DATA_FILE = STORAGE_DIR / 'data.json'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

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
            self.send_html_file(TEMPLATES_DIR / 'message.html')
        elif pr_url.path == '/read':
          print(222)
          # self.render_html_with_data(TEMPLATES_DIR / 'read.html')
          self.render_html_with_data(str(TEMPLATES_DIR / 'read.html'))
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

    def render_html_with_data(self, filename, status=200):
        """
        Відправляє HTML-файл клієнту, згенерований Jinja2 з даними.
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Завантажуємо дані з JSON
        messages = {}
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    messages = {}

        # Рендеримо шаблон з даними
        template = jinja_env.get_template(filename)
        print(filename)
        output = template.render(messages=messages)
        self.wfile.write(output.encode('utf-8'))

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



# import mimetypes
# import socket
# import urllib.parse
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import json
# from pathlib import Path
# from threading import Thread
# from datetime import datetime
# from jinja2 import Environment, FileSystemLoader

# # --- Constants ---
# # Визначаємо хост та порт сервера.
# HOST = '0.0.0.0'
# PORT = 3000

# # Визначаємо базову директорію проєкту та шляхи до файлів.
# # Path(__file__).parent.resolve() гарантує, що шлях завжди буде відносним до головного скрипту.
# BASE_DIR = Path(__file__).parent.resolve()
# STORAGE_DIR = BASE_DIR / 'storage'
# DATA_FILE = STORAGE_DIR / 'data.json'
# TEMPLATES_DIR = BASE_DIR / 'templates'

# # Налаштовуємо Jinja2
# jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


# # --- Handlers ---
# class HttpHandler(BaseHTTPRequestHandler):
#     """
#     Обробляє HTTP-запити для нашого веб-сервера.
#     """

#     def do_GET(self):
#         """
#         Обробляє GET-запити та надає файли відповідно до шляху запиту.
#         """
#         pr_url = urllib.parse.urlparse(self.path)

#         # Визначаємо шляхи до HTML-шаблонів
#         if pr_url.path == '/':
#             self.send_html_file('index.html')
#         elif pr_url.path == '/message':
#             self.send_html_file('message.html')
#         elif pr_url.path == '/read':
#             # Новий маршрут для читання даних з JSON та рендерингу
#             self.render_html_with_data('read.html')
#         elif pr_url.path == '/error':
#             self.send_html_file('error.html', status=404)

#         # Обробляємо статичні файли
#         elif pr_url.path.startswith('/static/'):
#             file_path = BASE_DIR / pr_url.path[1:]
#             if file_path.exists():
#                 self.send_static_file(file_path)
#             else:
#                 self.send_html_file('error.html', status=404)
#         else:
#             self.send_html_file('error.html', status=404)

#     def do_POST(self):
#         """
#         Обробляє POST-запити з форми.
#         """
#         data = self.rfile.read(int(self.headers['Content-Length']))
#         # Розбираємо URL-кодовані дані з тіла запиту.
#         data_parse = urllib.parse.unquote_plus(data.decode())

#         # Конвертуємо розібрані дані в словник.
#         data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

#         # Зберігаємо словник у JSON-файл.
#         self.save_to_json(data_dict)

#         # Відправляємо редирект на головну сторінку.
#         self.send_response(302)
#         self.send_header('Location', '/')
#         self.end_headers()

#     def send_html_file(self, filename, status=200):
#         """
#         Відправляє HTML-файл клієнту з вказаним статусом.
#         """
#         self.send_response(status)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()

#         # Шлях до файлу тепер будується з TEMPLATES_DIR
#         file_path = TEMPLATES_DIR / filename
#         with open(file_path, 'rb') as f:
#             self.wfile.write(f.read())

#     def render_html_with_data(self, filename, status=200):
#         """
#         Відправляє HTML-файл клієнту, згенерований Jinja2 з даними.
#         """
#         self.send_response(status)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()

#         # Завантажуємо дані з JSON
#         messages = {}
#         if DATA_FILE.exists():
#             with open(DATA_FILE, 'r', encoding='utf-8') as f:
#                 try:
#                     messages = json.load(f)
#                 except json.JSONDecodeError:
#                     messages = {}

#         # Рендеримо шаблон з даними
#         template = jinja_env.get_template(filename)
#         output = template.render(messages=messages)
#         self.wfile.write(output.encode('utf-8'))

#     def send_static_file(self, filename):
#         """
#         Відправляє статичний файл (наприклад, CSS, PNG) клієнту.
#         """
#         self.send_response(200)
#         # Визначаємо MIME-тип файлу.
#         mime_type, _ = mimetypes.guess_type(filename)
#         if mime_type:
#             self.send_header('Content-type', mime_type)
#         else:
#             self.send_header('Content-type', 'text/plain')
#         self.end_headers()
#         with open(filename, 'rb') as f:
#             self.wfile.write(f.read())

#     def save_to_json(self, data_to_save):
#         """
#         Додає нові дані до JSON-файлу, створюючи його, якщо він не існує.
#         """
#         # Переконуємось, що директорія для зберігання існує.
#         STORAGE_DIR.mkdir(exist_ok=True)

#         # Додаємо мітку часу до даних.
#         timestamp = datetime.now().isoformat()
#         formatted_data = {timestamp: data_to_save}

#         # Завантажуємо існуючі дані з файлу або створюємо порожній словник.
#         if DATA_FILE.exists():
#             with open(DATA_FILE, 'r', encoding='utf-8') as f:
#                 try:
#                     existing_data = json.load(f)
#                 except json.JSONDecodeError:
#                     # Обробляємо порожній або недійсний JSON-файл.
#                     existing_data = {}
#         else:
#             existing_data = {}

#         # Оновлюємо існуючі дані новим повідомленням.
#         existing_data.update(formatted_data)

#         # Записуємо оновлені дані назад до JSON-файлу.
#         with open(DATA_FILE, 'w', encoding='utf-8') as f:
#             json.dump(existing_data, f, indent=4, ensure_ascii=False)

# # --- Server Start ---
# def run_server(server_class=HTTPServer, handler_class=HttpHandler):
#     """
#     Запускає HTTP-сервер.
#     """
#     server_address = (HOST, PORT)
#     httpd = server_class(server_address, handler_class)
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     httpd.server_close()

# if __name__ == '__main__':
#     run_server()
