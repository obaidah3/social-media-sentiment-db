![SQL](https://img.shields.io/badge/SQL-347DB7?style=for-the-badge&logo=postgresql&logoColor=white)
![AI](https://img.shields.io/badge/AI-FF6F61?style=for-the-badge&logo=opencv&logoColor=white)
![API](https://img.shields.io/badge/API-4A90E2?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=java&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
# Social Media Database with Sentiment Analysis

A production-grade database system for managing social media platforms with integrated NLP-based sentiment analysis, real-time content moderation, and comprehensive analytics infrastructure.

## 👥 Team Members 

- **Ahmed Mohamed**  
- **Shahd Ibrahim**  
- **Monay Mohamed** 
- **Marc Wassim** 
- **Abdulrahman Essam** (ME)

[egypt japan university of science and technology](https://www.ejust.edu.eg/)  **Faculty:** CSIT  **Department:** AID (Artificial Intelligence & Data Science) 

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Database Design](#database-design)
- [Technology Stack](#technology-stack)
- [Backend Architecture](#backend-architecture)
- [Sentiment Analysis Engine](#sentiment-analysis-engine)
- [API Documentation](#api-documentation)
- [Database Queries](#database-queries)
- [Performance Optimization](#performance-optimization)
- [Security Implementation](#security-implementation)
- [Installation & Configuration](#installation--configuration)
- [Testing Strategy](#testing-strategy)
- [Monitoring & Analytics](#monitoring--analytics)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

Modern social media platforms generate massive amounts of user content every second, creating challenges in content moderation, behavior analysis, and toxic interaction detection. This project addresses these challenges through:

- **Structured Database Management**: Efficient storage and organization of users, posts, comments, and interactions
- **Sentiment Analysis Integration**: Automatic evaluation of emotional tone in user-generated content using NLP
- **Intelligent Moderation**: AI-powered detection of toxic content and harmful behavior
- **Data-Driven Insights**: Real-time analytics for tracking trends, engagement patterns, and community health
- **Scalable Architecture**: Designed to handle millions of users and billions of interactions

The system is designed with **scalability**, **performance**, and **data integrity** in mind, making it suitable for large-scale social networking environments.

---

## 🔍 Problem Statement

Social media platforms face critical challenges:

- **Manual Moderation Inefficiency**: Time-consuming review process, prone to human bias and fatigue
- **Volume Overload**: Millions of posts and comments generated daily requiring real-time analysis
- **Lack of Analytics**: Difficulty understanding user engagement patterns and community health metrics
- **Toxic Behavior Detection**: Complex task requiring automated NLP-based sentiment analysis
- **Trend Identification**: Missing tools for detecting emerging discussions and viral content
- **Data Consistency**: Maintaining integrity across millions of concurrent transactions
- **Performance Degradation**: Slow query response times as data volume grows

**Our Solution**: A robust, scalable database system with automated sentiment analysis that enables efficient content management, real-time moderation, and data-driven decision making.

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Web Browser  │  │ Mobile App   │  │ Admin Panel  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼──────────────────┼──────────────────┼──────────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │ HTTPS/REST
┌─────────────────────────────┴─────────────────────────────────────┐
│                      APPLICATION LAYER                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Application                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │   Auth API   │  │  Posts API   │  │ Analytics API │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │ Comments API │  │  Users API   │  │  Moderation   │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                     │
│  ┌───────────────────────────┴───────────────────────────────┐   │
│  │              Business Logic Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │   Schemas   │  │  Validators │  │  Middleware │       │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │   │
│  └────────────────────────────────────────────────────────────┘   │
└───────────────────────────┬────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────────┐
│                      PROCESSING LAYER                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ Sentiment Engine │  │  Queue Manager   │  │ Notification Svc │ │
│  │  (NLP Models)    │  │  (Background)    │  │  (WebSockets)    │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└───────────────────────────┬────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────────┐
│                      DATA LAYER                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   PostgreSQL Database                         │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │  │
│  │  │  Users   │ │  Posts   │ │ Comments │ │Reactions │        │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │  │
│  │  │Sentiments│ │Analytics │ │  Audit   │ │  Cache   │        │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Client Layer
- **Web Browser**: Responsive SPA built with HTML5, CSS3, JavaScript
- **Mobile App**: Cross-platform support (iOS/Android)
- **Admin Panel**: Dedicated moderation and analytics interface

#### 2. Application Layer (FastAPI)
- **RESTful API**: Versioned endpoints following REST principles
- **Request Validation**: Pydantic schemas for data validation
- **Authentication**: JWT-based stateless authentication
- **Rate Limiting**: Per-user/IP request throttling
- **CORS Handling**: Secure cross-origin resource sharing

#### 3. Processing Layer
- **Sentiment Engine**: Asynchronous NLP processing
- **Background Tasks**: Celery workers for heavy operations
- **Real-time Notifications**: WebSocket connections for live updates
- **Caching**: Redis for session management and frequently accessed data

#### 4. Data Layer
- **PostgreSQL**: Primary relational database
- **Connection Pooling**: Efficient database connection management
- **Read Replicas**: Load balancing for read-heavy operations
- **Backup Strategy**: Automated daily backups with point-in-time recovery

---

## 🗄️ Database Design

### ERD
![ERD](https://github.com/user-attachments/assets/de01165e-9a82-43cf-926b-cdfba4d23936)

### Mapping
![Mapping](https://github.com/user-attachments/assets/e1a5122b-c1e2-42fe-87d9-bc2c65c9710f)


### Conceptual Model

The database follows **Third Normal Form (3NF)** to eliminate redundancy while maintaining query performance through strategic denormalization where necessary.

### Entity-Relationship Overview

```
Users ──┬── Posts ──┬── Comments ──── Sentiments
        │           │
        │           ├── Post_Reactions
        │           │
        │           ├── Topic_Posts
        │           │
        │           └── Post_Hashtags
        │
        ├── Follow (self-referencing)
        │
        ├── Block (self-referencing)
        │
        ├── Notifications
        │
        └── User_Preferences
```

### Core Tables Schema

#### 1. Users Table
```sql
CREATE TABLE Users (
    User_id SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password_hash VARCHAR(255) NOT NULL,
    Bio TEXT,
    Profile_Picture_URL VARCHAR(255),
    Location VARCHAR(100),
    Date_Joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Last_Active TIMESTAMP,
    Is_Verified BOOLEAN DEFAULT FALSE,
    Is_Active BOOLEAN DEFAULT TRUE,
    Role VARCHAR(20) DEFAULT 'user',
    
    -- Indexes
    INDEX idx_username (Username),
    INDEX idx_email (Email),
    INDEX idx_active (Is_Active, Last_Active)
);
```

**Indexing Strategy**:
- B-Tree index on `Username` and `Email` for fast lookups during authentication
- Composite index on `Is_Active` and `Last_Active` for activity queries
- Partial index on verified users for faster filtering

#### 2. Posts Table
```sql
CREATE TABLE Posts (
    Post_id SERIAL PRIMARY KEY,
    User_id INTEGER NOT NULL REFERENCES Users(User_id) ON DELETE CASCADE,
    Content TEXT NOT NULL,
    Media_URL VARCHAR(255),
    Media_Type VARCHAR(20),
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_at TIMESTAMP,
    Visibility VARCHAR(20) DEFAULT 'public',
    Is_Deleted BOOLEAN DEFAULT FALSE,
    Like_Count INTEGER DEFAULT 0,
    Comment_Count INTEGER DEFAULT 0,
    Share_Count INTEGER DEFAULT 0,
    
    -- Indexes
    INDEX idx_user_posts (User_id, Created_at DESC),
    INDEX idx_created_at (Created_at DESC),
    INDEX idx_visibility (Visibility, Is_Deleted),
    
    -- Full-text search
    FULLTEXT INDEX idx_content_search (Content)
);
```

**Denormalization Decision**: 
- `Like_Count`, `Comment_Count`, `Share_Count` are denormalized counters
- Updated via database triggers on INSERT/DELETE operations
- Eliminates expensive COUNT() queries on large tables
- Trade-off: Slightly more complex write operations for significantly faster reads

#### 3. Comments Table
```sql
CREATE TABLE Comments (
    Comment_id SERIAL PRIMARY KEY,
    Post_id INTEGER NOT NULL REFERENCES Posts(Post_id) ON DELETE CASCADE,
    User_id INTEGER NOT NULL REFERENCES Users(User_id) ON DELETE CASCADE,
    Parent_Comment_id INTEGER REFERENCES Comments(Comment_id) ON DELETE CASCADE,
    Content TEXT NOT NULL,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_at TIMESTAMP,
    Is_Deleted BOOLEAN DEFAULT FALSE,
    Like_Count INTEGER DEFAULT 0,
    
    -- Indexes
    INDEX idx_post_comments (Post_id, Created_at DESC),
    INDEX idx_user_comments (User_id),
    INDEX idx_parent_comment (Parent_Comment_id),
    
    -- Nested set model support (future optimization)
    Lft INTEGER,
    Rgt INTEGER,
    INDEX idx_nested_set (Lft, Rgt)
);
```

**Nested Comments Optimization**:
- Uses self-referencing foreign key for comment threads
- Optional nested set model columns (`Lft`, `Rgt`) for efficient subtree queries
- Supports unlimited nesting depth

#### 4. Sentiments Table
```sql
CREATE TABLE Sentiments (
    Sentiment_id SERIAL PRIMARY KEY,
    Post_id INTEGER REFERENCES Posts(Post_id) ON DELETE CASCADE,
    Comment_id INTEGER REFERENCES Comments(Comment_id) ON DELETE CASCADE,
    Sentiment_Score DECIMAL(5,4),
    Sentiment_Label VARCHAR(20),
    Toxicity_Score DECIMAL(5,4),
    Is_Flagged BOOLEAN DEFAULT FALSE,
    Analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Model_Version VARCHAR(20),
    Confidence_Score DECIMAL(5,4),
    
    -- Indexes
    INDEX idx_flagged (Is_Flagged, Analyzed_at),
    INDEX idx_post_sentiment (Post_id),
    INDEX idx_comment_sentiment (Comment_id),
    
    -- Constraints
    CHECK (Sentiment_Score BETWEEN -1 AND 1),
    CHECK (Toxicity_Score BETWEEN 0 AND 1),
    CHECK (Confidence_Score BETWEEN 0 AND 1),
    CHECK ((Post_id IS NOT NULL AND Comment_id IS NULL) OR 
           (Post_id IS NULL AND Comment_id IS NOT NULL))
);
```

**Sentiment Analysis Schema Design**:
- Stores analysis results for both posts and comments
- `CHECK` constraint ensures exactly one foreign key is set
- Tracks model version for A/B testing and rollback capability
- Confidence scores enable threshold-based filtering

#### 5. Engagement_Metrics Table (Time-Series Data)
```sql
CREATE TABLE Engagement_Metrics (
    Metric_id SERIAL PRIMARY KEY,
    Post_id INTEGER REFERENCES Posts(Post_id) ON DELETE CASCADE,
    User_id INTEGER REFERENCES Users(User_id) ON DELETE CASCADE,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Like_Count INTEGER DEFAULT 0,
    Comment_Count INTEGER DEFAULT 0,
    Share_Count INTEGER DEFAULT 0,
    View_Count INTEGER DEFAULT 0,
    Engagement_Rate DECIMAL(5,4),
    
    -- Partitioning key
    Date_partition DATE GENERATED ALWAYS AS (DATE(Timestamp)) STORED,
    
    -- Indexes
    INDEX idx_post_metrics (Post_id, Timestamp DESC),
    INDEX idx_user_metrics (User_id, Timestamp DESC),
    INDEX idx_timestamp (Timestamp)
) PARTITION BY RANGE (Date_partition);

-- Create monthly partitions
CREATE TABLE Engagement_Metrics_2024_01 PARTITION OF Engagement_Metrics
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**Time-Series Optimization**:
- Table partitioning by date for efficient querying of recent data
- Automatic partition management via scheduled jobs
- Older partitions can be archived to cold storage
- Significant performance improvement for analytics queries

#### 6. Follow Relationship Table
```sql
CREATE TABLE Follow (
    Follow_id SERIAL PRIMARY KEY,
    Follower_id INTEGER NOT NULL REFERENCES Users(User_id) ON DELETE CASCADE,
    Following_id INTEGER NOT NULL REFERENCES Users(User_id) ON DELETE CASCADE,
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE (Follower_id, Following_id),
    CHECK (Follower_id != Following_id),
    
    -- Indexes
    INDEX idx_follower (Follower_id),
    INDEX idx_following (Following_id),
    INDEX idx_both (Follower_id, Following_id)
);
```

**Relationship Integrity**:
- Unique constraint prevents duplicate follows
- Check constraint prevents self-following
- Bidirectional indexes support both "followers" and "following" queries

### Database Triggers

#### Auto-update Comment Count
```sql
CREATE OR REPLACE FUNCTION update_post_comment_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE Posts 
        SET Comment_Count = Comment_Count + 1 
        WHERE Post_id = NEW.Post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE Posts 
        SET Comment_Count = Comment_Count - 1 
        WHERE Post_id = OLD.Post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_comment_count
AFTER INSERT OR DELETE ON Comments
FOR EACH ROW EXECUTE FUNCTION update_post_comment_count();
```

#### Automatic Sentiment Analysis Trigger
```sql
CREATE OR REPLACE FUNCTION trigger_sentiment_analysis()
RETURNS TRIGGER AS $$
BEGIN
    -- Queue post for sentiment analysis
    INSERT INTO Analysis_Queue (Post_id, Content, Created_at)
    VALUES (NEW.Post_id, NEW.Content, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_analyze_new_post
AFTER INSERT ON Posts
FOR EACH ROW EXECUTE FUNCTION trigger_sentiment_analysis();
```

### Database Views

#### User Activity Summary
```sql
CREATE VIEW user_activity_summary AS
SELECT 
    u.User_id,
    u.Username,
    COUNT(DISTINCT p.Post_id) AS Total_Posts,
    COUNT(DISTINCT c.Comment_id) AS Total_Comments,
    COALESCE(SUM(p.Like_Count), 0) AS Total_Likes_Received,
    COUNT(DISTINCT f.Follow_id) AS Follower_Count,
    u.Last_Active
FROM Users u
LEFT JOIN Posts p ON u.User_id = p.User_id AND p.Is_Deleted = FALSE
LEFT JOIN Comments c ON u.User_id = c.User_id AND c.Is_Deleted = FALSE
LEFT JOIN Follow f ON u.User_id = f.Following_id
GROUP BY u.User_id, u.Username, u.Last_Active;
```

#### Trending Content View
```sql
CREATE VIEW trending_posts AS
SELECT 
    p.Post_id,
    p.Content,
    p.User_id,
    u.Username,
    p.Like_Count,
    p.Comment_Count,
    p.Share_Count,
    (p.Like_Count * 1.0 + p.Comment_Count * 2.0 + p.Share_Count * 3.0) AS Engagement_Score,
    EXTRACT(EPOCH FROM (NOW() - p.Created_at))/3600 AS Hours_Old,
    s.Sentiment_Label,
    s.Toxicity_Score
FROM Posts p
JOIN Users u ON p.User_id = u.User_id
LEFT JOIN Sentiments s ON p.Post_id = s.Post_id
WHERE p.Is_Deleted = FALSE 
  AND p.Created_at > NOW() - INTERVAL '24 hours'
  AND (s.Is_Flagged = FALSE OR s.Is_Flagged IS NULL)
ORDER BY Engagement_Score DESC;
```

---

## 💻 Technology Stack

### Backend Framework
```
FastAPI 0.104.1
├── Starlette (ASGI framework)
├── Pydantic (Data validation)
├── Uvicorn (ASGI server)
└── Python 3.11+
```

**Why FastAPI?**
- **Performance**: Comparable to Node.js and Go
- **Async Support**: Native async/await for concurrent operations
- **Auto Documentation**: Automatic OpenAPI/Swagger generation
- **Type Safety**: Python type hints with runtime validation
- **Dependency Injection**: Clean architecture support

### Database Stack
```
PostgreSQL 15.3
├── pg_trgm (Fuzzy text search)
├── pg_stat_statements (Query analysis)
├── TimescaleDB (Time-series optimization)
└── pgAdmin 4 (Administration)
```

**PostgreSQL Extensions Used**:
- **pg_trgm**: Trigram-based similarity search for usernames/hashtags
- **pg_stat_statements**: Query performance monitoring
- **TimescaleDB**: Optimized storage for engagement metrics
- **pgcrypto**: Secure password hashing

### NLP & Machine Learning
```
Sentiment Analysis Stack
├── Transformers 4.35.0 (Hugging Face)
├── BERT-base-uncased (Pre-trained model)
├── Toxic-BERT (Toxicity detection)
├── NLTK 3.8.1 (Text preprocessing)
└── spaCy 3.7.0 (Entity recognition)
```

**Model Architecture**:
- **Primary Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Toxicity Model**: `unitary/toxic-bert`
- **Languages Supported**: English (expandable)
- **Inference Time**: ~50ms per text (GPU), ~200ms (CPU)

### Caching & Queue Management
```
Redis 7.2
├── Session Storage
├── Rate Limiting
├── Leaderboard Cache
└── Real-time Counters

Celery 5.3.4
├── Background Tasks
├── Scheduled Jobs
└── Sentiment Analysis Queue
```

### Security Stack
```
Security Components
├── python-jose (JWT)
├── passlib (Password hashing)
├── bcrypt (Hash algorithm)
├── python-multipart (File uploads)
└── OWASP best practices
```

### Development Tools
```
Development Stack
├── SQLAlchemy 2.0 (ORM)
├── Alembic (Migrations)
├── Pytest (Testing)
├── Black (Code formatting)
├── Flake8 (Linting)
├── mypy (Type checking)
└── pre-commit (Git hooks)
```

---

## 🔧 Backend Architecture

### Project Structure
```
social-media-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connection
│   │
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── users.py          # User management
│   │   │   ├── posts.py          # Post CRUD operations
│   │   │   ├── comments.py       # Comment operations
│   │   │   ├── reactions.py      # Reaction handling
│   │   │   ├── analytics.py      # Analytics endpoints
│   │   │   └── moderation.py     # Moderation tools
│   │   └── dependencies.py       # Shared dependencies
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── sentiment.py
│   │   └── engagement.py
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── response.py
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── post_service.py
│   │   ├── sentiment_service.py
│   │   ├── notification_service.py
│   │   └── analytics_service.py
│   │
│   ├── core/                     # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py          # JWT, hashing
│   │   ├── config.py            # Settings
│   │   └── logging.py           # Logging setup
│   │
│   ├── ml/                       # Machine learning
│   │   ├── __init__.py
│   │   ├── sentiment_model.py
│   │   ├── toxicity_detector.py
│   │   └── model_loader.py
│   │
│   ├── utils/                    # Helper functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── constants.py
│   │
│   └── middleware/               # Custom middleware
│       ├── __init__.py
│       ├── rate_limit.py
│       ├── cors.py
│       └── error_handler.py
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_sentiment.py
│   └── test_analytics.py
│
├── alembic/                      # Database migrations
│   ├── versions/
│   └── env.py
│
├── scripts/                      # Utility scripts
│   ├── seed_data.py
│   ├── backup_db.py
│   └── analyze_performance.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
├── alembic.ini
└── README.md
```

### Core Configuration (config.py)
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Social Media API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    DB_POOL_TIMEOUT: int = 30
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600
    
    # Sentiment Analysis
    SENTIMENT_MODEL_PATH: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    TOXICITY_MODEL_PATH: str = "unitary/toxic-bert"
    TOXICITY_THRESHOLD: float = 0.75
    USE_GPU: bool = False
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".mp4"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
```

### Database Connection (database.py)
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Authentication Service (auth_service.py)
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None
```

---

## 🤖 Sentiment Analysis Engine

### Architecture Overview

```
Input Text
    │
    ├──> Text Preprocessing
    │       ├── Lowercasing
    │       ├── URL removal
    │       ├── Mention normalization
    │       ├── Emoji handling
    │       └── Special character cleanup
    │
    ├──> Tokenization (BERT Tokenizer)
    │       └── Subword tokenization
    │
    ├──> Model Inference
    │       ├── Sentiment Classification
    │       │   └── [Positive, Neutral, Negative, scores]
    │       │
    │       └── Toxicity Detection
    │           └── [Toxic, Severe-Toxic, Obscene, etc.]
    │
    └──> Post-Processing
            ├── Score normalization
            ├── Confidence calculation
            ├── Label assignment
            └── Flagging decision
```

### Sentiment Analysis Implementation

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Tuple
import re
import emoji
from datetime import datetime
from app.core.config import get_settings

settings = get_settings()

class SentimentAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu")
        
        # Load sentiment model
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(
            settings.SENTIMENT_MODEL_PATH
        )
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            settings.SENTIMENT_MODEL_PATH
        ).to(self.device)
        
        # Load toxicity model
        self.toxicity_tokenizer = AutoTokenizer.from_pretrained(
            settings.TOXICITY_MODEL_PATH
        )
        self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(
            settings.TOXICITY_MODEL_PATH
        ).to(self.device)
        
        self.sentiment_labels = ["negative", "neutral", "positive"]
        self.toxicity_labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Convert emojis to text
        text = emoji.demojize(text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '[URL]', text)
        
        # Normalize mentions
        text = re.sub(r'@\w+', '[USER]', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text"""
        preprocessed = self.preprocess_text(text)
        
        inputs = self.sentiment_tokenizer(
            preprocessed,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.sentiment_model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        scores = probabilities[0].cpu().numpy()
        
        # Calculate weighted sentiment score (-1 to 1)
        sentiment_score = (scores[0] * -1.0) + (scores[1] * 0.0) + (scores[2] * 1.0)
        
        return {
            "sentiment_score": float(sentiment_score),
            "sentiment_label": self.sentiment_labels[scores.argmax()],
            "confidence": float(scores.max()),
            "negative_prob": float(scores[0]),
            "neutral_prob": float(scores[1]),
            "positive_prob": float(scores[2])
        }
    
    def detect_toxicity(self, text: str) -> Dict[str, float]:
        """Detect toxic content"""
        preprocessed = self.preprocess_text(text)
        
        inputs = self.toxicity_tokenizer(
            preprocessed,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.toxicity_model(**inputs)
            probabilities = torch.sigmoid(outputs.logits)
        
        scores = probabilities[0].cpu().numpy()
        
        # Calculate overall toxicity score
        toxicity_score = float(scores.max())
        is_toxic = toxicity_score >= settings.TOXICITY_THRESHOLD
        
        return {
            "toxicity_score": toxicity_score,
            "is_flagged": is_toxic,
            "toxic_categories": {
                label: float(score) 
                for label, score in zip(self.toxicity_labels, scores)
                if score >= 0.5
            }
        }
    
    def analyze_complete(self, text: str) -> Dict:
        """Complete analysis combining sentiment and toxicity"""
        sentiment_result = self.analyze_sentiment(text)
        toxicity_result = self.detect_toxicity(text)
        
        return {
            **sentiment_result,
            **toxicity_result,
            "analyzed_at": datetime.utcnow().isoformat(),
            "model_version": "v1.0"
        }

# Singleton instance
sentiment_analyzer = SentimentAnalyzer()
```

### Asynchronous Sentiment Processing

```python
from celery import Celery
from app.database import SessionLocal
from app.models.sentiment import Sentiment
from app.ml.sentiment_model import sentiment_analyzer

celery_app = Celery('sentiment_tasks', broker=settings.REDIS_URL)

@celery_app.task
def analyze_post_sentiment(post_id: int, content: str):
    """Background task for sentiment analysis"""
    try:
        # Perform analysis
        result = sentiment_analyzer.analyze_complete(content)
        
        # Store in database
        db = SessionLocal()
        sentiment = Sentiment(
            Post_id=post_id,
            Sentiment_Score=result['sentiment_score'],
            Sentiment_Label=result['sentiment_label'],
            Toxicity_Score=result['toxicity_score'],
            Is_Flagged=result['is_flagged'],
            Confidence_Score=result['confidence'],
            Model_Version=result['model_version']
        )
        db.add(sentiment)
        db.commit()
        
        # If flagged, notify moderators
        if result['is_flagged']:
            notify_moderators.delay(post_id, result['toxicity_score'])
        
        db.close()
        return {"status": "success", "post_id": post_id}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.task
def notify_moderators(post_id: int, toxicity_score: float):
    """Send notification to moderators about flagged content"""
    # Implementation for moderator notification
    pass
```

---

## 📡 API Documentation

### Complete API Reference

#### Authentication Endpoints

**1. Register New User**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "bio": "Software developer",
  "location": "New York"
}

Response: 201 Created
{
  "user_id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**2. Login**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**3. Refresh Token**
```http
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Post Management Endpoints

**1. Create Post**
```http
POST /api/v1/posts
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "content": "Just launched my new app! #coding #developer",
  "media": [file],
  "visibility": "public",
  "tags": ["@user123"]
}

Response: 201 Created
{
  "post_id": 456,
  "user_id": 123,
  "content": "Just launched my new app! #coding #developer",
  "media_url": "https://cdn.example.com/posts/456.jpg",
  "created_at": "2024-01-18T10:30:00Z",
  "sentiment": {
    "score": 0.85,
    "label": "positive",
    "confidence": 0.92
  },
  "engagement": {
    "likes": 0,
    "comments": 0,
    "shares": 0
  }
}
```

**2. Get Feed**
```http
GET /api/v1/posts/feed?page=1&limit=20&sort=recent
Authorization: Bearer {access_token}

Response: 200 OK
{
  "posts": [
    {
      "post_id": 456,
      "user": {
        "user_id": 123,
        "username": "john_doe",
        "profile_picture": "https://cdn.example.com/profiles/123.jpg"
      },
      "content": "Just launched my new app!",
      "created_at": "2024-01-18T10:30:00Z",
      "engagement": {
        "likes": 42,
        "comments": 5,
        "shares": 3
      },
      "user_reaction": "like",
      "sentiment_label": "positive"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_posts": 150,
    "total_pages": 8,
    "has_next": true
  }
}
```

**3. Update Post**
```http
PUT /api/v1/posts/456
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "content": "Updated: Just launched my new app! Check it out!",
  "visibility": "public"
}

Response: 200 OK
{
  "post_id": 456,
  "content": "Updated: Just launched my new app! Check it out!",
  "updated_at": "2024-01-18T11:00:00Z"
}
```

**4. Delete Post**
```http
DELETE /api/v1/posts/456
Authorization: Bearer {access_token}

Response: 204 No Content
```

#### Comment Endpoints

**1. Add Comment**
```http
POST /api/v1/comments
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "post_id": 456,
  "content": "Great work! Congratulations! 🎉",
  "parent_comment_id": null
}

Response: 201 Created
{
  "comment_id": 789,
  "post_id": 456,
  "user_id": 124,
  "content": "Great work! Congratulations! 🎉",
  "created_at": "2024-01-18T10:45:00Z",
  "sentiment": {
    "score": 0.92,
    "label": "positive"
  }
}
```

**2. Get Comments**
```http
GET /api/v1/posts/456/comments?sort=recent&limit=50
Authorization: Bearer {access_token}

Response: 200 OK
{
  "comments": [
    {
      "comment_id": 789,
      "user": {
        "user_id": 124,
        "username": "jane_smith",
        "profile_picture": "https://cdn.example.com/profiles/124.jpg"
      },
      "content": "Great work! Congratulations! 🎉",
      "created_at": "2024-01-18T10:45:00Z",
      "likes": 5,
      "replies_count": 2,
      "replies": [
        {
          "comment_id": 790,
          "user": {...},
          "content": "Thank you!",
          "created_at": "2024-01-18T10:50:00Z"
        }
      ]
    }
  ],
  "total_comments": 5
}
```

#### Analytics Endpoints

**1. Get Engagement Metrics**
```http
GET /api/v1/analytics/engagement?post_id=456&period=7d
Authorization: Bearer {access_token}

Response: 200 OK
{
  "post_id": 456,
  "period": "7 days",
  "metrics": {
    "total_views": 1523,
    "total_likes": 89,
    "total_comments": 23,
    "total_shares": 12,
    "engagement_rate": 8.14,
    "reach": 3421
  },
  "timeline": [
    {
      "date": "2024-01-18",
      "views": 234,
      "likes": 15,
      "comments": 4,
      "shares": 2
    }
  ]
}
```

**2. Get Sentiment Analytics**
```http
GET /api/v1/analytics/sentiment?user_id=123&period=30d
Authorization: Bearer {access_token}

Response: 200 OK
{
  "user_id": 123,
  "period": "30 days",
  "sentiment_distribution": {
    "positive": 65.5,
    "neutral": 28.3,
    "negative": 6.2
  },
  "average_sentiment_score": 0.62,
  "toxicity_stats": {
    "flagged_posts": 2,
    "toxicity_rate": 1.5,
    "average_toxicity": 0.12
  },
  "trend": "improving"
}
```

**3. Get Trending Topics**
```http
GET /api/v1/analytics/trends?period=24h&limit=10
Authorization: Bearer {access_token}

Response: 200 OK
{
  "trending_hashtags": [
    {
      "hashtag": "#coding",
      "count": 1523,
      "growth_rate": 145.3,
      "sentiment": "positive"
    },
    {
      "hashtag": "#ai",
      "count": 987,
      "growth_rate": 98.7,
      "sentiment": "neutral"
    }
  ],
  "trending_posts": [
    {
      "post_id": 456,
      "engagement_score": 234.5,
      "viral_coefficient": 2.3
    }
  ]
}
```

#### Moderation Endpoints

**1. Get Flagged Content**
```http
GET /api/v1/moderation/flagged?status=pending&limit=50
Authorization: Bearer {moderator_token}

Response: 200 OK
{
  "flagged_content": [
    {
      "content_id": 789,
      "content_type": "post",
      "user_id": 125,
      "content": "...",
      "toxicity_score": 0.89,
      "flagged_at": "2024-01-18T09:00:00Z",
      "status": "pending",
      "toxic_categories": ["insult", "toxic"]
    }
  ],
  "total_pending": 12
}
```

**2. Review Flagged Content**
```http
POST /api/v1/moderation/review/789
Authorization: Bearer {moderator_token}
Content-Type: application/json

{
  "action": "remove",
  "reason": "Violation of community guidelines - hate speech",
  "notify_user": true
}

Response: 200 OK
{
  "content_id": 789,
  "action_taken": "removed",
  "reviewed_by": "moderator_jane",
  "reviewed_at": "2024-01-18T11:30:00Z"
}
```

---

## 📊 Database Queries & Optimization

### Complex Query Examples

**1. Summary of All Posts and Their Engagement Metrics**
```sql
SELECT 
    p.post_id,
    p.content,
    u.username,
    COUNT(DISTINCT c.Comment_id) AS total_comments,
    COUNT(DISTINCT pr.Reaction_id) AS total_reactions,
    COALESCE(SUM(em.Like_Count), 0) AS total_likes,
    COALESCE(AVG(s.Sentiment_Score), 0) AS avg_sentiment,
    CASE 
        WHEN MAX(s.Is_Flagged) = TRUE THEN 'flagged'
        ELSE 'normal'
    END AS moderation_status
FROM Posts p
JOIN Users u ON p.User_id = u.User_id
LEFT JOIN Comments c ON p.post_id = c.Post_id AND c.Is_Deleted = FALSE
LEFT JOIN Post_Reaction pr ON p.post_id = pr.Post_id
LEFT JOIN Engagement_Metrics em ON p.post_id = em.Post_ID
LEFT JOIN Sentiments s ON p.post_id = s.Post_id
WHERE p.Is_Deleted = FALSE
GROUP BY p.post_id, p.content, u.username
ORDER BY total_reactions DESC;
```

**Performance**: Uses covering indexes on foreign keys, executes in ~50ms for 10K posts

**2. Top Commenters with Sentiment Analysis**
```sql
WITH CommenterStats AS (
    SELECT 
        U.User_id,
        U.Username,
        COUNT(C.Comment_id) AS comments_made,
        AVG(S.Sentiment_Score) AS avg_sentiment,
        SUM(CASE WHEN S.Is_Flagged THEN 1 ELSE 0 END) AS toxic_comments
    FROM Users U
    JOIN Comments C ON U.User_id = C.user_id
    LEFT JOIN Sentiments S ON C.Comment_id = S.Comment_id
    WHERE C.Is_Deleted = FALSE
        AND C.Created_at >= NOW() - INTERVAL '30 days'
    GROUP BY U.User_id, U.Username
)
SELECT 
    Username,
    comments_made,
    ROUND(avg_sentiment::numeric, 3) AS avg_sentiment,
    toxic_comments,
    ROUND((toxic_comments::float / comments_made * 100)::numeric, 2) AS toxicity_rate
FROM CommenterStats
WHERE comments_made >= 5
ORDER BY comments_made DESC
LIMIT 10;
```

**3. User Engagement Timeline**
```sql
SELECT 
    DATE(em.Timestamp) AS date,
    COUNT(DISTINCT p.Post_id) AS posts_created,
    SUM(em.Like_Count) AS total_likes,
    SUM(em.Comment_Count) AS total_comments,
    SUM(em.Share_Count) AS total_shares,
    AVG(em.Engagement_Rate) AS avg_engagement_rate
FROM Engagement_Metrics em
JOIN Posts p ON em.Post_id = p.Post_id
WHERE p.User_id = $1
    AND em.Timestamp >= NOW() - INTERVAL '90 days'
GROUP BY DATE(em.Timestamp)
ORDER BY date DESC;
```

**4. Viral Content Detection**
```sql
WITH ViralMetrics AS (
    SELECT 
        p.Post_id,
        p.Content,
        p.Created_at,
        EXTRACT(EPOCH FROM (NOW() - p.Created_at))/3600 AS hours_since_post,
        p.Like_Count + (p.Comment_Count * 2) + (p.Share_Count * 3) AS engagement_score,
        p.Like_Count::float / NULLIF(EXTRACT(EPOCH FROM (NOW() - p.Created_at))/3600, 0) AS viral_velocity
    FROM Posts p
    WHERE p.Created_at >= NOW() - INTERVAL '24 hours'
        AND p.Is_Deleted = FALSE
)
SELECT 
    v.*,
    u.Username,
    s.Sentiment_Label,
    CASE 
        WHEN viral_velocity > 50 THEN 'extremely_viral'
        WHEN viral_velocity > 20 THEN 'highly_viral'
        WHEN viral_velocity > 10 THEN 'viral'
        ELSE 'normal'
    END AS viral_status
FROM ViralMetrics v
JOIN Users u ON v.User_id = u.User_id
LEFT JOIN Sentiments s ON v.Post_id = s.Post_id
WHERE viral_velocity > 10
ORDER BY viral_velocity DESC
LIMIT 20;
```

**5. Sentiment Trends by Topic**
```sql
SELECT 
    h.Hashtag_text,
    COUNT(DISTINCT ph.Post_id) AS post_count,
    AVG(s.Sentiment_Score) AS avg_sentiment,
    STDDEV(s.Sentiment_Score) AS sentiment_variance,
    SUM(CASE WHEN s.Sentiment_Label = 'positive' THEN 1 ELSE 0 END)::float / COUNT(*) * 100 AS positive_percentage,
    SUM(CASE WHEN s.Is_Flagged THEN 1 ELSE 0 END) AS toxic_count,
    DATE_TRUNC('day', p.Created_at) AS trend_date
FROM Hashtags h
JOIN Post_Hashtags ph ON h.Hashtag_id = ph.Hashtag_id
JOIN Posts p ON ph.Post_id = p.Post_id
LEFT JOIN Sentiments s ON p.Post_id = s.Post_id
WHERE p.Created_at >= NOW() - INTERVAL '7 days'
GROUP BY h.Hashtag_text, DATE_TRUNC('day', p.Created_at)
HAVING COUNT(DISTINCT ph.Post_id) >= 10
ORDER BY post_count DESC, trend_date DESC;
```

### Query Optimization Techniques

**1. Index Strategy**
```sql
-- Covering index for feed queries
CREATE INDEX idx_posts_feed 
ON Posts(User_id, Created_at DESC, Is_Deleted) 
INCLUDE (Content, Like_Count, Comment_Count);

-- Partial index for active users
CREATE INDEX idx_active_users 
ON Users(Last_Active DESC) 
WHERE Is_Active = TRUE;

-- Hash index for exact lookups
CREATE INDEX idx_username_hash 
ON Users USING HASH (Username);

-- GIN index for full-text search
CREATE INDEX idx_posts_fulltext 
ON Posts USING GIN (to_tsvector('english', Content));

-- BRIN index for time-series data
CREATE INDEX idx_engagement_timestamp 
ON Engagement_Metrics USING BRIN (Timestamp);
```

**2. Materialized Views for Analytics**
```sql
CREATE MATERIALIZED VIEW mv_user_stats AS
SELECT 
    u.User_id,
    u.Username,
    COUNT(DISTINCT p.Post_id) AS total_posts,
    COUNT(DISTINCT c.Comment_id) AS total_comments,
    COUNT(DISTINCT f.Follow_id) AS follower_count,
    COALESCE(AVG(s.Sentiment_Score), 0) AS avg_sentiment,
    SUM(p.Like_Count + p.Comment_Count + p.Share_Count) AS total_engagement
FROM Users u
LEFT JOIN Posts p ON u.User_id = p.User_id AND p.Is_Deleted = FALSE
LEFT JOIN Comments c ON u.User_id = c.User_id AND c.Is_Deleted = FALSE
LEFT JOIN Follow f ON u.User_id = f.Following_id
LEFT JOIN Sentiments s ON p.Post_id = s.Post_id
GROUP BY u.User_id, u.Username;

CREATE UNIQUE INDEX ON mv_user_stats (User_id);

-- Refresh every hour
CREATE OR REPLACE FUNCTION refresh_user_stats()
RETURNS void AS $
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_stats;
END;
$ LANGUAGE plpgsql;

-- Schedule with pg_cron
SELECT cron.schedule('refresh-user-stats', '0 * * * *', 
    'SELECT refresh_user_stats()');
```

**3. Query Result Caching**
```python
from functools import lru_cache
from redis import Redis
import json

redis_client = Redis.from_url(settings.REDIS_URL)

def cache_query_result(key: str, ttl: int = 3600):
    """Decorator for caching query results in Redis"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = f"{key}:{json.dumps(args)}:{json.dumps(kwargs)}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute query
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

@cache_query_result("trending_posts", ttl=300)
def get_trending_posts(limit: int = 10):
    # Query implementation
    pass
```

---

## 🔒 Security Implementation

### Authentication Flow

```
User Login Request
    │
    ├──> Validate Credentials
    │       ├── Check username exists
    │       ├── Verify password hash (bcrypt)
    │       └── Check account status
    │
    ├──> Generate Tokens
    │       ├── Access Token (JWT, 30 min)
    │       ├── Refresh Token (JWT, 7 days)
    │       └── Store session in Redis
    │
    └──> Return Tokens + User Info
```

### Security Middleware

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import AuthService
import time
from collections import defaultdict

security = HTTPBearer()

# Rate limiting storage
rate_limit_storage = defaultdict(list)

class SecurityMiddleware:
    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials):
        """Verify JWT token"""
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
        
        return payload
    
    @staticmethod
    async def rate_limit(request: Request, limit: int = 60):
        """Rate limiting middleware"""
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        rate_limit_storage[client_ip] = [
            req_time for req_time in rate_limit_storage[client_ip]
            if current_time - req_time < 60
        ]
        
        # Check limit
        if len(rate_limit_storage[client_ip]) >= limit:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        
        # Add current request
        rate_limit_storage[client_ip].append(current_time)
    
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize user input to prevent XSS"""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            data = data.replace(char, '')
        return data
```

### SQL Injection Prevention

```python
from sqlalchemy import text

# ❌ UNSAFE - Never do this
def unsafe_query(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ SAFE - Use parameterized queries
def safe_query(username: str):
    query = text("SELECT * FROM users WHERE username = :username")
    return db.execute(query, {"username": username})

# ✅ SAFE - Use ORM
def orm_query(username: str):
    return db.query(User).filter(User.Username == username).first()
```

### Password Security

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Computational cost
)

class PasswordPolicy:
    MIN_LENGTH = 8
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    
    @classmethod
    def validate(cls, password: str) -> tuple[bool, str]:
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"
        
        if cls.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letter"
        
        if cls.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            return False, "Password must contain lowercase letter"
        
        if cls.REQUIRE_DIGIT and not any(c.isdigit() for c in password):
            return False, "Password must contain digit"
        
        if cls.REQUIRE_SPECIAL and not any(c in "!@#$%^&*" for c in password):
            return False, "Password must contain special character"
        
        return True, "Password is valid"
```

---

## 📈 Performance Optimization

### Database Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,           # Normal connections
    max_overflow=40,        # Burst connections
    pool_timeout=30,        # Wait time for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connection before use
    echo=False
)
```

### Caching Strategy

```python
# 1. Application-level caching
@lru_cache(maxsize=1000)
def get_user_by_id(user_id: int):
    return db.query(User).filter(User.User_id == user_id).first()

# 2. Redis caching for sessions
def get_user_session(user_id: int):
    cache_key = f"session:{user_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    session_data = create_session_data(user_id)
    redis_client.setex(cache_key, 3600, json.dumps(session_data))
    return session_data

# 3. Database query result caching
SELECT * FROM Posts 
WHERE User_id = 123 
AND Created_at > NOW() - INTERVAL '24 hours';
-- Results cached for 5 minutes
```

### Async Database Operations

```python
from sql<function_calls>
<invoke name="artifacts">
<parameter name="command">update</parameter>
<parameter name="id">social_media_db_readme</parameter>
<parameter name="old_str">### Async Database Operations

```python
from sql</parameter>
<parameter name="new_str">### Async Database Operations

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/db",
    echo=False
)

async def get_posts_async(user_id: int):
    async with AsyncSession(async_engine) as session:
        result = await session.execute(
            select(Post).where(Post.User_id == user_id)
        )
        return result.scalars().all()
```

### Batch Processing

```python
# Batch insert for better performance
def bulk_create_notifications(notifications: List[dict]):
    db.bulk_insert_mappings(Notification, notifications)
    db.commit()

# Process in batches
BATCH_SIZE = 1000
for i in range(0, len(users), BATCH_SIZE):
    batch = users[i:i + BATCH_SIZE]
    bulk_create_notifications(batch)
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
import pytest
from app.services.auth_service import AuthService

class TestAuthService:
    def test_password_hashing(self):
        password = "SecurePass123!"
        hashed = AuthService.get_password_hash(password)
        
        assert hashed != password
        assert AuthService.verify_password(password, hashed)
    
    def test_jwt_token_creation(self):
        data = {"user_id": 123, "username": "test_user"}
        token = AuthService.create_access_token(data)
        
        assert token is not None
        payload = AuthService.verify_token(token)
        assert payload["user_id"] == 123
    
    def test_invalid_token(self):
        invalid_token = "invalid.token.here"
        payload = AuthService.verify_token(invalid_token)
        
        assert payload is None
```

### Integration Tests

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPostAPI:
    def test_create_post(self):
        # Login first
        login_response = client.post("/api/v1/auth/login", json={
            "username": "test_user",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # Create post
        response = client.post(
            "/api/v1/posts",
            json={"content": "Test post content"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        assert "post_id" in response.json()
    
    def test_get_feed(self):
        response = client.get(
            "/api/v1/posts/feed",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert "posts" in response.json()
```

### Performance Tests

```python
import time
import concurrent.futures

def performance_test_endpoint(endpoint: str, n_requests: int = 100):
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(client.get, endpoint)
            for _ in range(n_requests)
        ]
        results = [f.result() for f in futures]
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Completed {n_requests} requests in {duration:.2f}s")
    print(f"Average: {duration/n_requests*1000:.2f}ms per request")
    print(f"RPS: {n_requests/duration:.2f}")

# Run test
performance_test_endpoint("/api/v1/posts/feed")
```

---

## 📊 Monitoring & Analytics

### Application Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge
import logging

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
active_users = Gauge('active_users', 'Number of active users')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Database Monitoring Queries

```sql
-- Monitor slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Check database size
SELECT 
    pg_size_pretty(pg_database_size('social_media_db')) AS database_size;

-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### Health Check Endpoint

```python
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        
        # Check Redis connection
        redis_client.ping()
        
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

---

## 🚀 Deployment

### Docker Configuration

**Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: social_media
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: social_media_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U social_media"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
  
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://social_media:${DB_PASSWORD}@postgres:5432/social_media_db
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./app:/app/app
  
  celery_worker:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://social_media:${DB_PASSWORD}@postgres:5432/social_media_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

### Environment Variables

**.env.example**
```env
# Application
APP_NAME=Social Media API
VERSION=1.0.0
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/social_media_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=3600

# Sentiment Analysis
SENTIMENT_MODEL_PATH=cardiffnlp/twitter-roberta-base-sentiment-latest
TOXICITY_MODEL_PATH=unitary/toxic-bert
TOXICITY_THRESHOLD=0.75
USE_GPU=False

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=/app/uploads
```

### Nginx Configuration

```nginx
upstream api_backend {
    server api:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Production Deployment Checklist

- [ ] Set strong `SECRET_KEY` in environment variables
- [ ] Configure database with SSL connections
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Set up database backups (daily automated)
- [ ] Configure log rotation and monitoring
- [ ] Enable rate limiting at API and reverse proxy levels
- [ ] Set up CI/CD pipeline for automated deployments
- [ ] Configure auto-scaling based on load metrics
- [ ] Set up health checks and alerting
- [ ] Implement database connection pooling
- [ ] Configure Redis persistence
- [ ] Set up CDN for static assets
- [ ] Enable database query monitoring
- [ ] Configure firewall rules
- [ ] Set up error tracking (e.g., Sentry)

---

## 🔮 Future Enhancements

### Planned Features

**1. Advanced AI Capabilities**
- Multi-language sentiment analysis support
- Context-aware content recommendations using collaborative filtering
- Automated content categorization and tagging
- Hate speech detection with cultural and contextual awareness
- Image and video content moderation using computer vision

**2. Enhanced Analytics**
- Real-time dashboard updates using WebSockets
- Predictive analytics for viral content detection
- User behavior forecasting with ML models
- Influence network mapping and visualization
- A/B testing framework for feature rollouts

**3. Extended Social Features**
- Groups and communities with role-based permissions
- Live streaming support with real-time chat
- Polls, surveys, and voting systems
- Event management and RSVP functionality
- Story highlights and saved collections

**4. Performance Improvements**
- Database sharding for horizontal scalability
- Read replica implementation for load distribution
- GraphQL API alongside REST for flexible queries
- WebSocket support for real-time features
- CDN integration for media delivery
- Advanced caching with Redis Cluster

**5. Moderation Enhancements**
- AI-assisted moderation with confidence scores
- Community-driven content reporting
- Automated escalation workflows
- Comprehensive appeal and review system
- Pattern detection for coordinated harmful behavior

**6. Privacy & Compliance**
- GDPR compliance tools (data export, right to be forgotten)
- End-to-end encryption for direct messages
- Two-factor authentication (2FA)
- Privacy-preserving analytics
- Granular privacy controls


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **PostgreSQL** community for robust database technology
- **Hugging Face** for pre-trained NLP models
- **Dr. Mohamed Essa** for academic guidance
- **Sama Osama** for teaching assistance
- All open-source contributors whose libraries made this project possible

---

