from bs4 import BeautifulSoup as BS
import requests as req

def scrape_latest_news():
    url = "https://www.businesstoday.in/latest/economy"
    webpage = req.get(url)
    trav = BS(webpage.content, "html.parser")
    
    strings = []
    for link in trav.find_all('a'):
        if (str(type(link.string)) == "<class 'bs4.element.NavigableString'>" and len(link.string) > 35):
            strings.append(link.string)
    
    return strings




