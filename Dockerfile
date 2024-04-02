FROM python:3.6

COPY requirements.txt /tmp

RUN pip install setuptools
RUN pip install -r /tmp/requirements.txt
RUN mkdir /app

COPY init_db.py /app
COPY main.py /app
COPY start_server.py /app

WORKDIR /app

EXPOSE 6000

CMD ["python3", "start_server.py"]
