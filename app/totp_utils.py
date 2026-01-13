import pyotp
import base64
import time

def generate_totp(hex_seed: str):
    # The instructor sends a 64-char hex seed. 
    # We must convert hex -> bytes -> base32 for the TOTP library.
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # Standard TOTP: 6 digits, 30s interval, SHA1
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6, digest='sha1')
    
    # Calculate how many seconds are left in the current 30s window
    current_time = int(time.time())
    valid_for = 30 - (current_time % 30)
    
    return totp.now(), valid_for

def verify_totp(hex_seed: str, code: str):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, interval=30, digits=6, digest='sha1')
    # valid_window=1 allows for 30s clock skew
    return totp.verify(code, valid_window=1)