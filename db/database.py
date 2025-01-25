from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Configuration
DATABASE_URL = "sqlite:///./chatbot.db"  # SQLite DB
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

# Functions
def init_db():
    Base.metadata.create_all(bind=engine)

def get_user_by_username(username):
    with SessionLocal() as session:
        return session.query(User).filter(User.username == username).first()

def create_user(username, password_hash):
    with SessionLocal() as session:
        new_user = User(username=username, password_hash=password_hash)
        session.add(new_user)
        session.commit()

def save_query(query, response):
    with SessionLocal() as session:
        new_query = Query(query=query, response=response)
        session.add(new_query)
        session.commit()
