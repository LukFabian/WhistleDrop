import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Crypto.PublicKey import RSA


def generate_aes_key() -> bytes:
    return AESGCM.generate_key(256)


def encrypt_file_with_aes(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, associated_data=None)
    return nonce, ciphertext  # Store nonce with the ciphertext or separately


def encrypt_key_with_rsa(public_pem: bytes, key: bytes) -> bytes:
    public_key = serialization.load_pem_public_key(public_pem)
    return public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def generate_rsa_keypair(bits: int = 2048) -> tuple[str, str]:
    key = RSA.generate(bits)
    private_key_pem = key.export_key().decode()
    public_key_pem = key.publickey().export_key().decode()
    return public_key_pem, private_key_pem

def decrypt_key_with_rsa(private_key_pem: str, encrypted_key: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )

    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key

def decrypt_file_with_aes(nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return decrypted_data