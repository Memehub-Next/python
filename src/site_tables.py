from sqlalchemy import Column, DateTime, Float, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RedditMemes(Base):
    __tablename__ = 'reddit_memes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_1ae085193dc492081d372e0299c'),
        UniqueConstraint('url', name='UQ_80fc13a6facb2e40853bc5ce717')
    )

    id = Column(UUID, server_default=text('uuid_generate_v4()'))
    reddit_id = Column(String, nullable=False)
    subreddit = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    url = Column(String, nullable=False)
    upvote_ratio = Column(Float(53), nullable=False)
    upvotes = Column(Integer, nullable=False)
    downvotes = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)
    created_at = Column(DateTime(True), nullable=False, server_default=text('now()'))
    percentile = Column(Float(53))
