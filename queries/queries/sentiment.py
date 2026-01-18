import pandas as pd
from sqlalchemy import text
from database import engine

def comment_sentiments():
    return pd.read_sql(text("""
        SELECT c.content, s.score, s.label
        FROM comments c
        JOIN sentiments s ON c.id = s.comment_id
    """), engine)
