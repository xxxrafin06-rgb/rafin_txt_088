FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Asia/Dhaka
ENV PORT=10000

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch token.txt
RUN if [ ! -f spam_targets.json ]; then echo "[]" > spam_targets.json; fi

EXPOSE 10000

CMD ["python", "-u", "main.py"]