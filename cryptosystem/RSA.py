# 이산 수학 5강 참조하기

import random
from time import sleep
import sys

class Euclide:
	# 최대공약수를 구하는 함수
	def gcd(a, b):
		while (b != 0):
			temp = a % b
			a = b
			b = temp
		return abs(a)

	# 서로소를 구하는 함수
	def coprime(self,a,b):
		if (self.gcd(a,b)==1):
			return True
		else:
			return False

class RSA:
	# 7,000 ~ 8,000 사이의 임의의 소수를 출력하는 함수
	def make_p():
		list_p = set({})
		for n in range(7000,8000):
			state = True
			for i in range(2,n):
				if(n%i == 0):
					state = False
			if (state):
				list_p.add(n)
		list_p = list(list_p)
		p = list_p[random.randrange(0,len(list_p))]
		return p

	# 9,000 ~ 10,000 사이의 임의의 소수를 출력하는 함수
	def make_q():
		list_q = set({})
		for n in range(9000,10000):
			state = True
			for i in range(2,n):
				if(n%i == 0):
					state = False
			if (state):
				list_q.add(n)
		list_q = list(list_q)
		q= list_q[random.randrange(0,len(list_q))]
		return q

	# n과 pi를 계산하는 함수
	def make_key(p,q):
		n = p*q
		pi = (p-1)*(q-1)
		return [n, pi]

	# pi와 서로소이면서 pi보다 작은 수들을 모두 구해서 그 중 임의의 값을 e로 지정하는 함수
	def find_e(pi):
		list_e = set({})
		for i in range(2,pi):
			if (Euclide.coprime(Euclide,i,pi)):
				list_e.add(i)
		list_e = list(list_e)
		e = list_e[random.randrange(0,len(list_e))]
		return e

	# 
	def find_d(e,pi):
		d=[]
		i=1

		while (len(d)==0):
			if ((i*e)%pi==1):
				d.append(i)
			else:
				i+=1

		return d[0]

def fast_c(a, n, z):
	result = 1
	x = a % z
	while n > 0:
		if (n%2) == 1:
			result = (result*x) % z
		x = (x**2) % z
		if (n % 2) == 1:
			n = int((n-1)/2)
		else:
			n = n/2
	return result

def encrypt(n,e):
	mesg = input('Write a message to Encrypt: ')
	log = "Encryping '" + mesg + "'"
	print_mesg(log)

	code = [ord(char) for char in mesg]
	crypto = []
	for m in code:
		c=fast_c(m, e, n)
		crypto.append(c)
	print('Encrypted message is', crypto)

def decrypt(n,d):
	pw = list(map(int, input('Write a message to Decrypt: ').split(',')))
	mesg = ''.join([chr(fast_c(c,d,n)) for c in pw])
	print_mesg('Decrypting')
	print("The message was '" + mesg + "'")

def print_mesg(msg):
	print(msg, end="")
	for i in range(5):
		sys.stdout.write(".")
		sys.stdout.flush()
		sleep(0.5)
	print()

def main():
	p = 7151
	q = 9587
	n = 68556637
	pi = 68539900
	e = 21110703
	d = 38951467

	print("<Option>")
	print("1. Encrypt")
	print("2. Decrypt")

	option = input('Enter Option: ')
	if (option=='1'):
		encrypt(n,e)
	elif (option == '2'):
		decrypt(n,d)
	else:
		print('Wrong Option! Try again')
		main()

if __name__ == '__main__':
	main()



