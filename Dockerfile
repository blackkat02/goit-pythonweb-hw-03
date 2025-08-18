# Використання офіційного образу Python
FROM python:3.13-slim

# Встановлення curl для завантаження інсталятора uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Встановлення uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Додавання шляху uv до PATH
ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .

# Встановлення залежностей у системний Python
# RUN uv pip install --system -r requirements.txt

# Створюємо віртуальне середовище
RUN uv venv

# Активуємо середовище і встановлюємо залежності
RUN . .venv/bin/activate && uv pip install -r requirements.txt

RUN mkdir -p /app/storage

VOLUME /app/storage

COPY . .

EXPOSE 3000

CMD ["python", "main.py"]
