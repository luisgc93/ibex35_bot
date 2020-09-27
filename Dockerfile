FROM python:3.8

COPY . /tmp
RUN pip install -r /tmp/requirements.txt
