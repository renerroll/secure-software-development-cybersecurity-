FROM python:3.10-slim

# non-root user for security
RUN useradd -m appuser || true
WORKDIR /app

# copy pinned deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# run as non-root
USER appuser

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
