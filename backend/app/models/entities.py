from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(320),unique=True,index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(20),default="learner")
    is_active: Mapped[bool]=mapped_column(Boolean,default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))
    profile: Mapped["Profile"] = relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")

class Profile(Base):
    __tablename__="profiles"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),unique=True)
    display_name: Mapped[str]=mapped_column(String(100),default="Learner")
    known_language: Mapped[str]=mapped_column(String(10),default="en")
    target_language: Mapped[str]=mapped_column(String(10),default="ur")
    explanation_language: Mapped[str]=mapped_column(String(10),default="en")
    daily_goal_minutes: Mapped[int]=mapped_column(Integer,default=15)
    user: Mapped[User]=relationship(back_populates="profile")

class SavedWord(Base):
    __tablename__="saved_words"
    __table_args__=(UniqueConstraint("user_id","word","language_code",name="uq_saved_word_user_word_lang"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    word: Mapped[str]=mapped_column(String(200)); translation: Mapped[str]=mapped_column(String(300),default="")
    definition: Mapped[str]=mapped_column(Text,default=""); example: Mapped[str]=mapped_column(Text,default="")
    language_code: Mapped[str]=mapped_column(String(10),default="en")
    mastery: Mapped[int]=mapped_column(Integer,default=0); next_review_at: Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

class LearningProgress(Base):
    __tablename__="learning_progress"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    activity_type: Mapped[str]=mapped_column(String(40)); activity_id: Mapped[str]=mapped_column(String(100),default="")
    completed: Mapped[bool]=mapped_column(Boolean,default=False); score: Mapped[int|None]=mapped_column(Integer,nullable=True)
    minutes_spent: Mapped[int]=mapped_column(Integer,default=0); created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

class Conversation(Base):
    __tablename__="conversations"
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    title: Mapped[str]=mapped_column(String(200),default="AI Tutor chat"); created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))
class Message(Base):
    __tablename__="messages"
    id: Mapped[int]=mapped_column(primary_key=True); conversation_id: Mapped[int]=mapped_column(ForeignKey("conversations.id",ondelete="CASCADE"),index=True)
    role: Mapped[str]=mapped_column(String(20)); content: Mapped[str]=mapped_column(Text); created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))
class Course(Base):
    __tablename__="courses"
    id: Mapped[int]=mapped_column(primary_key=True); language_code: Mapped[str]=mapped_column(String(10)); title: Mapped[str]=mapped_column(String(200)); level: Mapped[str]=mapped_column(String(10)); description: Mapped[str]=mapped_column(Text,default="")
class Lesson(Base):
    __tablename__="lessons"
    id: Mapped[int]=mapped_column(primary_key=True); course_id: Mapped[int]=mapped_column(ForeignKey("courses.id",ondelete="CASCADE")); title: Mapped[str]=mapped_column(String(200)); content: Mapped[str]=mapped_column(Text,default=""); order_index: Mapped[int]=mapped_column(Integer,default=0)
class Achievement(Base):
    __tablename__="achievements"
    id: Mapped[int]=mapped_column(primary_key=True); user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE")); code: Mapped[str]=mapped_column(String(50)); title: Mapped[str]=mapped_column(String(100)); earned_at: Mapped[datetime]=mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))
