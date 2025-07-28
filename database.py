from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{user}:{password}@localhost:3306/{DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
