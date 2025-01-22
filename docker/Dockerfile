FROM python:3.11-slim

# Change working directory
WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

# COPY and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY docker/dagster.yaml  .
COPY workspace.yaml .
COPY dbt_ragster ./dbt_ragster
COPY praw.ini .
COPY .env .


CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]