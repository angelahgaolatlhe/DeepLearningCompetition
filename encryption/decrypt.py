import argparse
import base64
import os
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"DLENC1"
NONCE_SIZE = 12


def load_private_key():
    raw = os.environ.get("PRIVATE_KEY", "")
    if not raw:
        raise ValueError("PRIVATE_KEY manquante")
    if "-----BEGIN" in raw:
        data = raw.encode("utf-8")
    else:
        try:
            data = base64.b64decode(raw)
        except Exception as exc:
            raise ValueError("PRIVATE_KEY invalide") from exc
    return serialization.load_pem_private_key(data, password=None)


def decrypt_file(input_path: str, output_path: str):
    private_key = load_private_key()
    with open(input_path, "rb") as f:
        blob = f.read()

    if len(blob) < len(MAGIC) + 2 + NONCE_SIZE:
        raise ValueError("Fichier chiffré invalide")
    if blob[: len(MAGIC)] != MAGIC:
        raise ValueError("Format de fichier inconnu")

    idx = len(MAGIC)
    enc_key_len = int.from_bytes(blob[idx : idx + 2], "big")
    idx += 2
    nonce = blob[idx : idx + NONCE_SIZE]
    idx += NONCE_SIZE
    enc_key = blob[idx : idx + enc_key_len]
    idx += enc_key_len
    ciphertext = blob[idx:]

    aes_key = private_key.decrypt(
        enc_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, "wb") as f:
        f.write(plaintext)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        decrypt_file(args.input, args.output)
    except Exception as exc:
        print(f"Erreur déchiffrement: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
