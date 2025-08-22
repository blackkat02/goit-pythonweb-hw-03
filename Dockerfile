# Використовуємо офіційний образ Python
FROM python:3.13-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо curl та uv
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

COPY . .

RUN uv pip install --system -r requirements.txt \
    && mkdir -p storage

VOLUME ["/app/storage"]

EXPOSE 3000

CMD ["uv", "run", "main.py"]


