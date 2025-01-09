from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key,load_pem_public_key
import base64
from cryptography.exceptions import InvalidSignature
import json

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    public_key_pem_str = public_key_pem.decode().replace("\n", "")

    return public_key_pem_str, private_key_pem.decode()


def sign_request(private_key_pem):
    """
    Signs a predefined dictionary payload containing a country code with the provided private key.
    """
    payload = {"country_code": "EG"}  
    payload_json = json.dumps(payload)  
    
    private_key = load_pem_private_key(private_key_pem.encode(), password=None)
    
    signature = private_key.sign(
        payload_json.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    
    return base64.b64encode(signature).decode()


def verify_request_signature(signature_base64, public_key_pem):
    """
    Verifies a predefined dictionary payload containing a country code against the provided signature.
    """
    payload = {"country_code": "EG"}  
    payload_json = json.dumps(payload)  
    signature = base64.b64decode(signature_base64)
    public_key = load_pem_public_key(public_key_pem.encode())
    
    try:
        public_key.verify(
            signature,
            payload_json.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False

