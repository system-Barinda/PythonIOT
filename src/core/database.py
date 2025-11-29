"""
Database connection and operations
Uses PostgreSQL as specified in the guide
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from contextlib import asynccontextmanager

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    bio = Column(Text)
    photos = Column(JSON)
    interests = Column(JSON)
    location = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(String, ForeignKey('profiles.profile_id'), index=True)
    matched_profile_id = Column(String, ForeignKey('profiles.profile_id'), index=True)
    compatibility_score = Column(Integer)
    matched_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(String, ForeignKey('profiles.profile_id'), index=True)
    match_id = Column(Integer, ForeignKey('matches.id'), index=True)
    content = Column(Text)
    direction = Column(String)  # 'sent' or 'received'
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)


class Database:
    def __init__(self):
        # FIXED getenv() usage
        database_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:12345@localhost:5432/iot_db"
)

        # Auto-convert sync URL → async URL
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

        self.engine = create_async_engine(database_url, echo=False)
        self.SessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")

    async def disconnect(self):
        await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        async with self.SessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
