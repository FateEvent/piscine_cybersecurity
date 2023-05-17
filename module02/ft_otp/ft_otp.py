import hmac, base64, struct, hashlib, time

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    #decoding our key
    msg = struct.pack(">Q", intervals_no)
    #conversions between Python values and C structs represente
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = o = h[-1] & 15
    #Generate a hash using both of these. Hashing algorithm is HMAC
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    #unpacking
    return h

def get_totp_token(secret):
    #ensuring to give the same otp for 30 seconds
    x =str(get_hotp_token(secret,intervals_no=int(time.time())//30))
    #adding 0 in the beginning till OTP has 6 digits
    while len(x)!=6:
        x+='0'
    return x
	
#base64 encoded key
secret = 'abc123242561acdd212aaa2a1273672369376937694736209987402707430708'
b52 = str(base64.b32encode(bytearray.fromhex(secret.upper())))
print(b52)
b51 = b52[2:len(b52) - 1]
print(b51)
print(get_totp_token(b51))

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
