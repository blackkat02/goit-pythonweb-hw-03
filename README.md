goit-pythonweb-hw-03


This project is a simple web server built with Python, demonstrating basic HTTP request handling, form data processing, and dynamic HTML rendering using Jinja2 templates.


Features

- HTTP Request Handling: Serves static HTML pages (index.html, message.html, error.html).
- Static File Serving: Correctly handles requests for static assets like CSS and images.
- Form Data Processing: Accepts POST requests from a form and saves the submitted data to a JSON file.
- Dynamic Content Generation: Uses the Jinja2 templating engine to dynamically render an HTML page (read.html) with data loaded from a JSON file.


Getting Started

Prerequisites
- Python 3.x
- uv (recommended) or pip
- Docker (optional, for containerized setup)


Installation

1. Clone this repository:

  git clone https://github.com/your-username/goit-pythonweb-hw-03.git
  cd goit-pythonweb-hw-03

2. Install the required Python packages using uv:

  uv pip install -r requirements.txt


Usage

Option 1: Using UV

1. Run the server from the project's root directory:

  uv run main.py

2. Open your web browser and navigate to http://localhost:3000.

Option 2: Using Docker

1. Build the Docker image:

  docker build -t goit-pythonweb-hw-03 .

2. Run the container:

  docker run -p 3000:3000 goit-pythonweb-hw-03

3. Open your web browser and navigate to http://localhost:3000.


Project Structure.

├── storage/
│   └── data.json              # Stores messages in JSON format
├── templates/
│   ├── index.html             # Main page HTML template
│   ├── message.html           # Form for submitting messages
│   ├── read.html              # Dynamically displays messages from data.json
│   └── error.html             # 404 error page
├── static/
│   ├── css/
│   │   └── style.css          # CSS file for styling
│   └── img/
│       └── logo.png           # Example image
├── main.py                    # The core Python web server script
└── requirements.txt           # List of project dependencies


Dependencies

- Jinja2: For HTML templating.

- Markupsafe: A dependency of Jinja2.

The server is built using Python's built-in http.server and urllib.parse modules, which do not require separate installation.