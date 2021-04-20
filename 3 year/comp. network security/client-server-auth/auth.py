from cryptography.hazmat.primitives import hashes


class Authentication:
    def get_hash(self, passwd: str) -> str:
        """Get a hash of the password"""
        # TODO: Fix the issue with the hash object
        digest = hashes.Hash(hashes.SHA256())
        digest.update(passwd.encode('utf-8'))
        hash = digest.finalize()
        return hash


def main():
    auth = Authentication()
    hash = auth.get_hash('password')
    print(hash)


if __name__=='__main__':
    main()
