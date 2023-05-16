import os
import sys
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrap_links(links: set, depth: int, max_depth: int, base_url: str, followed_links: set):
	if depth >= max_depth:
		return
	response = requests.get(base_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	parsed_uri = urlparse(response.url)
	domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
	for link in soup.find_all('a'):
		if link.has_attr('href'):
			link_url = urljoin(domain, link['href'])
			link_parsed_uri = urlparse(link_url)
			link_domain = '{uri.scheme}://{uri.netloc}'.format(uri=link_parsed_uri)
			terminal_width = shutil.get_terminal_size().columns
			if domain == link_domain and link_url != domain:
				output_link = str("\r\033[KScrapped : {}".format(link_url))
				output_total = str("(Total {})".format(len(links)))
				if len(output_link + output_total) > terminal_width:
					output_link = output_link[:terminal_width - len(output_total) - 3] + "..."
				print("{} {}".format(output_link, output_total), end='', flush=True)
				links.add(link_url)
				if link_url not in followed_links:
					followed_links.add(link_url)
					scrap_links(links, depth + 1, max_depth, link_url, followed_links)

def scrap_images(link: str, saved_images: set, path: str):
	count = 0
	downloaded = 0
	valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
	print("\r\033[KScrapping images from '{}' ...".format(link), end='')
	response = requests.get(link)
	soup = BeautifulSoup(response.content, 'html.parser')
	for img in soup.find_all('img'):
		if img.has_attr('src'):
			img_url = urljoin(response.url, img['src'])
			img_filename = os.path.basename(img_url)
			img_extension = os.path.splitext(img_filename)[1]
			if img_extension.lower() in valid_extensions:
				img_path = os.path.join(path, urlparse(img_url).hostname, os.path.dirname(urlparse(img_url).path)[1:])
				img_full_path = os.path.join(img_path, img_filename)
				if img_full_path not in saved_images:
					downloaded += 1
					saved_images.add(img_full_path)
					os.makedirs(img_path, exist_ok=True)
					with open(img_full_path, "wb") as file:
						file.write(requests.get(img_url).content)
				count += 1
	print(" Found {} images, {} downloaded.".format(count, downloaded))

def main(max_depth: int, path: str, recursive: bool, target_uri: str):
	print("Crawling...")
	links = set()
	followed_links = set()
	saved_images = set()
	if (recursive):
		followed_links.add(target_uri)
		links.add(target_uri)
		scrap_links(links, 0, max_depth, target_uri, followed_links)
		print("\r\033[KScrapped {} links".format(len(links)), flush=True)
		for link in links:
			scrap_images(link, saved_images, path)
	else:
		scrap_images(target_uri, saved_images, path)

if (__name__ == "__main__"):
	max_depth = 5
	max_depth_changed = False
	max_depth_pos = 0
	path = "./data/"
	recursive = False
	target_uri = ''
	if len(sys.argv) == 1 or len(sys.argv) > 7:
		sys.exit("Usage: python3 spider.py [-rlpS] URL")
	else:
		if len(sys.argv) > 2:
			for i in range(1, len(sys.argv)):
				if sys.argv[i][0] == '-' and len(sys.argv[i]) == 2 and i != len(sys.argv) - 1:
					for j in range (1, len(sys.argv[i])):
						if sys.argv[i][j] == 'r':
							recursive = True
						elif sys.argv[i][j] == 'l':
							if i <= len(sys.argv) and sys.argv[i + 1].isdigit():
								max_depth = int(sys.argv[i + 1])
								max_depth_changed = True
								max_depth_pos = int(i)
							else:
								sys.exit("Usage: python3 spider.py [-rlpS] URL")
						elif sys.argv[i][j] == 'p':
							if i <= len(sys.argv):
								path = sys.argv[i + 1]
							else:
								sys.exit("Usage: python3 spider.py [-rlpS] URL")
						else:
							sys.exit("Usage: python3 spider.py [-rlpS] URL")
				elif i == len(sys.argv) - 1:
					target_uri = sys.argv[i]
				elif max_depth_changed and i == max_depth_pos + 1:
					continue
				else:
					sys.exit("Usage: python3 spider.py [-rlpS] URL")
		else:
			target_uri = sys.argv[1]
		if not (target_uri.startswith("http://") or target_uri.startswith("https://")) or (max_depth_changed == True and recursive == False):
			sys.exit("Usage: python3 spider.py [-rlpS] URL")
		if not os.path.exists(path):
			os.makedirs(path)
		main(max_depth, path, recursive, target_uri)