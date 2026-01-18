import pandas as pd
from sqlalchemy import text
from database import engine

def most_engaging_posts():
    return pd.read_sql(text("""
        SELECT p.id, p.content, COUNT(r.id) AS reaction_count
        FROM posts p
        LEFT JOIN reactions r ON p.id = r.post_id
        GROUP BY p.id, p.content
        ORDER BY reaction_count DESC
        LIMIT 10
    """), engine)
