# `python-base` sets up all our shared environment variables
FROM python:3.11-slim as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        openssh-client \
        libffi-dev \
        git \
        libpcre3 libpcre3-dev

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
