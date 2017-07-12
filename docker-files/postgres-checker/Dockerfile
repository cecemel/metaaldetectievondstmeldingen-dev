FROM python:3.5

RUN apt-get update
RUN apt-get install -y postgresql-client
COPY requirements.txt /app/
WORKDIR "/app"
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "postgres_checker.py"]