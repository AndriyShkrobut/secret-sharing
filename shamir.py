import sys

from Crypto.Random import random

from mathhelpers import lagrange_basis
from secretsharingscheme import SecretSharingScheme

P = 2**257 - 93


class Shamir(SecretSharingScheme):
    def __init__(self, k, n, key_size):
        super().__init__(k, n, key_size)

    def generate_shares(self, s: bytes):
        k = self.k
        n = self.n
        a_0 = int.from_bytes(s, byteorder=sys.byteorder)
        p = P

        q = [a_0]
        for i in range(k - 1):
            a_i = random.randint(0, p)
            q.append(a_i)

        shares = []
        for i in range(1, n + 1):
            x = [i ** j for j in range(k)]
            y_i = sum(q[j] * x[j] % p for j in range(k))

            share = [i, y_i % p]
            shares.append(share)

        return {'shares': shares, 'public_info': {'p': p}}

    def reconstruct(self, payload):
        p = payload.get('public_info').get('p')
        shares = payload.get('shares')
        k = len(shares)

        x = []
        y = []
        for [i, s_i] in shares:
            x.append(i)
            y.append(s_i)

        interpolation_polynomial = []
        for i in range(k):
            y_i = y[i]
            l_i = lagrange_basis(x, k, i, p)

            interpolation_polynomial.append(y_i * l_i % p)

        s = int(sum(interpolation_polynomial) % p) % 2 ** self.key_size
        key = s.to_bytes(self.key_size // 8, byteorder=sys.byteorder)

        return key
