import pandas as pd
from sqlalchemy import text
from database import engine

def all_posts():
    return pd.read_sql(text("SELECT * FROM posts"), engine)

def posts_by_user(username):
    return pd.read_sql(text("""
        SELECT *
        FROM posts
        WHERE user_id = (
            SELECT id FROM users WHERE username = :username
        )
    """), engine, params={"username": username})

def posts_by_visibility():
    return pd.read_sql(text("""
        SELECT visibility, COUNT(*) AS post_count
        FROM posts
        GROUP BY visibility
    """), engine)
