FROM python:3.10.13-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

# Install ONLY required dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests==2.31.0 openai==1.30.1

# 🔥 IMPORTANT: run inference.py (not FastAPI)
CMD ["python", "inference.py"]
