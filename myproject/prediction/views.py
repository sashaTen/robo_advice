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
    vectorizer = vectorize_artifact.load()
    model_artifact = Client().get_artifact_version("0eef78a6-cfbb-411b-b397-20fe4f07b997")
    model = model_artifact.load()

    if request.method == "POST":
        ticker = request.POST.get("ticker")  # Get the text input from form
       
        company_news = request.POST.get("sentiment")  # This should be renamed if it's sentiment, not news

        prediction = model.predict(vectorizer.transform([company_news]))
        

    

        return HttpResponse(
            f"found: for {   ticker} the predicted sentiment: {prediction}"
        )
    else:
        return HttpResponse("News related to stock are not found")


'''
    save_news_with_sentiment( prediction)

        if test_data(NewsArticle) == 1:
            auto_retrain(3, NewsArticle)
'''


# https://raw.githubusercontent.com/sashaTen/investment_app/refs/heads/main/invest/S%26P500data/clusters_df.csv



def testing(request):
  

    return HttpResponse('test')



#   python  manage.py runserver     python manage.py migrate