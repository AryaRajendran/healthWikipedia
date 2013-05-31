from bs4 import BeautifulSoup

f = open("article.htm", "r")
lines = f.read()

soup = BeautifulSoup(lines)
text = soup.get_text()

print text
