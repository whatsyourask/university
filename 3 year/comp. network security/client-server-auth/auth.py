from crypto import generate_keys
from re import fullmatch
from typing import Tuple


class Auth:
    """Class to share common functionality"""
    def _generate_keys(self, bits_length: int) -> None:
        """Generate keys and save them"""
        rsa, pub_key, priv_key = generate_keys(bits_length)
        self._rsa = rsa
        self._pub_key = pub_key
        self._priv_key = priv_key

    def _get_key(self, key: str) -> Tuple:
        """Extract e and n from the format (e, n)"""
        splited_key = key.split(', ')
        extracted_key = (int(splited_key[0][1:]), int(splited_key[1][:-1]))
        #print(extracted_key)
        return extracted_key

    def _check_the_key(self, key: str) -> bool:
        """Check the key that it's in proper format"""
        pattern = '\(\d*, \d*\)'
        valid = fullmatch(pattern, key)
        if not valid:
            return False
        return True

    def _encrypt(self, data: str, key: Tuple=None) -> str:
        """Encrypt one time, if the key is specified, then set it to rsa obj"""
        if key:
            self._rsa.e = key[0]
            self._rsa.n = key[1]
        return self._rsa.encrypt(data)

    def _decrypt(self, data: str, key: Tuple=None) -> str:
        """Decrypt one time, if the key is specified, then set it to rsa obj"""
        if key:
            self._rsa.d = key[0]
            self._rsa.n = key[1]
        return self._rsa.decrypt(data)

    def encrypt_twice(self, key: Tuple, data: str) -> str:
        """Encrypt twice
        First: with your private key
        Second: with public key of another side
        """
        self._rsa.e = self._priv_key[0]
        encrypted_once = self._encrypt(data).split()
        print(encrypted_once)
        encrypted_twice = self._encrypt(encrypted_once, key)
        print(encrypted_twice)
        return encrypted_twice
