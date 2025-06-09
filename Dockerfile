# =============================
# 🏗️ STAGE 1: builder
# =============================
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Установка зависимостей в отдельный путь
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --prefix=/install \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements.txt

# =============================
# 🏁 STAGE 2: runtime
# =============================
FROM python:3.10-slim AS runtime

WORKDIR /app

# Копируем только установленное из builder-образа
COPY --from=builder /install /usr/local
COPY app.py ./app.py
COPY config.py ./config.py
COPY load_posts.py ./load_posts.py
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
