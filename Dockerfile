FROM python:3.8

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt

COPY ./src /code/

RUN python -m models.py

COPY . /code/

CMD python -m src.clock
