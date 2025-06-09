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

    query = f"""
        SELECT {settings.post_id_column} AS id, {settings.post_content_column} AS content
        FROM {settings.post_table_name}
        WHERE {settings.post_content_column} IS NOT NULL
        LIMIT {settings.post_limit}
    """

    cursor.execute(query)
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
