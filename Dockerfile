FROM python:3.8

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r /tmp/requirements.txt

COPY . /code/

CMD python /code/clock.py
