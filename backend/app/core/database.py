from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings  

config = Settings.get_settings()
env = config.app.env  

DATABASE_URL = config.database.url
ssl_crt_file = config.database.ssl_cert_file
ssl_key_file = config.database.ssl_key_file

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
