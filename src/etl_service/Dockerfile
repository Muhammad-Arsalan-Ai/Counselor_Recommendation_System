# Base Image
FROM python:latest

# Working Dir
WORKDIR /home/etl_service/

# Copy files
COPY . /home/etl_service/

# Update package lists
RUN apt-get update

# Install OpenJDK 17 JDK
RUN apt-get install -y --no-install-recommends openjdk-17-jdk

# RUN apt-get install -y redis-server
RUN apt install -y redis-server

# RUN requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cronjob
RUN apt-get update && apt-get install -y cron

# Copy the cron job configuration file to the container
COPY cronjob /etc/cron.d/cronjob

# Create the log file
RUN touch /var/log/cron.log

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Apply the cron job
RUN crontab /etc/cron.d/cronjob

# Run cron and tail the log file
CMD cron && tail -f /var/log/cron.log
