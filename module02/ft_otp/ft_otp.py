import os
import sys
import string
import hmac
from binascii import unhexlify
import time

def main():
	obj = time.gmtime(0)
	epoch = time.asctime(obj)
	print("The epoch is:",epoch)
	curr_time = round(time.time()*1000)
	print("Milliseconds since epoch:",curr_time)
	f = open("hex.txt", "r")
	string = f.read()
	if all(c in string.hexdigits for c in string): #and len(string) >= 64:
		print(f.read())
	print(s)
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
