import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = BASE_DIR / 'templates'
STORAGE_DIR = BASE_DIR / 'storage'
DATA_FILE = STORAGE_DIR / 'data.json'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        """
        Handles POST requests.
        Reads the request body, parses form data,
        saves it to JSON, and redirects to home page.
        """
        data: bytes = self.rfile.read(int(self.headers['Content-Length']))
        data_parse: str = urllib.parse.unquote_plus(data.decode())
        data_dict: Dict[str, str] = {
            key: value for key, value in [el.split('=') for el in data_parse.split('&')]
        }

        self.save_to_json(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self) -> None:
        """
        Handles GET requests.
        Serves HTML pages, renders templates with data,
        or serves static files depending on the requested path.
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file(TEMPLATES_DIR / 'index.html')
        elif pr_url.path == '/message':
            self.send_html_file(TEMPLATES_DIR / 'message.html')
        elif pr_url.path == '/read':
            self.render_html_with_data('read.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file(TEMPLATES_DIR / 'error.html', 404)

    def send_html_file(self, filename: Path, status: int = 200) -> None:
        """
        Sends a static HTML file to the client.

        :param filename: Path to the HTML file
        :param status: HTTP status code (default=200)
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def render_html_with_data(self, filename: str, status: int = 200) -> None:
        """
        Renders an HTML template using Jinja2 and sends it to the client.
        Loads messages from a JSON file.

        :param filename: Template file name inside the templates folder
        :param status: HTTP status code (default=200)
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Load data from JSON
        messages: Dict[str, Any] = {}
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    messages = {}

        # Render template with data
        template = jinja_env.get_template(filename)
        output = template.render(messages=messages)
        self.wfile.write(output.encode('utf-8'))

    def send_static(self) -> None:
        """
        Serves static files (e.g. CSS, JS, images).
        Determines MIME type automatically.
        """
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def save_to_json(self, data_to_save: Dict[str, Any]) -> None:
        """
        Adds a new record to the JSON file.
        Creates the storage directory and file if they don't exist.

        :param data_to_save: Dictionary with parsed form data
        """
        STORAGE_DIR.mkdir(exist_ok=True)

        # Read existing data or create empty dict
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        # Add new record with timestamp
        existing_data[datetime.now().isoformat()] = data_to_save

        # Write back to file
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)


def run(server_class=HTTPServer, handler_class=HttpHandler) -> None:
    """
    Runs the HTTP server on port 3000.
    Press Ctrl+C (KeyboardInterrupt) to stop.
    """
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
