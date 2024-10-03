from sqlalchemy import Column, String, JSON, Text, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(10000), nullable=False)
    languages = Column(JSON, nullable=False)
    status = Column(String(50), default="in progress")

    translations = Column(JSON, default={})