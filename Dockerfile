FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .
COPY data/ ./data/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
