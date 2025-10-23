# Dockerfile for E-commerce Web Automation Testing with Selenium and Pytest
FROM selenium/standalone-chrome:latest

USER root

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "pytest", "tests/", "-v"]