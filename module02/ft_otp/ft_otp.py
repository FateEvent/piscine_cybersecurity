import os
import sys
import hmac
import codecs
import time

def encrypt_secret(secret: int):
	with open('ft_otp.key', 'w') as file:
		file.write(str(secret))
		file.close()

def main():
	obj = time.gmtime(0)
	epoch = time.asctime(obj)
	print("The epoch is:",epoch)
	curr_time = round(time.time()*1000)
	print("Milliseconds since epoch:",curr_time)
	f = open("hex.txt", "r")
	hex_string = f.readline()
	try:
		value = int(hex_string, 16)
	except ValueError:
		sys.exit("error: the string is not a valid hexadecimal string")
	if len(hex_string) >= 64:
		if len(hex_string) % 2 == 0:
			hex_data = codecs.decode(hex_string, 'hex')
			hmac_obj = hmac.new(hex_data, str(curr_time).encode(), 'sha256')
			msg_digest = hmac_obj.digest()
			print(msg_digest)
			offset = msg_digest[len(msg_digest) - 1] & 0xf
			bin_code = (msg_digest[offset] & 0x7f) << 24 \
				| (msg_digest[offset + 1] & 0xff) << 16 \
				| (msg_digest[offset + 2] & 0xff) <<  8 \
				| (msg_digest[offset + 3] & 0xff)
			print(bin_code)
			hashing = bin_code % 10**6
			print(hashing)
			encrypt_secret(hashing)
		else:
			sys.exit("error: the hexadecimal string must have an even number of digits.")
	else:
		sys.exit("error: key must be 64 hexadecimal characters.")



	# for file in sys.argv[1:]:
	# 	print(f"Metadata for {file} :")
	# 	image = get_image(file)
	# 	if image:
	# 		print(f"Size : {os.path.getsize(file)} bytes")
	# 		print(f"Height : {image.height}")
	# 		print(f"Width : {image.width}")
	# 		print(f"Format : {image.format}")
	# 		print(f"Mode : {image.mode}")
	# 		print(f"Is animated : {getattr(image, 'is_animated', False)}")
	# 		print(f"Frames : {getattr(image, 'n_frames', False)}")
	# 		exif = get_exif(image)
	# 		if exif:
	# 			if "GPSInfo" in exif:
	# 				print_gps_info(exif)
	# 		else:
	# 			print("No EXIF data !")
	# 	print()


if (__name__ == "__main__"):
	# if len(sys.argv) == 1 or len(sys.argv) > 2 \
		# or sys.argv[1] != '-k' and sys.argv[1] != '-g':
	if sys.argv[1] != '-k' and sys.argv[1] != '-g':
		print(sys.argv[1])
		sys.exit("Usage: python3 ft_otp.py FLAG FILE")
	main()
