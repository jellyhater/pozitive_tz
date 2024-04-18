import requests
import json
import csv
import pandas as pd
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        default=5432,
                        type=int,
                        help='database port, 5432 by default')
    parser.add_argument('--data_dir',
                        default='./',
                        type=str,
                        help='csv file directory, current by default')
    args = parser.parse_args()

    time.sleep(5)

    data_dir = Path(args.data_dir)
    engine = create_engine(f'postgresql+psycopg2://postgres:postgres@database:{args.port}/postgres')
    Session = sessionmaker(bind=engine)

    with Session() as session:
        for data_file in data_dir.glob("*.csv"):
            # init table name
            table_name = 'predictions_' + data_file.stem
            # open file, parse data and get predictions
            with open(str(data_file), 'r') as f:
                reader = csv.DictReader(f)
                data = [{"data": json.dumps(sample)} for sample in reader]
            resp = requests.post("http://app:8000/predict", json=data)
            json_data = resp.json()
            # write predictions to csv
            headers = json_data[0].keys()
            output_csv = f'{Path(data_dir, "output", table_name)}.csv'
            with open(output_csv, 'w', newline='\n') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(json_data)
            # create postgres table with predictions
            df = pd.read_csv(output_csv)
            df.to_sql(table_name, con=engine, if_exists='replace')
            # check whether data was inserted
            result = engine.execute(f"SELECT * FROM {table_name}").mappings().all()
            print(*df.columns)
            for r in result:
                print(*[r[column] for column in df.columns])
