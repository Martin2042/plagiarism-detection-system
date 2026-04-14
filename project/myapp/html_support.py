from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
#import re

def get_html_text(url):
	try:
		req = Request(url)#"http://127.0.0.1:8000/myapp/test_doc")
		html_page = urlopen(req)
		soup = BeautifulSoup(html_page, "html.parser")
		html_text = soup.get_text()
		#print(html_text.strip())
		return html_text.strip()
	except:
		return 'SERVER NOT FOUND'

if __name__ == '__main__':

		html_text = get_html_text('http://127.0.0.1:8000/myapp/test_doc')
		print(html_text)
