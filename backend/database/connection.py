import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Ranjithkumar%40123@localhost:3306/nightvision_guardian_db")

# To handle database creation if it doesn't exist, we first connect without the db name
# But for typical SQLAlchemy, we just create engine with the db name. We will handle creation separately.
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error connecting to DB: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
