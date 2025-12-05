#!/usr/bin/env python3

# Cron script to log 2FA codes every minute

import os
from datetime import datetime, timezone
import pyotp

SEED_FILE = "/data/seed.txt"    # persistent seed file

def read_seed():
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, "r") as f:
        return f.read().strip()

def generate_totp(hex_seed):
    # Convert hex to base32 (needed for Google Authenticator style)
    base32_seed = pyotp.utils.hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

def main():
    seed = read_seed()
    if not seed:
        print("Seed not found")
        return

    code = generate_totp(seed)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()