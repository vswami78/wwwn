from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship # Needed for relationships, though not explicitly defined in this step
from app.db import Base
from datetime import datetime

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True, nullable=False)
    text = Column(Text, nullable=False)
    label = Column(String, nullable=False)  # "working" or "not"
    ts = Column(DateTime, default=datetime.utcnow, nullable=False)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    ts = Column(DateTime, default=datetime.utcnow, nullable=False)

class EntryTopic(Base):
    __tablename__ = "entry_topics"
    entry_id = Column(Integer, ForeignKey("entries.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)
    __table_args__ = (PrimaryKeyConstraint('entry_id', 'topic_id'),)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    __table_args__ = (UniqueConstraint('user', 'topic_id', name='uq_user_topic'),)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=datetime.utcnow, nullable=False)
    owner = Column(String, nullable=True)
    steps = Column(Text, nullable=True)
