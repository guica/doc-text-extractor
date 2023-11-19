FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt update && apt install -y libreoffice
ADD requirements.txt /code/
RUN pip install -r requirements.txt && python -m spacy download pt_core_news_lg
ADD . /code/