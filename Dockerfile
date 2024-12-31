# Example minimal Dockerfile for a Python web app
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# If you have a requirements.txt, install it:
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on, e.g. 8080
EXPOSE 8080

# Start your server (like a Flask app)
CMD ["python", "server_example.py"]