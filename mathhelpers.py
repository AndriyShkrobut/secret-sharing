def product(numbers):
    result = 1

    for i in numbers:
        result *= i

    return result


def extended_euclidean(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return b, x0, y0


def module_inverse(b, n):
    g, x, _ = extended_euclidean(b, n)

    if g != 1:
        raise Exception('не вдалося знайти обернене число за модулем')

    return x % n


def lagrange_basis(x, k, i, p):
    multipliers = []
    for j in range(k):
        if j == i:
            continue
        multipliers.append(-x[j] * module_inverse(x[i] - x[j], p))

    l_i = product(multipliers)
    return l_i % p


def get_primes_from_range(a, limit):
    result = []
    prime_candidate = a

    while len(result) < limit:
        if prime_candidate > 1:
            for i in range(2, prime_candidate):
                if (prime_candidate % i) == 0:
                    break
            else:
                result.append(prime_candidate)
        prime_candidate += 1

    return result


def get_prime_bigger_than(x: int):
    [p] = get_primes_from_range(x + 1, 1)
    return p


def verify_asmuth_bloom_sequence(k, n, p_0, p):
    higher_product = p_0
    for i in range(k - 1):
        higher_product *= p[n - i - 1]

    lower_product = 1
    for i in range(k):
        lower_product *= p[i]

    return higher_product < lower_product


def verify_asmuth_bloom_sequence_modified(k, n, p):
    p_0 = p[0]
    new_p = p[1:]

    higher_product = p_0
    for i in range(k - 1):
        higher_product *= new_p[n - i - 1]

    lower_product = 1
    for i in range(k):
        lower_product *= new_p[i]

    return higher_product < lower_product


def is_prime(n: int):
    if n <= 3:
        return n > 1
    if not n % 2 or not n % 3:
        return False
    i = 5
    stop = int(n ** 0.5)
    while i <= stop:
        if not n % i or not n % (i + 2):
            return False
        i += 6
    return True


def generate_asmuth_bloom_sequence(k, n, p_0, secret):
    initial_multiplier = int(secret / 10)

    sequence_valid = False
    # max_retries = 25
    # current_try = 1
    while not sequence_valid:
        p = []
        [temp_prime] = get_primes_from_range(secret * initial_multiplier, 1)
        for _ in range(n):
            [temp_prime] = get_primes_from_range(temp_prime + 1, 1)
            p.append(temp_prime)

        if verify_asmuth_bloom_sequence(k, n, p_0, p):
            sequence_valid = True
        else:
            initial_multiplier += 1
            # current_try += 1

    return p


def generate_asmuth_bloom_sequence_modified(k, n, secret):
    if secret == 0:
        return 0
    initial_multiplier = int(secret / 10)

    p_0 = get_prime_bigger_than(secret)

    sequence_valid = False
    max_retries = 100
    current_try = 1
    while not sequence_valid and current_try != max_retries:
        p = [p_0]
        temp_prime = get_prime_bigger_than(1 * initial_multiplier if secret == 0 else secret * initial_multiplier)
        for _ in range(n):
            temp_prime = get_prime_bigger_than(temp_prime)
            p.append(temp_prime)

        if verify_asmuth_bloom_sequence_modified(k, n, p):
            sequence_valid = True
        else:
            initial_multiplier += 1
            current_try += 1

    return p
