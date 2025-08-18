FROM python:3.13-slim

WORKDIR /app

# Встановлення curl для завантаження інсталятора uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Встановлення uv через офіційний скрипт
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Додавання uv у PATH (uv ставиться в ~/.cargo/bin)
ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

COPY . .

RUN mkdir -p storage

VOLUME ["/app/storage"]

EXPOSE 3000

# Запуск через uv (uv run сам підтягне залежності з pyproject.toml або requirements.txt)
CMD ["uv", "run", "main.py"]

