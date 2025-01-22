FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install flask_restful flask flask_sqlalchemy

EXPOSE 5000

CMD ["python","app.py"]