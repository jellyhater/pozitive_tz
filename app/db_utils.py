import argparse

from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()


class Requests(Base):
    __tablename__ = 'requests'

    event_id = Column(String, primary_key=True)
    client_ip = Column(String)
    client_useragent = Column(String)
    request_size = Column(Integer)
    response_code = Column(Integer)
    matched_variable_src = Column(String)
    matched_variable_name = Column(String)
    matched_variable_value = Column(String)
    label_pred = Column(Integer)


class Database:

    def __init__(self, db_port, user="postgres", password="postgres"):
        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@database:{db_port}/postgres')
        self.session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def insert(self, event_id, client_ip=None, client_useragent=None, request_size=None, response_code=None,
               matched_variable_src=None, matched_variable_name=None, matched_variable_value=None, label_pred=None):
        with self.session() as session:
            try:
                session.add(
                    Requests(
                        event_id=event_id,
                        client_ip=client_ip,
                        client_useragent=client_useragent,
                        request_size=request_size,
                        response_code=response_code,
                        matched_variable_src=matched_variable_src,
                        matched_variable_name=matched_variable_name,
                        matched_variable_value=matched_variable_value,
                        label_pred=label_pred
                    )
                )
                session.commit()
            # skip if primary key duplicated
            except sqlalchemy.exc.IntegrityError:
                print(f"Event id {event_id} already exists; skip logging stage")

    def select(self):
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM requests;")).mappings().all()
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        default=5432,
                        type=int,
                        help='database port, 5432 by default')
    args = parser.parse_args()

    db = Database(db_port=args.port)





