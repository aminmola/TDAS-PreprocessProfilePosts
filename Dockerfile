FROM python:3.9-slim-buster

WORKDIR ../code

RUN apt-get update

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

CMD ["python","api/main.py"]