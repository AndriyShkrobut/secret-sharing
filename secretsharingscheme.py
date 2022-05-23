from typing import List


class SecretSharingScheme:
    def __init__(self, k: int, n: int, key_size: int):
        self.k = k
        self.n = n
        self.key_size = key_size

    def generate_shares(self, shares: List[List[int]]):
        pass

    def reconstruct(self, s: bytes):
        pass
