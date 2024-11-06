ARG PYTHON_VERSION=3.13.0
ARG DEBIAN_VERSION=bullseye

FROM python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION} AS base
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /project

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR $PROJECT_DIR/solutions
ADD . $PROJECT_DIR