FROM ubuntu:18.04

LABEL MAINTANER Your Name "hervekouamo@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python3 python3-pip python3-dev vim locales gunicorn3


RUN locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

ENV DB_HOST database
ENV DB_USER 237story
ENV DB_PASSWORD 237story
ENV DB_NAME 237story

# We copy just the requirements.txt first to leverage Docker cache
COPY ./src/requirements.txt /app/requirements.txt

WORKDIR /app


RUN pip3 install -r requirements.txt

COPY ./src /app

ENTRYPOINT [ "/usr/bin/gunicorn3"]

CMD [ "--bind", "0.0.0.0:8000", "run:app" ]
