FROM python:3.10-bookworm

# Install cron
RUN apt-get update && apt-get install -y cron

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Copy cron job
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Set correct permissions for cron file
RUN chmod 0644 /etc/cron.d/2fa-cron

# Apply cron job
RUN crontab /etc/cron.d/2fa-cron

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start cron + start app
CMD service cron start && python src/main.py