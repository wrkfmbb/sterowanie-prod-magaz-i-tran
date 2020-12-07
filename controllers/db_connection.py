from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    return create_engine('sqlite:///database/KLIENT_SERW.db')


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
