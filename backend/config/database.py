from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.settings.base import GLOBAL_SETTINGS

# Create the SQLAlchemy engine
DATABASE_URL = GLOBAL_SETTINGS.get_database_url()

# Sets up the connection to PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# session factory used to create new session objects that interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    This function is a generator that provide database sessions
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
