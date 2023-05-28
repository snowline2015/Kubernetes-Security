FROM python:3.11.3-slim-buster

RUN apt-get update && apt-get install -y wget gnupg lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | tee /usr/share/keyrings/trivy.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && apt-get install -y trivy && trivy image --download-db-only && trivy image --download-java-db-only && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /Source /app

RUN pip3 install -r requirements.txt

EXPOSE 50000

CMD ["python3", "app.py"]
