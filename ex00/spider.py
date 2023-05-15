import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrap_images(link: str, images: set) -> int:
	count = 0
	multiple = ''
	accepted_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
	print("Crawling {} ...".format(sys.argv[1]))
	response = requests.get(link)
	soup = BeautifulSoup(response.content, 'html.parser')
	for img in soup.find_all('img'):
		if img['src']:
			img_url = urljoin(response.url, img['src'])
			img_filename = os.path.basename(img_url)
			img_extension = os.path.splitext(img_filename)[1]
			if img_extension.lower() in accepted_extensions:
				count += 1
				if count > 1:
					multiple = 's'
				print("Found {} image{}".format(count, multiple), end='\r', flush=True)
				images.add(img_url)
	print('')


def scrap_links(links: set, params: list, max_depth: int, images: set, base_url: str) -> int:
	params["depth"] += 1
	multiple = ''
	response = requests.get(base_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	parsed_uri = urlparse(response.url)
	domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
	for link in soup.find_all('a'):
		if link['href']:
			link_url = urljoin(response.url, link['href'])
			link_parsed_uri = urlparse(link_url)
			link_domain = '{uri.scheme}://{uri.netloc}'.format(uri=link_parsed_uri)
			if domain == link_domain and link_url != domain:
				params["count"] += 1
				if params["count"] > 1:
					multiple = 's'
				links.add(link_url)
				if params["depth"] <= max_depth:
					scrap_links(links, params, max_depth, images, link_url)


def main() -> int:
	params = {"depth": 0, "count": 0}
	links = set()
	images = set()
	scrap_links(links, params, 2, images, sys.argv[1])
	for link in links:
		scrap_images(link, images)
		print(link)
	for image in images:
		img_filename = os.path.basename(image)
		with open(os.path.join("data", img_filename), "wb") as file:
			file.write(requests.get(image).content)


if (__name__ == "__main__"):
	if len(sys.argv) == 1 or len(sys.argv) > 3:
		print("Usage: python3 spider.py [-rlpS] URL")
	else:
		if not os.path.exists("data"):
			os.makedirs("data")
		main()
