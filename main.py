from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_full.rag import rag
from hashing.hashing import hash_json
from pdf_file_handling.pdf_file_handling import download_from_fileshare, extract_pages_from_pdf
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/public_pdfs", StaticFiles(directory="public_pdfs"), name="pdfs")

class GenerateAnswerRequest(BaseModel):
    question: str

class GetPdfRequest(BaseModel):
    file_path: str
    page: int
    access_key: str

@app.post("/generate-answer")
def generate_answer(generate_answer_request: GenerateAnswerRequest):
    """
        ### Input
            - question 
        
        ### Returns
            Answer and also a list of json objects (one json object for each relevant chunk). The json objects are structured as:
                - download path to pdf file
                - page number
                - content
    """
    question = generate_answer_request.question
    answer = rag(question)
    # answer = {"answer": "bot answer", "chunks": [{"file_path": "./kleine-kattengids-compressed.pdf","page": 33,"content": "# Wanneer kunt u er beter geen andere kat bij nemen?","distance": 0.25741089924638727,"file_access_key": "aadbe3d4e0b0fc5cfe50415bbfe042a2e91e1abdf2872c71768a1480a4136e6a"},{"file_path": "./kleine-kattengids-compressed.pdf","page": 34,"content": "Voor mensen kan het erg leuk zijn om veel katten te hebben. Voor katten is het dat in zijn om veel katten te hebben. Zou u dat leuk vinden? Nee toch? Waarom zou uw kat het dan wel leuk moeten vinden als hij in zijn eigen huis ineens een vreemde kat tegenkomt?","distance": 0.2653573751449585,"file_access_key": "8942a9af0fa2ef86aa8d04ec075a49b57b5901c9a646d8cb07af85ab651f12d4"}]}
    if answer is None:
        raise HTTPException(status_code=500, detail="Internal server error: No answer generated")
    return answer

@app.post("/get-pdf")
def get_pdf(get_pdf_request: GetPdfRequest):
    try:
        request_hash = hash_json({"file_path": get_pdf_request.file_path, "page": get_pdf_request.page})
        if request_hash == get_pdf_request.access_key:
            download_from_fileshare("pdf-files", get_pdf_request.file_path, "./temp")
            extracted_pdf_path = f"./temp/extracted.pdf"
            extract_pages_from_pdf(f"./temp/{get_pdf_request.file_path}", [get_pdf_request.page], extracted_pdf_path)
            return FileResponse(extracted_pdf_path, media_type="application/pdf", filename=get_pdf_request.file_path)
        else:
            return {"status": "unauthorized", "message": "Access key incorrect"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"status": "error", "message": e}