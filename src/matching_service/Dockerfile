# Base Image
FROM python:latest

# Working dir
WORKDIR /home/matching_service/

# Copy requirements.txt
COPY ./requirements.txt ./

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . /home/matching_service/
