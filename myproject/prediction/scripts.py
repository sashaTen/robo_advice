from bs4 import BeautifulSoup as BS
import requests as req

def scrape_latest_news(ticker):
    url = "https://www.businesstoday.in/latest/economy"
    webpage = req.get(url)
    trav = BS(webpage.content, "html.parser")
    
    strings = []
    for link in trav.find_all('a'):
        if (str(type(link.string)) == "<class 'bs4.element.NavigableString'>" and len(link.string) > 35):
            strings.append(link.string)
    
    
    return strings




def filter_strings(strings_array, string):
    return [s for s in strings_array if string in s]



def get_stock_data(ticker , class_name = "Yfwt5"):
    url = f'https://www.google.com/finance/quote/{ticker}?hl=en'
    response = req.get(url)
    soup = BS(response.content, 'html.parser')
    html = BS(response.text, "html.parser")
    stock_data = {}
    stock_data['title'] = soup.find('div', class_='zzDege').text
    stock_data['price'] = soup.find('div', class_='AHmHk').text
    stock_data['price_change'] = soup.find('div', class_='JwB6zf').text
    elements = html.find_all("div", class_=class_name)
    news =  []
    for e in elements:
        news.append((e.text.strip()))
    
    return stock_data , news
strings = []
stock_data , news =  get_stock_data('AAPL:NASDAQ')
#  print(type( elements[0]))
      