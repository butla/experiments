import time
import random
import itertools


def random_permuts(text: str):
    while True:
        character_list = list(text)
        random.shuffle(character_list)
        yield ''.join(character_list)


def regular_permuts(text: str):
    for permut in itertools.permutations(text):
        yield ''.join(permut)


if __name__ == '__main__':
    zagadka = 'jedziemy sobie pociągiem i jestem trochę zmęczony, ale jednak wesoło'
    print(f'Hasło to:\n{zagadka}\n')
    print('Losowe przetasowania jego liter to:')
    # for p in regular_permuts(zagadka):
    for p in random_permuts(zagadka):
        print(p)
        time.sleep(0.1)
