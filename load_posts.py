import json
import psycopg2
from config import settings


def get_posts_from_db():
    conn = psycopg2.connect(
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port
    )
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT id, content FROM posts_post WHERE content IS NOT NULL LIMIT {settings.post_limit}"
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row[0]: row[1] for row in result}


def get_posts_from_file():
    with open(settings.data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_posts():
    if settings.data_source == "database":
        return get_posts_from_db()
    else:
        return get_posts_from_file()
