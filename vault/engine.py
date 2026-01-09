import json
from crypto.aes import encrypt, decrypt

class Vault:
    def __init__(self, password: str, data: dict):
        self._password = password
        self._data = data
        if "entries" not in self._data:
            self._data["entries"] = []

    def list_entries(self):
        return self._data["entries"]
    
    def add_entry(self, entry: dict):
        self._validate_entry(entry)
        self._data["entries"].append(entry)

    def delete_entry(self, index: int):
        del self._data["entries"][index]

    def update_entry(self, index: int, entry: dict):
        self._validate_entry(entry)
        self._data["entries"][index] = entry

    def serialize(self) -> bytes:
        return encrypt(self._password, self._data)
    
    def _validate_entry(self, entry: dict):
        if not entry.get("site"):
            raise ValueError("Site is required")
        if not entry.get("password"):
            raise ValueError("Password is required")
        
        if entry.get("totp"):
            totp = entry["totp"]
            if not isinstance(totp, dict) or not totp.get("secret"):
                raise ValueError("Invalid TOTP format")