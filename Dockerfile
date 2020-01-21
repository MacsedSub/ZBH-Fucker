FROM python:alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .
RUN pip install requests

ENTRYPOINT [ "python" ,"-u", "fucker.py"  ]