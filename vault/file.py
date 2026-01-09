import os
from crypto.aes import decrypt, encrypt

MAGIC = b"VAULT"

def open_vault(filename: str, password: str):
    if not os.path.exists(filename):
        return {"entries": []}
    
    with open(filename, "rb") as f:
        blob = f.read()

    if not blob:
        return {"entries": []}

    if not blob.startswith(MAGIC):
        raise ValueError("Not a vault file")
    
    data = decrypt(password, blob)
    return data

def create_vault(filename: str, password: str):
    data = {"entries": []}
    blob = encrypt(password, data)
    with open(filename, "wb") as f:
        f.write(blob)