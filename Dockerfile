FROM python:3.8

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
