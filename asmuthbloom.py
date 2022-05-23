import sys

from Crypto.Random import random

from mathhelpers import *
from secretsharingscheme import *


class AsmuthBloom(SecretSharingScheme):
    def __init__(self, k, n, key_size):
        super().__init__(k, n, key_size)
        p_0 = get_prime_bigger_than(256)
        self.p_0 = p_0
        self.p = generate_asmuth_bloom_sequence(self.k, self.n, self.p_0, 256)

    def generate_shares(self, s: bytes):
        shares = []

        p = self.p
        for s_chunk in s:
            if not verify_asmuth_bloom_sequence(self.k, self.n, self.p_0, p):
                raise Exception('задана послідовність не задовільняє умови послідовності Асмута-Блума')

            p_k = p[:self.k]
            product_p_k = product(p_k)

            r = random.randrange(0, math.floor((product_p_k - s_chunk) / self.p_0))
            s_i = s_chunk + r * self.p_0
            assert s_i < product_p_k

            chunk_shares = []
            for p_i in p:
                chunk_shares.append([p_i, s_i % p_i])
            shares.append(chunk_shares)

        return shares

    # MODIFIED
    # def generate_shares(self, s: bytes):
    #     shares = []
    #     p_0 = get_prime_bigger_than(2 ** 8)
    #     for s_chunk in s:
    #         p = generate_asmuth_bloom_sequence_modified(self.k, self.n, s_chunk)
    #         # p_0 = p.pop(0)
    #
    #         # if not verify_asmuth_bloom_sequence_modified(self.k, self.n, p):
    #         #     raise Exception('задана послідовність не задовільняє умови послідовності Асмута-Блума')
    #
    #         p_k = p[:self.k]
    #         print(s_chunk, p_0, p, p_k)
    #         product_p_k = product(p_k)
    #         print((product_p_k - s_chunk) / p_0)
    #         r = random.randrange(0, math.floor((product_p_k - s_chunk) / p_0) or 1)
    #         s_i = s_chunk + r * p_0
    #         assert s_i < product_p_k
    #
    #         chunk_shares = []
    #         for p_i in p:
    #             chunk_shares.append([p_i, s_i % p_i])
    #         print(chunk_shares)
    #         shares.append({'shares': chunk_shares, 'public_info': {'p_0': p_0}})
    #
    #     return shares


    def reconstruct(self, shares):
        first_chunk_share = shares[0]
        k = len(first_chunk_share)
        p = [share[0] for share in first_chunk_share]
        chunks = []
        print(first_chunk_share, k, p)
        for i in range(len(shares)):
            chunks.append([])
            for [p_i, s_i] in shares[i]:
                chunks[i].append(s_i)

        m = product([p_i for p_i in p])
        m_i = [product([p[i] for i in range(k) if i != j]) for j in range(k)]
        m_i_inverse = [module_inverse(m_i[i], p[i]) for i in range(k)]
        s_chunks = [int(sum(y[i] * m_i[i] * m_i_inverse[i] % m for i in range(k)) % m % self.p_0) for y in chunks]

        key_bytes_number = self.key_size // 8
        s = sum(s_chunks[i] * (self.key_size ** i) for i in range(key_bytes_number))
        key = s.to_bytes(key_bytes_number, byteorder=sys.byteorder)

        return key

    # MODIFIED
    # def reconstruct(self, shares):
    #     first_chunk_share = shares[0].get('shares')
    #     k = len(first_chunk_share)
    #     chunks = []
    #
    #     for share_index in range(len(shares)):
    #         chunks.append([])
    #         p = []
    #         p_0 = shares[share_index].get('public_info').get('p_0')
    #
    #         for share in shares[share_index].get('shares'):
    #             [p_i, s_i] = share
    #             chunks[share_index].append(s_i)
    #             p.append(p_i)
    #
    #         m = product([p_i for p_i in p])
    #         m_i = [product([p[i] for i in range(k) if i != j]) for j in range(k)]
    #         m_i_inverse = [module_inverse(m_i[i], p[i]) for i in range(k)]
    #         s_chunks = [int(sum(y[i] * m_i[i] * m_i_inverse[i] % m for i in range(k)) % m % p_0) for y in chunks]
    #
    #     key_bytes_number = self.key_size // 8
    #     s = sum(s_chunks[i] * (self.key_size ** i) for i in range(key_bytes_number))
    #     key = s.to_bytes(key_bytes_number, byteorder=sys.byteorder)
    #
    #     return key
