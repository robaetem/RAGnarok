import pickle
import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
import numpy
from sentence_transformers import SentenceTransformer

def get_db_connection():
    conn = psycopg2.connect(
        database="rag_chunks",
        user="postgres",
        password="password",
        host="localhost",
        port="6024"
    )
    return conn

def execute_sql_on_db(sql_query: str, conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
    try:
        cursor.execute(sql_query)
        conn.commit()
    except Exception as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_chunks_into_db(chunks):
    try:
        conn = get_db_connection()
        register_vector(conn)
        cursor = conn.cursor()
        execute_values(
            cursor,
            """insert into chunks (file_path, page, content, embedding) values %s""",
            [(chunk["file_path"], chunk["page"], chunk["content"], chunk["embedding"].tolist()) for chunk in chunks]
        )
        conn.commit()

        if cursor:
            cursor.close()

        if conn:
            conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def get_n_closest_chunks(input_embedding, n: int): 
    conn = get_db_connection()
    register_vector(conn)
    cursor = conn.cursor()
    sql_query = """
        select *, embedding <=> %s as distance
        from chunks
        order by distance
        limit 5;
    """
    cursor.execute(sql_query, (input_embedding))
    results = cursor.fetchall()
    return results