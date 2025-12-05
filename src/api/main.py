# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import pyotp
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os
import time

app = FastAPI()

DATA_FILE = "data/seed.txt"
PRIVATE_KEY_PATH = "keys/student_private.pem"

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str


# ---------- 1) POST /decrypt-seed ----------
@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    try:
        # 1. Load private key
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # 2. Base64 decode
        encrypted_bytes = base64.b64decode(req.encrypted_seed)

        # 3. RSA/OAEP-SHA256 decrypt
        decrypted_seed_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 4. Convert to hex and validate
        hex_seed = decrypted_seed_bytes.decode() if isinstance(decrypted_seed_bytes, bytes) and all(32 <= b <= 126 for b in decrypted_seed_bytes) else decrypted_seed_bytes.hex()
        # the portal returns a UTF-8 hex string (most likely), so we try decode first then fallback to .hex()

        # ensure hex format: 64 chars and only 0-9a-f
        if not isinstance(hex_seed, str) or len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed.lower()):
            raise Exception("Invalid seed after decrypt")

        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        # For debugging locally you can log e (but don't expose exception messages to portal)
        # print("decrypt error:", e)
        return {"error": "Decryption failed"}


# ---------- 2) GET /generate-2fa ----------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(DATA_FILE, "r") as f:
        hex_seed = f.read().strip()

    # convert hex -> bytes -> base32 string
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)  # default SHA-1, 30s, 6 digits
    code = totp.now()

    current_time = int(time.time())
    valid_for = 30 - (current_time % 30)

    return {"code": code, "valid_for": valid_for}


# ---------- 3) POST /verify-2fa ----------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(DATA_FILE, "r") as f:
        hex_seed = f.read().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    valid = totp.verify(req.code, valid_window=1)  # ±1 step window

    return {"valid": valid}