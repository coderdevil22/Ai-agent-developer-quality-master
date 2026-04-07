FROM python:3.10.13-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.27.1 \
    requests==2.31.0 \
    pydantic==2.6.4 \
    openai==1.30.1 \
    httpx==0.27.0

# 🔥 RUN SERVER + INFERENCE
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 7860 & sleep 5 && python inference.py"
