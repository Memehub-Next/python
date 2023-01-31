FROM python:3.10.5-buster
ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1 
ENV TERM=xterm 
RUN --mount=type=cache,target=/var/cache/apt \
	--mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -qq -y \
	apt-transport-https ca-certificates curl gnupg \
	build-essential libpq-dev sqlite3 libsqlite3-dev python3-setuptools tree \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /app/
USER root
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt