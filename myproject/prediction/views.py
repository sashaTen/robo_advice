from django.shortcuts import render
from .scripts  import scrape_latest_news , filter_strings ,get_stock_data , save_news_with_sentiment , get_price_change , auto_retrain
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .pipeline  import   sentiment_analysis_pipeline
from zenml.client import Client
from   .data_tests   import  test_data
from .models  import NewsArticle


def hello_world(request):
 
  
       
  return render(request ,  'hello.html')



def prediction_result(request):
    
    vectorize_artifact = Client().get_artifact_version("9f42ba36-0287-4b1e-aaa9-46fbb54d45f4")
    vectorizer = vectorize_artifact .load()
    model_artifact = Client().get_artifact_version("0eef78a6-cfbb-411b-b397-20fe4f07b997")
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
          price_change =  get_price_change(ticker)
          save_news_with_sentiment(company_news_single_str  ,  average_sentiment  ,price_change)
          if   test_data(NewsArticle) == 1:
               auto_retrain(3,NewsArticle)
          return HttpResponse(f"news  found: {company_news_single_str },     the  predicted  sentiment  :     {prediction} ")  # Simple response for now
        else   :
          return HttpResponse('news related to stock are  not    found ') 
        

    return HttpResponse("Invalid request")

# https://raw.githubusercontent.com/sashaTen/investment_app/refs/heads/main/invest/S%26P500data/clusters_df.csv



def testing(request):
  

    return HttpResponse('test')



#   python  manage.py runserver     python manage.py migrate