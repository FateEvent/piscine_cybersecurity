import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_if_exists(data, key):
	if key in data:
		return data[key]
	return None

def get_image(path: str) -> Image:
	try:
		image = Image.open(path)
		return image
	except:
		print("Could not open the image!")

def get_exif(image: Image) -> Image.Exif:
	data = dict()
	exif_data = getattr(image, '_getexif', lambda: None)()
	if exif_data:
		for key, value in exif_data.items():
			tag = TAGS.get(key, key)
			if tag == "GPSInfo":
				gps_data = dict()
				for i in value:
					gps_decoded = GPSTAGS.get(i, i)
					gps_data[gps_decoded] = value[i]
				data[tag] = gps_data
			else:
				print(f"{tag} : {value}")
				data[tag] = value
		return data
			
def convert_to_degrees(value) -> float:
	decimal = value[0]
	minute = value[1] / 60.0
	second = value[2] / 3600.0
	return decimal + (minute / 60.0) + (second / 3600)

def print_gps_info(exif: Image.Exif):
	latitude = 0.0
	longitude = 0.0
	gps_info = exif["GPSInfo"]
	gps_lat = get_if_exists(gps_info, "GPSLatitude")
	gps_lat_ref = get_if_exists(gps_info, "GPSLatitudeRef")
	gps_long = get_if_exists(gps_info, "GPSLongitude")
	gps_long_ref = get_if_exists(gps_info, "GPSLongitudeRef")
	if gps_lat and gps_lat_ref and gps_long and gps_long_ref:
		latitude = convert_to_degrees(gps_lat)
		longitude = convert_to_degrees(gps_long)
		if gps_lat_ref != "N":
			latitude *= -1
		if gps_long_ref != "E":
			longitude *= -1
		print(f"Latitude : {latitude}\nLongitude : {longitude}")

def main():
	for file in sys.argv[1:]:
		print(f"Metadata for {file} :")
		image = get_image(file)
		if image:
			print(f"Size : {os.path.getsize(file)} bytes")
			print(f"Height : {image.height}")
			print(f"Width : {image.width}")
			print(f"Format : {image.format}")
			print(f"Mode : {image.mode}")
			print(f"Is animated : {getattr(image, 'is_animated', False)}")
			print(f"Frames : {getattr(image, 'n_frames', False)}")
			exif = get_exif(image)
			if exif:
				if "GPSInfo" in exif:
					print_gps_info(exif)
			else:
				print("No EXIF data !")
		print()


if (__name__ == "__main__"):
	if len(sys.argv) == 1:
		sys.exit("Usage: python3 ./scorpion.py FILE1 [FILE2 ...]")
	main()
