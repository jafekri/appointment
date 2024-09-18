FROM python:3.11.2-bullseye

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV COLUMNS 80

RUN apt-get update \
 && apt-get install -y --force-yes

WORKDIR /code/

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .