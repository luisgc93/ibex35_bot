FROM python:3.8

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt

COPY . /code/

CMD python clock.py
