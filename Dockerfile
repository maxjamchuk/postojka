FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Указываем доп. индекс при установке torch
RUN pip install --no-cache-dir \
    -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
