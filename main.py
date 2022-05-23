import argparse
import json
from time import time

from Crypto import Random

from asmuthbloom import AsmuthBloom
from fileaes import FileAES
from shamir import Shamir

MODES = ['encrypt', 'decrypt']
SHARING_SCHEMES = {
    'shamir': Shamir,
    'asmuth-bloom': AsmuthBloom
}


def validate_arguments(args):
    try:
        if args.mode == MODES[0]:
            if not (args.n and args.k):
                n_missing_message = "--n" if not args.n else ""
                k_missing_message = "--k" if not args.k else ""
                is_both_missing = k_missing_message != "" and n_missing_message != ""
                raise Exception(
                    f'необхідні аргументи в режимі "encrypt" відсутні: {k_missing_message} {"та" if is_both_missing else ""} {n_missing_message}'
                )

            if args.k > args.n:
                raise Exception('помилка вхідних даних: введіть k \u2264 n')

        if not args.shares.endswith('.json'):
            raise Exception('файл з частинами секрету має бути у форматі json')
    except Exception as error:
        print(error.with_traceback(error.__traceback__))


def main(args):
    validate_arguments(args)

    [encrypt_mode, decrypt_mode] = MODES
    mode = args.mode
    n = args.n
    k = args.k
    input_file_path = args.input
    output_file_path = args.output
    shares_file_path = args.shares

    key_bytes_number = args.aes // 8
    chosen_scheme = SHARING_SCHEMES[args.scheme](k, n, args.aes)

    with open(input_file_path, 'rb') as file:
        input_file = file.read()

    if mode == encrypt_mode:
        key = Random.new().read(key_bytes_number)
        FileAES(output_file_path).encrypt_file(input_file, key)

        t0 = time()
        shares = chosen_scheme.generate_shares(key)
        t1 = time()
        print(f'Схема: {args.scheme}, Генерація частин секрету.\nЧас виконання для (k, n) = ({k}, {n}) - {t1 - t0}')

        with open(shares_file_path, 'w') as file:
            json.dump(shares, file)
    else:
        with open(shares_file_path, 'r') as file:
            shares = json.load(file)

        t0 = time()
        key = chosen_scheme.reconstruct(shares)
        t1 = time()
        print(f'Схема: {args.scheme}, Реконструкція секрету.\nЧас виконання для (k, n) = ({k}, {n}) - {t1 - t0}')

        FileAES(output_file_path).decrypt_file(input_file, key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Засіб з інтерфейсом командного рядка для зашифрування файл та розділення ключа шифрування між n учасниками з використанням схем розділення секрету'
    )
    parser.add_argument(
        '-s', '--scheme',
        dest='scheme',
        help='Схема розділення секрету: shamir, asmuth-bloom',
        choices=SHARING_SCHEMES.keys(),
        required=True
    )
    parser.add_argument(
        '-m',
        '--mode',
        metavar='mode',
        dest='mode',
        help='Режим виконання: encrypt, decrypt',
        choices=MODES,
        required=True
    )
    parser.add_argument(
        '-i',
        '--input',
        metavar='path',
        dest='input',
        help='Вхідний файл: шлях до вхідного файлу',
        required=True
    )
    parser.add_argument(
        '-o',
        '--output',
        metavar='path',
        dest='output',
        help='Вихідний файл: шлях до вихідного зашифрованого файлу',
        required=True
    )
    parser.add_argument(
        '--shares',
        metavar='path',
        dest='shares',
        help='Файл json для збереження розділеного секрету: шлях до json файлу із згенерованими частинами секрету',
        default='shares.json'
    )
    parser.add_argument(
        '-n',
        '--n',
        dest='n',
        help='Кількість учасників схеми: число згенерованих ключів',
        type=int,
        default=0,
        required=True
    )
    parser.add_argument(
        '-k',
        '--k',
        dest='k',
        help='Кількість учасників для відновлення: число необхідних ключів для відновлення',
        type=int,
        required=True
    )
    parser.add_argument(
        '--aes',
        dest='aes',
        help='Варіація AES: розмір ключа шифрування',
        choices=[128, 192, 256],
        type=int,
        default=256,
    )
    parsed_args = parser.parse_args()
    try:
        main(parsed_args)
    except Exception as error:
        print(error)
