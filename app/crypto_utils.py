from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()
    
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return priv_pem, pub_pem

def decrypt_rsa_oaep(private_key_pem, encrypted_data_b64):
    import base64
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    ciphertext = base64.b64decode(encrypted_data_b64)
    
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

def sign_and_encrypt_commit(commit_hash, student_priv_pem, instructor_pub_pem):
    import base64
    # 1. Sign (PSS)
    priv_key = serialization.load_pem_private_key(student_priv_pem, password=None)
    signature = priv_key.sign(
        commit_hash.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    # 2. Encrypt (OAEP)
    inst_pub_key = serialization.load_pem_public_key(instructor_pub_pem)
    encrypted_sig = inst_pub_key.encrypt(
        signature,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return base64.b64encode(encrypted_sig).decode()