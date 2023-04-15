FROM python:3.11.3-slim-buster

# Install dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y wget gnupg lsb-release && \
    rm -rf /var/lib/apt/lists/*
    
# Install trivy
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && apt-get install trivy -y && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD ["python3", "Source/main.py"]
