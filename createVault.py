from crypto.aes import encrypt

password = "password"
data = {
    "entries": []
}

blob = encrypt(password, data)

with open("safe.vault", "wb") as f:
    f.write(blob)

print("Vault created, size:", len(blob))