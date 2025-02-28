from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./wifi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WifiSettings(Base):
    __tablename__ = "wifi_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    ssid = Column(String, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

# Initialize default settings if not exists
def init_db():
    db = SessionLocal()
    settings = db.query(WifiSettings).first()
    if not settings:
        default_settings = WifiSettings(ssid="DefaultSSID", password="DefaultPassword")
        db.add(default_settings)
        db.commit()
    db.close()

init_db()
