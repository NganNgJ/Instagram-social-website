FROM python:3.6.12

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]