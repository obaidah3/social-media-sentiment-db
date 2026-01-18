import pandas as pd
from sqlalchemy import text
from database import engine

def all_users():
    return pd.read_sql(text("SELECT * FROM users"), engine)

def users_with_no_posts():
    return pd.read_sql(text("""
        SELECT u.username
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        WHERE p.id IS NULL
    """), engine)

def recent_users():
    return pd.read_sql(text("""
        SELECT username, created_at
        FROM users
        WHERE created_at >= NOW() - INTERVAL '6 months'
    """), engine)

def dark_theme_users():
    return pd.read_sql(text("""
        SELECT u.username, up.theme, up.language
        FROM users u
        JOIN user_preferences up ON u.id = up.user_id
        WHERE up.theme = 'dark'
    """), engine)
