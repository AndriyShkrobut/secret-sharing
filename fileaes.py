from Crypto.Cipher import AES
from Crypto.Util import Counter


class FileAES:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def encrypt_file(self, plain: bytes, key) -> bytes:
        aes = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))

        cipher = aes.encrypt(plain)

        with open(self.output_file, 'wb') as file:
            file.write(cipher)

        return cipher

    def decrypt_file(self, cipher: bytes, key) -> bytes:
        aes = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
        plain = aes.decrypt(cipher)

        with open(self.output_file, 'wb') as file:
            file.write(plain)

        return plain
