FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MATHTRANS_DATA_DIR=/data
RUN apt-get update && apt-get install -y --no-install-recommends \
        libreoffice-writer fonts-wqy-zenhei fonts-dejavu-core libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e . && python scripts/fetch_fonts.py /app/fonts || true
VOLUME ["/data"]
EXPOSE 8000
CMD ["python", "-m", "mathtrans.cli", "serve", "--host", "0.0.0.0", "--port", "8000"]
