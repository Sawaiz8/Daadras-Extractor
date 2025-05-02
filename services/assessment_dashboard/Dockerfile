FROM python:3.10.14-slim

WORKDIR /app

# Install system dependencies that Chainlit might need
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

RUN chmod +x docker-entrypoint.sh

# Command to run the Scltreamlit app
CMD ["./docker-entrypoint.sh"]
