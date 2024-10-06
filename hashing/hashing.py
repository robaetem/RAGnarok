import json
import hashlib
import os
from dotenv import load_dotenv

def generate_secret_key():
    return os.urandom(32).hex()

def hash_json(json_obj):
    load_dotenv()
    json_str = json.dumps(json_obj, sort_keys=True)
    secret_str = json_str + os.getenv("PDF_API_ACCESS_KEY")
    json_hash = hashlib.sha256(secret_str.encode()).hexdigest()
    return json_hash

# print(hash_json({
#     "file_path": "kleine-kattengids-compressed.pdf",
#     "page": 69
# }))