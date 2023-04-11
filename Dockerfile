FROM python:3.11.3-slim-buster

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 50000 available to the world outside this container
EXPOSE 50000

# Run app.py when the container launches
CMD ["python3", "Source/main.py"]
