import os
import sys
import time
import struct
import hmac
import hashlib
from cryptography.fernet import Fernet

def is_hex(key: str) -> int:
	try:
		value = int(key, 16)
	except ValueError:
		return 1
	return 0

def encrypt_secret(secret: bytes):
	if os.path.isfile('config.key'):
		try:
			with open('config.key', "rb") as config:
				try:
					with open('ft_otp.key', "wb") as file:
						f = config.read()
						file.write(Fernet(f).encrypt(secret))
				except Exception as e:
					sys.exit(f"error: cannot create ft_otp.key! ({e})")
		except Exception as e:
			sys.exit(f"error: cannot read config.key! ({e})")
	else:
		try:
			key = Fernet.generate_key()
			with open('config.key', "wb") as config:
				config.write(key)
				config.close()
		except Exception as e:
			sys.exit(f"error: cannot create config.key! ({e})")

def decrypt_secret() -> bytes:
	try:
		with open('config.key', 'rb') as config:
			try:
				f = config.read()
				with open(sys.argv[2], 'rb') as file:
					secret = file.read()
				return Fernet(f).decrypt(secret)
			except Exception as e:
				sys.exit(f"error: cannot read config.key! ({e})")
	except Exception as e:
		sys.exit(f"error: cannot read the secret file! ({e})")

def get_secret_len() -> int:
	try:
		with open(sys.argv[2], 'rb') as file:
			secret = file.read()
		length = len(secret)
		if (length % 2):
			exit("error: hex decoding of secret key failed")
		return length
	except Exception as e:
		sys.exit(f"error: cannot read the secret file! ({e})")

def get_secret_str() -> str:
	try:
		with open(sys.argv[2], 'rb') as file:
			return file.read().decode('utf-8')
	except Exception:
		sys.exit("error: cannot read the secret file!")

def otp_generator() -> str:
	secret = decrypt_secret().decode('utf-8')
	key = bytes.fromhex(secret)
	intervals = struct.pack('>Q', int(time.time() // 30))
	hmac_hash = hmac.new(key, intervals, hashlib.sha1).digest()
	offset = hmac_hash[-1] & 15
	truncated_hash = (struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7fffffff) % 1000000
	otp = str(truncated_hash)
	return otp.rjust(6, '0')

def main():
	if (sys.argv[1] == '-g'):
		key = get_secret_str()
		encrypt_secret(key.encode())
		print("ft_otp.key file created successfully. You can now generate OTPs using python3 ft_otp.py -k ft_otp.key")
	elif (sys.argv[1] == '-k'):
		otp = otp_generator()
		print(f"Your password is : {otp[:3]} {otp[3:]}")

if (__name__ == "__main__"):
	if len(sys.argv) != 3 or (sys.argv[1] != '-k' and sys.argv[1] != '-g'):
		sys.exit("usage: python3 ./ft_otp.py [-gk] secret|key")
	elif sys.argv[1] == '-g' and (get_secret_len() < 64 or is_hex(get_secret_str())):
		sys.exit("error: key must be at least 64 hexadecimal characters.")
	main()
