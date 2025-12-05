import base64
import pyotp


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    """
    # 1. Convert hex seed (string) → bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # 2. Convert bytes → Base32 string
    base32_seed = base64.b32encode(seed_bytes).decode()

    # 3. Create TOTP object (SHA-1, 30s period, 6 digits)
    totp = pyotp.TOTP(base32_seed)

    # 4. Generate current 6-digit TOTP code
    code = totp.now()

    # 5. Return code
    return code



def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    """
    # 1. Convert hex seed → bytes → Base32 string
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    # 2. Create TOTP object
    totp = pyotp.TOTP(base32_seed)

    # 3. Verify with ± valid_window time steps (default ±30s)
    return totp.verify(code, valid_window=valid_window)