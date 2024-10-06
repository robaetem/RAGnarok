from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector
from question_answering.question_answering import generate_response
from embedding.nomic_embedding import embed_string
from database.database import get_db_connection
from hashing.hashing import hash_json
from pdf_file_handling.pdf_file_handling import download_and_extract_pages_from_pdf

def rag(question: str) -> list:
    question_embedding = embed_string(question)
    try:
        conn = get_db_connection()
        register_vector(conn)
        cursor = conn.cursor()
        cursor.execute("""
            select *, embedding <=> %s as distance
            from chunks
            order by distance
            limit 5;
        """, (question_embedding,))
        results = cursor.fetchall()

        # Extract the chunks from the database select query
        chunks = [{
            "file_name": result[4], 
            "page": result[1], 
            "content": result[2], 
            "distance": result[5]
        } for result in results]


        # Upload relevant pdf pages to the public_pdfs directory and add download_url to the chunk objects
        # Use these functions to achieve this:
        for chunk in chunks:
            print("(!) processing chunk")
            chunk_hashed = hash_json({"file_name": chunk["file_name"], "page": chunk["page"]})
            print("(!) chunk hash:", chunk_hashed)
            download_url = f"http://localhost:8000/public_pdfs/{chunk_hashed}.pdf"
            print("(!) download url:", download_url)
            download_and_extract_pages_from_pdf("pdf-files", chunk["file_name"], "./temp", [chunk["page"]], f"./public_pdfs/{chunk_hashed}.pdf")
            chunk["download_url"] = download_url

        # Generate question response based on the provided chunks
        # answer = generate_response([chunk["content"] for chunk in chunks], question)
        answer = "Bot answer"

        return {"answer": answer, "chunks": chunks}
    except Exception as e:
        print(f"An error occurred: {e}")

# rag_returns = rag("Hoeveel eet een kat per dag?")
# print(rag_returns)