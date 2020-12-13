import sqlite3

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    return create_engine('sqlite:///D:/Inne/Materialy/Magisterskie/2_Semestr/SPMiT/P/database/KLIENT_SERW.db')


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
