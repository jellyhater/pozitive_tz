import argparse

from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

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


def run_session(db_port):
    engine = create_engine(f'postgresql+psycopg2://postgres:postgres@database:{db_port}/postgres')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


def insert(db_session, event_id, client_ip=None, client_useragent=None, request_size=None, response_code=None,
           matched_variable_src=None, matched_variable_name=None, matched_variable_value=None, label_pred=None):

    with db_session() as session:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        default=5432,
                        type=int,
                        help='database port, 5432 by default')
    args = parser.parse_args()

    db_session = run_session(db_port=args.port)





