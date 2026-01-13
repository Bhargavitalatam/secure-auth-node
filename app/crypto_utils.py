import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_rsa_oaep(private_key_pem: bytes, encrypted_data_b64: str):
    # Load the student private key
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    
    # Decode the base64 encrypted seed from the API
    ciphertext = base64.b64decode(encrypted_data_b64)
    
    # Decrypt using RSA-OAEP with SHA256
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')