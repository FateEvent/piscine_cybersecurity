#include <iostream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <curl/curl.h>
#include <regex>

void	find_image(std::string buffer)
{
	std::string	image;
	std::regex	img_regex("<img[^>]*src=\"([^\"]*)\"[^>]*>");

	auto	img_begin = std::sregex_iterator(buffer.begin(), buffer.end(), img_regex);
	auto	img_end = std::sregex_iterator();

	for (std::sregex_iterator i = img_begin; i != img_end; ++i)
	{
		std::smatch	match = *i;
		std::string	match_str = match[1].str();
		std::cout << match_str << std::endl;
	}
}

size_t append_data(void *ptr, size_t size, size_t nmemb, std::string *buffer)
{
	size_t totalSize = size * nmemb;
	buffer->append(*(static_cast<std::string *>(ptr)), totalSize);
	std::cout << *buffer << std::endl;
	return (totalSize);
}

size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream)
{
	size_t written;
	written = fwrite(ptr, size, nmemb, stream);
	return written;
}

void	clauncher()
{
	CURL		*curl;
	CURLcode	res;
	FILE		*filename;
	
	curl_global_init(CURL_GLOBAL_ALL);
	curl = curl_easy_init();
	std::string	outfilename = "test.html";
	if	(curl) {
		std::string	buffer;
		filename = fopen(outfilename.c_str(), "wb");

		curl_easy_setopt(curl, CURLOPT_URL, "https://curl.se/libcurl/c/CURLOPT_URL.html");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, filename);

		res = curl_easy_perform(curl);
		curl_easy_cleanup(curl);
		fclose(filename);
	}
}

int main(int ac, char *av[])
{
	(void)ac;
	(void)av;

	clauncher();
}