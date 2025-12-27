# Use official Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install uv
RUN pip install uv

# Copy only requirements to cache them in docker layer
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy the rest of the application code
COPY . ./

# Install the project itself
RUN uv sync --frozen

# Collect static files
RUN uv run python manage.py collectstatic --noinput

# Run the web service on container startup.
# We use daphne for ASGI support (WebSockets)
CMD exec uv run daphne -b 0.0.0.0 -p $PORT config.asgi:application
