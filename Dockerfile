# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set noninteractive installation to avoid stuck processes during build
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    cron

# Setup for running headless Chrome
RUN apt-get install -y \
xvfb \
libxi6 \
libgconf-2-4

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Give execution rights on the cron job
COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Make the startup script executable
COPY startup.sh startup.sh

# Set the environment variable for the display
ENV DISPLAY=:99

# Run the startup script
CMD ["/usr/src/app/startup.sh"]
