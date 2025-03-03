from bs4 import BeautifulSoup as BS
import requests as req
from .models import NewsArticle
from datetime import datetime
import yfinance as yf
from  .models import NewsArticle , Count

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


import requests as req
from bs4 import BeautifulSoup as BS

def get_stock_data(ticker, class_name="Yfwt5"):
    url = f'https://www.google.com/finance/quote/{ticker}?hl=en'
    response = req.get(url)

    if response.status_code != 200:
        return [f"{ticker} was not found"]

    html = BS(response.text, "html.parser")
    elements = html.find_all("div", class_=class_name)

    news = [e.text.strip() for e in elements] if elements else ["neutral"]

    return news


#stock_data , news =  get_stock_data('AAPL:NASDAQ')
#  print(type( elements[0]))
      


def save_news_with_sentiment(content, sentiment,  real_price_change):
    article = NewsArticle.objects.create(
        content=content,
        sentiment=sentiment,
        real_price_change= real_price_change,
        scraped_at=datetime.now()
    )

def   save_count(count):
    obj = Count.objects.first()
    obj.count   =   obj.count +1
    obj.save()
    print(obj)





def get_price_change(stock_symbol):
  
    # Fetch stock data
    data = yf.download(stock_symbol,period ="2d")

    yesterday_price = data['Close'].iloc[-2].item()  # Convert Series to scalar
    today_price = data['Close'].iloc[-1].item()  # Convert Series to scalar

    # Calculate price change indicator
    return 1 if today_price >= yesterday_price else 0



def   auto_retrain():
    count = NewsArticle.objects.count()
    print("Total count:", count)
    return count