import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_signup():
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!",
            "name": "Test User",
            "country": "Egypt"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_signup_duplicate_email():
    """Test registration with duplicate email"""
    # First signup
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "TestPass123!",
            "name": "User One"
        }
    )

    # Second signup with same email
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "TestPass123!",
            "name": "User Two"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login():
    """Test user login"""
    # First create a user
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "TestPass123!",
            "name": "Login User"
        }
    )

    # Now login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "TestPass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password():
    """Test login with wrong password"""
    # Create user
    client.post(
        "/api/v1/auth/signup",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "TestPass123!",
            "name": "Wrong Pass User"
        }
    )

    # Try wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "WrongPassword123!"
        }
    )
    assert response.status_code == 401


def test_get_current_user():
    """Test getting current user info"""
    # Create and login user
    signup_response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "currentuser",
            "email": "current@example.com",
            "password": "TestPass123!",
            "name": "Current User"
        }
    )
    token = signup_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["Username"] == "currentuser"
    assert data["Email"] == "current@example.com"


def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403  # Forbidden without credentials