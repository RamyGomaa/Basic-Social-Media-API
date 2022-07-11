from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = settings.DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Gomaa1574*',connection_factory=RealDictConnection)
    cursor = conn.cursor()
    print("Connected Successfully!")
except Exception as error:
    print(error)
'''