from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def decrypt_seed():
    # Load private key
    with open("keys/student_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Load encrypted seed
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    encrypted_seed = base64.b64decode(encrypted_seed_b64)

    # Decrypt
    decrypted = private_key.decrypt(
        encrypted_seed,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
    )

    print("Decrypted Seed:", decrypted.decode())
    return decrypted.decode()

if __name__ == "__main__":
    decrypt_seed()