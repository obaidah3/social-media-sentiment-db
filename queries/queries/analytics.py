import pandas as pd
from sqlalchemy import text
from database import engine

def post_count_per_user():
    return pd.read_sql(text("""
        SELECT user_id, COUNT(id) AS total_posts
        FROM posts
        GROUP BY user_id
    """), engine)

def notifications_by_user_id(user_id: int):
    return pd.read_sql(text("""
        SELECT *
        FROM notifications
        WHERE recipient_id = :user_id
        ORDER BY created_at DESC
    """), engine, params={"user_id": user_id})
