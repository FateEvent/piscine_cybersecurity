import os
import sys
import time
import struct
import hmac
import hashlib
import config
from cryptography.fernet import Fernet

def is_hex(key: str) -> int:
    try:
        value = int(key, 16)
    except ValueError:
        return 1
    return 0

def encrypt_secret(secret: bytes):
    try:
        with open('ft_otp.key', "wb") as file:
            file.write(Fernet(config.ENCRYPT_KEY).encrypt(secret))
    except Exception as e:
        sys.exit(f"Error: Cannot write ft_otp.key! ({e})")

def decrypt_secret() -> bytes:
    try:
        with open(sys.argv[2], 'rb') as file:
            secret = file.read()
        return Fernet(config.ENCRYPT_KEY).decrypt(secret)
    except Exception as e:
        sys.exit(f"Error: Cannot read secret file! ({e})")

def get_secret_len() -> int:
    try:
        with open(sys.argv[2], 'rb') as file:
            secret = file.read()
        return len(secret)
    except Exception as e:
        sys.exit(f"Error: Cannot read secret file! ({e})")

def get_secret_str() -> str:
    try:
        with open(sys.argv[2], 'rb') as file:
            return file.read().decode('utf-8')
    except Exception:
        sys.exit("Error: Cannot read secret file!")

def otp_generator() -> str:
    secret = decrypt_secret()
    intervals = int(time.time() / 30)
    intervals_packed = struct.pack('>Q', intervals)
    hmac_hash = hmac.new(secret, intervals_packed, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated_hash = hmac_hash[offset:offset+4]
    otp = struct.unpack('>I', truncated_hash)[0] & 0x7FFFFFFF
    otp_str = str(otp % 10**6).rjust(6, '0')
    return otp_str

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
        sys.exit("Usage: python3 ./ft_otp.py [-gk] secret|key")
    elif sys.argv[1] == '-g' and (get_secret_len() < 64 or is_hex(get_secret_str())):
        sys.exit("Error: key must be at least 64 hexadecimal characters.")
    main()

# import hmac, base64, struct, hashlib, time

# def get_hotp_token(secret, intervals_no):
#     key = base64.b32decode(secret, True)
#     #decoding our key
#     msg = struct.pack(">Q", intervals_no)
#     #conversions between Python values and C structs represente
#     h = hmac.new(key, msg, hashlib.sha1).digest()
#     o = o = h[-1] & 15
#     #Generate a hash using both of these. Hashing algorithm is HMAC
#     h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
#     #unpacking
#     return h

# def get_totp_token(secret):
#     #ensuring to give the same otp for 30 seconds
#     x =str(get_hotp_token(secret,intervals_no=int(time.time())//30))
#     #adding 0 in the beginning till OTP has 6 digits
#     while len(x)!=6:
#         x+='0'
#     return x
	
# #base64 encoded key
# secret = 'abc123242561acdd212aaa2a1273672369376937694736209987402707430708'
# b52 = str(base64.b32encode(bytearray.fromhex(secret.upper())))
# print(b52)
# b51 = b52[2:len(b52) - 1]
# print(b51)
# print(get_totp_token(b51))

# import os
# import sys
# import hmac
# import codecs
# import time
# import struct
# import base64

# def encrypt_secret(secret: int):
# 	with open('ft_otp.key', 'w') as file:
# 		file.write(str(secret))
# 		file.close()

# def main():
# 	intervals = int(time.time() / 30)
# 	intervals_packed = struct.pack('>Q', intervals)
# 	f = open("hex.txt", "r")
# 	hex_string = f.readline()
# 	try:
# 		value = int(hex_string, 16)
# 	except ValueError:
# 		sys.exit("error: the string is not a valid hexadecimal string")
# 	if len(hex_string) >= 64:
# 		# hmac_obj = hmac.new(hex_string.encode(), intervals_packed.encode(), 'sha1')
# 		# msg_digest = hmac_obj.digest()
# 		hex_data = base64.b32encode(bytearray.fromhex(hex_string))
# 		msg_digest = hmac.digest(base64.b32decode(hex_data), intervals_packed, 'sha1')
# 		offset = msg_digest[-1] & 0xf
# 		bin_code = (msg_digest[offset] & 0x7f) << 24 \
# 			| (msg_digest[offset + 1] & 0xff) << 16 \
# 			| (msg_digest[offset + 2] & 0xff) <<  8 \
# 			| (msg_digest[offset + 3] & 0xff)
# 		hashing = bin_code % 10**6
# 		print(hashing)
# 		encrypt_secret(hashing)
# 	else:
# 		sys.exit("error: key must be made up of at least 64 hexadecimal characters.")

# if (__name__ == "__main__"):
# 	if len(sys.argv) != 3 or sys.argv[1] != '-k' and sys.argv[1] != '-g':
# 		sys.exit("Usage: python3 ft_otp.py FLAG[-gk] FILE")
# 	main()
