from dotenv import load_dotenv
import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import nest_asyncio

def ocr_pdf_file(file_path: str):
    """
        ### args 
            file_path: file path of the pdf file

        ### returns
            list of json objects (one for each page of the pdf) that contain:
                - page
                - file_path
                - content

    """
    load_dotenv()
    nest_asyncio.apply()

    parser = LlamaParse(result_type="markdown")
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[file_path], file_extractor=file_extractor).load_data()
    documents_json = [{"page": index+1, "file_path": file_path, "content": document.text} for index, document in enumerate(documents)]
    return documents_json