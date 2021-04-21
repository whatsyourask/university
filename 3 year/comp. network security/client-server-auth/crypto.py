import sys
# To import FastModularExponentiation
sys.path.insert(0, '../../computer security/')
from rsa.backend import RSA, miller_rabin_generate
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Tuple


def generate_keys(bits_length: int) -> Tuple:
    p = miller_rabin_generate(bits_length)
    q = miller_rabin_generate(bits_length)
    n = p * q
    euler_func = (p - 1) * (q - 1)
    rsa = RSA()
    rsa.n = n
    rsa.euler_func = euler_func
    pub_key = (rsa.generate_public_key(bits_length), n)
    priv_key = (rsa.generate_private_key(), n)
    return rsa, pub_key, priv_key


def get_hash(passwd: str) -> str:
    """Get a hash of the password"""
    # TODO: Fix the issue with the hash object
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(passwd.encode('utf-8'))
    hash = digest.finalize()
    return hash
