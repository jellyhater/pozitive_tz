FROM python:3

ARG DB_PORT
ARG SERVER_PORT

ENV DB_PORT ${DB_PORT}
ENV SERVER_PORT ${SERVER_PORT}

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY model.py /app/model.py
COPY db.py /app/db.py
COPY config.py /app/config.py

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD python3 /app/app.py