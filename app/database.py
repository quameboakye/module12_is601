from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings

Base = declarative_base()


def get_engine():
    try:
        db_url = settings.DATABASE_URL

        connect_args = (
            {"check_same_thread": False}
            if db_url.startswith("sqlite")
            else {}
        )

        database_engine = create_engine(
            db_url,
            connect_args=connect_args
        )

        if database_engine.dialect.name == "sqlite":

            @event.listens_for(database_engine, "connect")
            def configure_sqlite(dbapi_connection, connection_record):
                # Let SQLAlchemy control transaction beginnings.
                dbapi_connection.isolation_level = None

                # Enable SQLite foreign-key enforcement.
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            @event.listens_for(database_engine, "begin")
            def begin_sqlite_transaction(connection):
                connection.exec_driver_sql("BEGIN")

        return database_engine

    except SQLAlchemyError as e:
        print(f"Error creating engine: {e}")
        raise


def get_sessionmaker(engine):
    return sessionmaker(
        autoflush=False,
        bind=engine
    )


engine = get_engine()
SessionLocal = get_sessionmaker(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
