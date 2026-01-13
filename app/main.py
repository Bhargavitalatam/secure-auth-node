from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from .crypto_utils import decrypt_rsa_oaep
from .totp_utils import generate_totp, verify_totp

app = FastAPI()
SEED_PATH = "/data/seed.txt"

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(req: SeedRequest):
    try:
        with open("student_private.pem", "rb") as f:
            priv_key = f.read()
        # RSA/OAEP Decryption with SHA-256 and MGF1
        decrypted = decrypt_rsa_oaep(priv_key, req.encrypted_seed)
        
        # Persistent storage at /data/seed.txt
        os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(decrypted)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    # 6-digit TOTP code generation
    code, valid_for = generate_totp(seed)
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
async def verify_2fa(req: VerifyRequest):
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed missing")
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    # Verify with ±1 period tolerance
    is_valid = verify_totp(seed, req.code)
    return {"valid": is_valid}