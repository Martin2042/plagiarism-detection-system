from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request("http://127.0.0.1:8000/myapp/test_doc")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "html.parser")

html_text = soup.get_text()
print(html_text.strip())
f = open("html_text.txt", "w")         # Creating html_text.txt File

for line in html_text:
	f.write(line)

f.close()