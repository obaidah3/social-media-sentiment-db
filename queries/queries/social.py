import pandas as pd
from sqlalchemy import text
from database import engine

def followed_users_by_id(user_id: int):
    return pd.read_sql(text("""
        SELECT u.*
        FROM users u
        JOIN follows f ON u.id = f.following_id
        WHERE f.follower_id = :user_id
    """), engine, params={"user_id": user_id})
