import hmac
import hashlib
import struct
import time

def generate_totp(totp_data: dict) -> tuple[str, int]:
    secret = totp_data["secret"]
    digits = totp_data.get("digits", 6)
    period = totp_data.get("period", 30)
    
    secret_bytes = base32_decode(secret)
    
    current_time = int(time.time())
    time_counter = current_time // period
    
    counter_bytes = struct.pack(">Q", time_counter)
    
    hmac_hash = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
    
    offset = hmac_hash[-1] & 0x0F
    truncated = struct.unpack(">I", hmac_hash[offset:offset+4])[0]
    truncated &= 0x7FFFFFFF
    
    code = truncated % (10 ** digits)
    code_str = str(code).zfill(digits)
    
    remaining = period - (current_time % period)
    
    return code_str, remaining

def base32_decode(s: str) -> bytes:
    s = s.upper().replace(" ", "")
    padding = (8 - len(s) % 8) % 8
    s += "=" * padding
    
    result = bytearray()
    buffer = 0
    bits_left = 0
    
    for char in s:
        if char == "=":
            break
        
        if "A" <= char <= "Z":
            val = ord(char) - ord("A")
        elif "2" <= char <= "7":
            val = ord(char) - ord("2") + 26
        else:
            raise ValueError(f"Invalid base32 character: {char}")
        
        buffer = (buffer << 5) | val
        bits_left += 5
        
        if bits_left >= 8:
            bits_left -= 8
            result.append((buffer >> bits_left) & 0xFF)
    
    return bytes(result)