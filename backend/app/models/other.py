# app/models/other.py

from sqlalchemy import Column, BigInteger, String, Date, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date, datetime

# Association table for media-post
media_post_association = Table(
    'Media_Post',
    Base.metadata,
    Column('Media_id', BigInteger, ForeignKey('Media.Media_id'), primary_key=True),
    Column('Post_id', BigInteger, ForeignKey('Posts.post_id'), primary_key=True)
)


class Media(Base):
    __tablename__ = "Media"

    Media_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Media_type = Column(String(50))
    Media_url = Column(Text)
    Uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    posts = relationship("Post", secondary=media_post_association, back_populates="media")

    def __repr__(self):
        return f"<Media {self.Media_type}>"


class Story(Base):
    __tablename__ = "Story"

    Story_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Expired_at = Column(DateTime)
    MediaType = Column(String(50))
    Created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    Media_Url = Column(Text)
    user_id = Column(BigInteger, ForeignKey("Users.User_id"), nullable=False)

    # Relationships
    author = relationship("User", back_populates="stories")

    def __repr__(self):
        return f"<Story {self.Story_id}>"


class Message(Base):
    __tablename__ = "Message"

    Message_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Message_content = Column(Text)
    Status = Column(String(50), default="sent")
    Message_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(BigInteger, ForeignKey("Users.User_id"), nullable=False)

    # Relationships
    sender = relationship("User", back_populates="messages_sent")

    def __repr__(self):
        return f"<Message {self.Message_id}>"


class Notification(Base):
    __tablename__ = "Notification"

    notification_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_Id = Column(BigInteger, ForeignKey("Users.User_id"), nullable=False)
    Is_Read = Column(String(5), default="False")
    Notification_date = Column(Date, nullable=False, default=date.today)
    Notification_Type = Column(String(255))
    Content = Column(Text)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.notification_id}>"


class Sentiment(Base):
    __tablename__ = "Sentiments"

    Sentiment_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    Sentiment_Score = Column(String(50))
    Sentiment_Label = Column(String(100))
    Target_Type = Column(String(50))
    comment_id = Column(BigInteger, ForeignKey("Comments.Comment_id"))
    Post_Id = Column(BigInteger, ForeignKey("Posts.post_id"))

    # Relationships
    comment = relationship("Comment", back_populates="sentiments")
    post = relationship("Post", back_populates="sentiments")

    def __repr__(self):
        return f"<Sentiment {self.Sentiment_Label}>"