FROM python:3.8

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt

RUN python -m src.models

COPY . /code/

CMD python -m src.clock
