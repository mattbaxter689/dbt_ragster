FROM python:3.11-slim

# Change working directory
WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

# Install dependencies
RUN pip install dagster-webserver dagster-postgres dagster-aws

# Copy source code
COPY docker/dagster.yaml  .
COPY workspace.yaml .
COPY dbt_ragster ./dbt_ragster


CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]