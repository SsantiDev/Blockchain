import json
import hashlib
import binascii
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from src.domain.interfaces.cryptography_service import CryptographyService

class ECDSAService(CryptographyService):
    """
    Implementation of CryptographyService using ECDSA (SECP256K1).
    """
    def calculate_hash(self, data: Any) -> str:
        if hasattr(data, "to_dict"):
            data_dict = data.to_dict(include_signature=False)
        elif isinstance(data, dict):
            data_dict = data
        else:
            data_dict = {"data": str(data)}
            
        data_string = json.dumps(data_dict, sort_keys=True)
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    def sign_data(self, data: str, private_key: ec.EllipticCurvePrivateKey) -> str:
        signature = private_key.sign(
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return binascii.hexlify(signature).decode('ascii')

    def verify_signature(self, public_key_hex: str, signature_hex: str, data: str) -> bool:
        try:
            public_key_bytes = binascii.unhexlify(public_key_hex)
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256K1(),
                public_key_bytes
            )
            
            signature_bytes = binascii.unhexlify(signature_hex)
            public_key.verify(
                signature_bytes,
                data.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False

    def generate_key_pair(self) -> Dict[str, Any]:
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_key = private_key.public_key()
        
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        return {
            "private_key": private_key,
            "public_key_hex": binascii.hexlify(public_key_bytes).decode('ascii')
        }
