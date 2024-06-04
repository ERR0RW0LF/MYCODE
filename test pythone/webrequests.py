from pprint import pprint
from requests import get
from bs4 import BeautifulSoup

def get_page(url):
    response = get(url)
    return response.text

def get_links(page):
    soup = BeautifulSoup(page, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def main():
    url = 'https://de.wikipedia.org/wiki/Gentechnik'
    page = get_page(url)
    links = get_links(page)
    for link in links:
        print(link)

if __name__ == '__main__':
    main()