FROM python:3.7.5

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

EXPOSE 8000

RUN pip install -r requirements.txt

RUN pip install channels
RUN pip install channels-redis

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
