from ocr.ocr import ocr_pdf_file
from chunking.chunking import chunk_page_recursive_character_text
from embedding.nomic_embedding import embed_chunks
from database.database import insert_chunks_into_db

pdf_name = "./kleine-kattengids-compressed.pdf"
pdf_json = ocr_pdf_file(pdf_name)
chunks = chunk_page_recursive_character_text(pdf_json)
chunks_embedded = embed_chunks(chunks)
insert_chunks_into_db(chunks_embedded)