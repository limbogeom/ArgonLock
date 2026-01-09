from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

SCRYPT_N = 2 ** 17
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LENGTH = 32

def derive_key(password: str, salt: bytes) -> bytes:
     if not isinstance(password, str):
        raise TypeError("Password must be string")

     if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("Salt must be bytes")

     if len(salt) != 16:
        raise ValueError("Salt must be exactly 16 bytes")

     kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=default_backend(),
    )

     return kdf.derive(password.encode("utf-8"))