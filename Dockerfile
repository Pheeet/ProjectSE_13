# Build stage
FROM python:3.10-alpine3.17 AS build


# Set work directory
WORKDIR /flask_app


# Update system & install build dependencies
RUN apk update && apk --no-cache add git gcc libc-dev libffi-dev


# Install dependencies
COPY ./requirements.txt /flask_app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt




# Application image
FROM python:3.10-alpine3.17


# Set work directory
WORKDIR /flask_app


# Prevent Python from writing pyc files & buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/flask_app/bin:$PATH"


# Copy installed dependencies from the build stage
COPY --from=build \
   /usr/local/lib/python3.10/site-packages \
   /usr/local/lib/python3.10/site-packages


# Specify the entry point
ENTRYPOINT [ "./gunicorn_starter.sh" ]


# Keep the Docker process running even when crashes
CMD ["tail", "-f", "/dev/null"]
