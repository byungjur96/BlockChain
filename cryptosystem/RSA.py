# 이산 수학 5강 참조하기

import random
from time import sleep
import sys


class Euclide:
    # 범위 내의 소수를 모두 구하는 함수
    @staticmethod
    def find_prime(variable):
        result = set({})
        a, b = map(int, input('Define range of '+variable+':').split(','))
        for n in range(a, b):
            state = True
            for i in range(2, n):
                if n % i == 0:
                    state = False
            if state:
                result.add(n)
        return result

    # 최대공약수를 구하는 함수
    @staticmethod
    def gcd(a, b):
        while b != 0:
            temp = a % b
            a = b
            b = temp
        return abs(a)

    # 서로소를 구하는 함수
    def coprime(self, a, b):
        if self.gcd(a, b) == 1:
            return True
        else:
            return False


class RSA:
    # 7,000 ~ 8,000 사이의 임의의 소수를 출력하는 함수
    def make_p(self):
        list_p = Euclide.find_prime('p')
        while len(list_p) == 0:
            print('Chosen range has no prime number!')
            list_p = Euclide.find_prime('p')
        list_p = list(list_p)
        p = list_p[random.randrange(0, len(list_p))]
        return p

    # 9,000 ~ 10,000 사이의 임의의 소수를 출력하는 함수
    def make_q(self):
        list_q = Euclide.find_prime('q')
        while len(list_q) == 0:
            print('Chosen range has no prime number!')
            list_q = Euclide.find_prime('q')
        list_q = list(list_q)
        q = list_q[random.randrange(0, len(list_q))]
        return q

    # n과 pi를 계산하는 함수
    def make_key(self, p, q):
        n = p * q
        pi = (p - 1) * (q - 1)
        return [n, pi]

    # pi와 서로소이면서 pi보다 작은 수들을 모두 구해서 그 중 임의의 값을 e로 지정하는 함수
    def find_e(self, pi):
        list_e = set({})
        euclide = Euclide()
        for i in range(2, pi):
            if Euclide.coprime(euclide, i, pi):
                list_e.add(i)
        list_e = list(list_e)
        e = list_e[random.randrange(0, len(list_e))]
        return e

    def find_d(self, e, pi):
        d = []
        i = 1

        while len(d) == 0:
            if (i * e) % pi == 1:
                d.append(i)
            else:
                i += 1

        return d[0]


def fast_c(a, n, z):
    result = 1
    x = a % z
    while n > 0:
        if (n % 2) == 1:
            result = (result * x) % z
        x = (x ** 2) % z
        if (n % 2) == 1:
            n = int((n - 1) / 2)
        else:
            n = n / 2
    return result


def encrypt():
    rsa = RSA()
    p = rsa.make_p()
    q = rsa.make_q()
    [n, pi] = rsa.make_key(p, q)
    e = rsa.find_e(pi)
    d = rsa.find_d(e, pi)
    mesg = input('Write a message to Encrypt: ')
    log = "Encryping '" + mesg + "'"
    print_mesg(log)

    code = [ord(char) for char in mesg]
    crypto = []
    for m in code:
        c = fast_c(m, e, n)
        crypto.append(c)
    print('Public key: ' + str([e, n]))
    print('Private key: ' + str([d, n]))
    print('Encrypted message is', crypto)
    print()


def decrypt():
    n1 = None
    n2 = None
    while n1 is None or n2 is None or (n1 != n2):
        e, n1 = map(int, input('Enter a Public Key: ').split(','))
        d, n2 = map(int, input('Enter a Private Key: ').split(','))

    pw = list(map(int, input('Write a message to Decrypt: ').split(',')))
    mesg = ''.join([chr(fast_c(c, d, n1)) for c in pw])
    print_mesg('Decrypting')
    print("The message was '" + mesg + "'")
    print()


def print_mesg(msg):
    print(msg, end="")
    for i in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(0.5)
    print()


def main():
    option = -1
    while option != '0':
        print("<Option>")
        print("1. Encrypt")
        print("2. Decrypt")
        print("Enter '0' to exit")
        option = input('Enter Option: ')
        if option == '1':
            encrypt()
        elif option == '2':
            decrypt()
        elif option == '0':
            print('End this Program')
        else:
            print('Wrong Option! Try again')


if __name__ == '__main__':
    main()
