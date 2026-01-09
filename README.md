# ArgonLock

Secure password manager with TOTP support built with Python and Qt.

---

## Features

- AES-256-GCM encryption with Scrypt KDF (N=2^17)
- TOTP two-factor authentication codes
- Search and auto-save functionality
- Auto-clear clipboard after 30 seconds

---

## Installation

```bash
git clone https://github.com/limbogeom/ArgonLock.git
cd ArgonLock
pip install PySide6 cryptography
```

---

### Launch application:
```bash
python main.py
```
---

## Security

- **Encryption**: AES-256-GCM with AAD
- **Key Derivation**: Scrypt (N=2^17, r=8, p=1)
- **TOTP**: HMAC-SHA1, 30s period, RFC 6238 compliant

---

## Disclaimer

Educational software - not professionally audited. Use at your own risk.

---

## License

**MIT License**

---

**By limbogeom**

