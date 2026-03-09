import argparse
import base64
import os
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"DLENC1"
NONCE_SIZE = 12
KEY_SIZE = 32


def load_public_key(path: str):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
    else:
        data = os.environ.get("PUBLIC_KEY", "").encode("utf-8")
        if not data:
            raise ValueError("Clé publique introuvable")
    return serialization.load_pem_public_key(data)


def encrypt_file(input_path: str, output_path: str, public_key_path: str):
    public_key = load_public_key(public_key_path)
    with open(input_path, "rb") as f:
        plaintext = f.read()

    aes_key = os.urandom(KEY_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    if len(encrypted_key) > 65535:
        raise ValueError("Clé chiffrée trop longue")

    with open(output_path, "wb") as f:
        f.write(MAGIC)
        f.write(len(encrypted_key).to_bytes(2, "big"))
        f.write(nonce)
        f.write(encrypted_key)
        f.write(ciphertext)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--public-key", default="encryption/public_key.pem")
    args = parser.parse_args()

    try:
        encrypt_file(args.input, args.output, args.public_key)
    except Exception as exc:
        print(f"Erreur chiffrement: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
