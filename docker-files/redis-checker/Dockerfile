FROM python:3.5

COPY requirements.txt /app/
WORKDIR "/app"
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "redis_checker.py"]