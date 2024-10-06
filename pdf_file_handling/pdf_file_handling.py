from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader, PdfWriter

def download_from_fileshare(container_name, file_name, local_path):
    """
        Download file from container_name/file_name and store it in the directory defined by local_path
    """
    try:
        print("(3) download_from_fileshare:",container_name,file_name,local_path)
        load_dotenv()

        blob_service_client = BlobServiceClient.from_connection_string(conn_str=os.getenv("FILE_SHARE_CNX_STR"))
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)
        with open(os.path.join(local_path, file_name), "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        print("File successfully downloaded!")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def extract_pages_from_pdf(pdf_file: str, pages: list, target_path: str):
    """
        Extracts the pages defined in pages list from pdf_file and stores it at the path defined by target_path
    """
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
    for page_number in pages:
        if 0 <= page_number < len(reader.pages):
            writer.add_page(reader.pages[page_number-1])
        else:
            print(f"Page number {page_number} is out of range.")
    
    with open(target_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"Selected pages have been extracted and saved to ${target_path}.")

def download_and_extract_pages_from_pdf(container_name: str, file_name: str, local_path: str, pages: list, output_pdf_path: str):
    """
        Downloads a PDF from Azure Blob Storage and extracts specified pages to a new PDF file.
        
        Parameters:
            container_name (str): The name of the container in Azure Blob Storage.
            file_name (str): The name of the PDF file to download.
            local_path (str): The local directory to save the downloaded PDF.
            pages (list): A list of page numbers to extract from the PDF.
            output_pdf_path (str): The path where the extracted pages PDF will be saved.
    """
    # Step 1: Download the PDF from Azure Blob Storage
    print("(2) downloading file from fileshare")
    if file_name.startswith("./"):
        file_name =  file_name[2:]
    download_from_fileshare(container_name, file_name, local_path)
    print("(2) pdf file downloaded from fileshare")

    # Step 2: Define the full path of the downloaded PDF
    print("(2) extracting pages from pdf")
    pdf_file_path = os.path.join(local_path, file_name)

    # Step 3: Extract specified pages from the downloaded PDF
    extract_pages_from_pdf(pdf_file_path, pages, output_pdf_path)
    print("(2) extracted pages from pdf")

# download_and_extract_pages_from_pdf("pdf-files", "kleine-kattengids-compressed.pdf", "./temp", [3,4], "./public_pdfs/testinggg.pdf")