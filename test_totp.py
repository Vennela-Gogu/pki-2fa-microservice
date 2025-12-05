import time
from src.totp_utils import generate_totp_code, verify_totp_code

def read_seed():
    """Read the decrypted 64-character hex seed from data/seed.txt"""
    with open("data/seed.txt", "r") as f:
        return f.read().strip()

def test_totp():
    hex_seed = read_seed()
    
    print("\n=== Testing TOTP Generation ===")
    print("Hex Seed:", hex_seed)

    # Generate TOTP code
    code = generate_totp_code(hex_seed)
    print("Generated TOTP Code:", code)

    # Verify the TOTP code
    print("\n=== Testing TOTP Verification ===")
    is_valid = verify_totp_code(hex_seed, code)

    print("Verification Result:", is_valid)

    # Extra: show that code changes after 30 seconds
    print("\nNext code will generate in 30 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    test_totp()