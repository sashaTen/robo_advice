from django.shortcuts import render
from .scripts  import scrape_latest_news , filter_strings ,get_stock_data
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .pipeline  import   sentiment_analysis_pipeline
from zenml.client import Client
import yfinance as yf
import io
import base64
import matplotlib.pyplot as plt



def hello_world(request):
  return render(request ,   'hello.html')



def prediction_result(request):
    vectorize_artifact = Client().get_artifact_version("9f42ba36-0287-4b1e-aaa9-46fbb54d45f4")
    vectorizer = vectorize_artifact .load()
    model_artifact = Client().get_artifact_version("62efc70b-2133-497d-94f5-cfb4ff03f4fa")
    model = model_artifact.load()
    if request.method == "POST":
        ticker = request.POST.get("ticker")  # Get the text input from form
        company = request.POST.get("company")
        strings = scrape_latest_news( ticker)
        news =  get_stock_data(f"{ticker}:NASDAQ")
        company_news = filter_strings(strings ,    company)
        for  i in news :
         company_news .append(i)
        if company_news:
          prediction =  model.predict(vectorizer.transform(company_news))
          return HttpResponse(f"news  found: {company_news},     the  predicted  sentiment  :     {prediction} ")  # Simple response for now
        else   :
          return HttpResponse('news related to stock are  not    found ') 
        

    return HttpResponse("Invalid request")

# https://raw.githubusercontent.com/sashaTen/investment_app/refs/heads/main/invest/S%26P500data/clusters_df.csv



def testing(request):
    chart = None  # Default to None if no data is available

    if request.method == "POST":
        ticker = request.POST.get("ticker")  # Get ticker from form input

        if ticker:
            # Fetch stock data
            data = yf.download(ticker, start="2024-01-01", end="2025-01-01")

            if not data.empty:
                # Create a plot
                plt.figure(figsize=(10, 5))
                plt.plot(data.index, data['Close'], label=f"{ticker} Closing Price")
                plt.xlabel("Date")
                plt.ylabel("Price (USD)")
                plt.title(f"{ticker} Stock Closing Prices (2024)")
                plt.legend()
                plt.grid()

                # Convert plot to base64 image
                buffer = io.BytesIO()
                plt.savefig(buffer, format="png")
                buffer.seek(0)
                chart = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()

    return render(request, "check_data.html", {"chart": chart})



#   python  manage.py runserver     python manage.py migrate