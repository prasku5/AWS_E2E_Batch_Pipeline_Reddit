# we will use the official Apache Airflow image as the base image
# and install the required Python packages using the requirements.txt file.
# This image is coming from the official Apache Airflow DockerHub repository.
# Docker will pull the image from the DockerHub repository and install the required Python packages.
FROM apache/airflow:2.7.1-python3.9 

# Copy the requirements.txt file from the image pulled to the /opt/airflow/ directory
COPY requirements.txt /opt/airflow/
# Switch to the root user and install the required packages using apt-get
USER root
# Install the required packages using apt-get
RUN apt-get update && apt-get install -y gcc python3-dev
# Switch back to the airflow user
USER airflow
# Install the required Python packages using pip
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

