import secrets
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .kdf import derive_key

MAGIC = b"VAULT"
VERSION_V1 = b"\x01"
VERSION_V2 = b"\x02"
SALT_SIZE = 16
NONCE_SIZE = 12

def encrypt(password: str, data: dict) -> bytes:
    salt = secrets.token_bytes(SALT_SIZE)
    key = derive_key(password, salt)

    nonce = secrets.token_bytes(NONCE_SIZE)
    aes = AESGCM(key)

    plaintext = json.dumps(data).encode()
    aad = MAGIC + VERSION_V2 + salt
    ciphertext = aes.encrypt(nonce, plaintext, aad)

    return MAGIC + VERSION_V2 + salt + nonce + ciphertext


def decrypt(password: str, blob: bytes) -> dict:
    if not blob.startswith(MAGIC):
        raise ValueError("Bad magic")
    
    if len(blob) < 6:
        try:
            return decrypt_v1(password, blob)
        except:
            raise ValueError("Invalid vault file")

    version = blob[5:6]
    
    if version == VERSION_V1:
        return decrypt_v1(password, blob)
    elif version == VERSION_V2:
        return decrypt_v2(password, blob)
    else:
        return decrypt_v1(password, blob)


def decrypt_v1(password: str, blob: bytes) -> dict:
    salt = blob[5:5+SALT_SIZE]
    nonce = blob[5+SALT_SIZE:5+SALT_SIZE+NONCE_SIZE]
    ciphertext = blob[5+SALT_SIZE+NONCE_SIZE:]

    key = derive_key(password, salt)
    aes = AESGCM(key)

    plaintext = aes.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode())


def decrypt_v2(password: str, blob: bytes) -> dict:
    salt = blob[6:6+SALT_SIZE]
    nonce = blob[6+SALT_SIZE:6+SALT_SIZE+NONCE_SIZE]
    ciphertext = blob[6+SALT_SIZE+NONCE_SIZE:]

    key = derive_key(password, salt)
    aes = AESGCM(key)

    aad = MAGIC + VERSION_V2 + salt
    plaintext = aes.decrypt(nonce, ciphertext, aad)
    return json.loads(plaintext.decode())