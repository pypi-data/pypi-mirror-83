import random
class Crypter:

	def encrypt(text, password):
		if type(password) is str:
			psw = 0
			for x in range(len(password)):
				psw += ord(password[-(x + 1)]) * (x + 1)

		elif type(password) is int:
			psw = password
		
		else:
			return None

		output_text = ''

		for x in text:
			output_text += chr(ord(x) + (psw % len(text)) + 1)
			num = int(len(str(psw)) / ord(x))
			psw += psw % len(text) + ord(x) + len(str(psw)) + int(str(psw)[-1]) + int(str(psw)[0]) + int(str(psw)[num])

		return output_text

	def decrypt(text, password):
		if type(password) is str:
			psw = 0
			for x in range(len(password)):
				psw += ord(password[-(x + 1)]) * (x + 1)

		elif type(password) is int:
			psw = password
		
		else:
			return None

		output_text = ''

		for x in text:
			output_text += chr(ord(x) - ((psw % len(text)) + 1))
			num = int(len(str(psw)) / (ord(x) - ((psw % len(text)) + 1)))
			psw += psw % len(text) + (ord(x) - ((psw % len(text)) + 1)) + len(str(psw)) + int(str(psw)[-1]) + int(str(psw)[0]) + int(str(psw)[num])

		return output_text

	def encrypt_caesar_cipher(text, password):
		if type(password) is str:
			psw = 0
			for x in range(len(password)):
				psw += ord(password[-(x + 1)]) * (x + 1)

		elif type(password) is int:
			psw = password
		
		else:
			return None

		output_text = ''

		for x in text:
			output_text += chr(ord(x) + psw)

		return output_text

	def decrypt_caesar_cipher(text, password):
		if type(password) is str:
			psw = 0
			for x in range(len(password)):
				psw += ord(password[-(x + 1)]) * (x + 1)

		elif type(password) is int:
			psw = password
		
		else:
			return None

		output_text = ''

		for x in text:
			output_text += chr(ord(x) - psw)

		return output_text

class DHA:

	def p_g(p_n, g_n):

		p = ''
		g = ''

		for x in range(p_n):
			p += str(random.randint(0,9))

		p = int(p)

		for x in range(g_n):
			g += str(random.randint(0,9))

		g = int(g)

		return p, g

	def get_n(p,g,num):

		return (g ** num) % p

	def key(p,num,n):

		return (n**num) % p