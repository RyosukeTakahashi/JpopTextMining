from bs4 import BeautifulSoup as bs
import urllib.request as urlrequest

def generate_soup(url): 
    html = urlrequest.urlopen(url).read()
    print(html)
    soup = bs(html, "lxml")
    return soup

url = "https://www.joysound.com/web/search/song/121447"
soup = generate_soup(url)

print(soup.find_all("p", class_="ng-binding"))
print(soup.find_all("p"))

 