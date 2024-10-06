from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_page_recursive_character_text(pdf_json):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )

    chunks = []

    # Iterate over pages, convert each page to list of chunks and add to chunks list
    for page_json in pdf_json:
        page_chunks = text_splitter.split_text(page_json["content"])
        for chunk in enumerate(page_chunks):
            chunks.append({
                "page": page_json["page"],
                "file_path": page_json["file_path"],
                "content": chunk[1]
            })

    return chunks