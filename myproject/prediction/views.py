from django.shortcuts import render
from .scraping  import scrape_latest_news
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .pipeline  import   sentiment_analysis_pipeline
from zenml.client import Client





def hello_world(request):
   
   
        
    return render(request ,   'hello.html')



def  testing(request):
    return   HttpResponse('testing')

# https://raw.githubusercontent.com/sashaTen/investment_app/refs/heads/main/invest/S%26P500data/clusters_df.csv


def  prediction_result(request):
    vectorize_artifact = Client().get_artifact_version("9f42ba36-0287-4b1e-aaa9-46fbb54d45f4")
    vectorizer = vectorize_artifact .load()
    model_artifact = Client().get_artifact_version("62efc70b-2133-497d-94f5-cfb4ff03f4fa")
    model = model_artifact.load()
    text= 'bad news'
    text = [text]
    strings = scrape_latest_news()
    prediction =  model.predict(vectorizer.transform(strings))
    strings = scrape_latest_news()
    return   HttpResponse( prediction )



#   python  manage.py runserver 