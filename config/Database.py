from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# from configs.Environment import get_environment_variables
from config.Config import Config

# Runtime Environment Configuration
user, password, host, database = Config().get_database_settings()
DEBUG_MODE = True

# Generate Database URL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@database:3306/{database}"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=DEBUG_MODE, future=True, pool_pre_ping=True, pool_size=32, max_overflow=64
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
