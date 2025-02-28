from django.shortcuts import render
from .scripts  import scrape_latest_news , filter_strings ,get_stock_data , save_news_with_sentiment ,get_price_change
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
  
  artifact_log = Client().get_artifact_version("9e8d22cf-4df8-418d-a9c3-4244af505f36")
  data_log = artifact_log.load()

  artifact_nb = Client().get_artifact_version("8e81134c-7c28-49e1-ac13-f33bab935b23")
  data_nb = artifact_nb.load()

  artifactTree = Client().get_artifact_version("51404133-bb64-4f1a-adaa-ac3c8fa94cb9")
  dataTree = artifactTree.load()

  print('   log regression    accuracy ,  '   ,data_log)
  print('  nb  accuracy ',   data_nb )
  print(   '    tree  accuracy   ,    ' ,    dataTree)
  return render(request ,  'hello.html')



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
          company_news_single_str   =  " ".join(company_news)
          average_sentiment =round(sum(prediction) / len(prediction))
        
          save_news_with_sentiment(company_news_single_str  ,  average_sentiment  ,1)
          return HttpResponse(f"news  found: {company_news_single_str },     the  predicted  sentiment  :     {prediction} ")  # Simple response for now
        else   :
          return HttpResponse('news related to stock are  not    found ') 
        

    return HttpResponse("Invalid request")

# https://raw.githubusercontent.com/sashaTen/investment_app/refs/heads/main/invest/S%26P500data/clusters_df.csv



def testing(request):
  

    return HttpResponse('test')



#   python  manage.py runserver     python manage.py migrate