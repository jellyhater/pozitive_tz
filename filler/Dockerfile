FROM python:3

ARG DATA_DIR
ARG DB_PORT 

ENV DATA_DIR ${DATA_DIR}
ENV DB_PORT ${DB_PORT}

WORKDIR /filler
COPY requirements.txt /filler/requirements.txt
COPY filler.py /filler/filler.py

RUN pip install --no-cache-dir -r /filler/requirements.txt

CMD python3 /filler/filler.py --port $DB_PORT --data_dir $DATA_DIR