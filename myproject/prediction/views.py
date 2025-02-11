from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .pipeline  import   sentiment_analysis_pipeline
from zenml.client import Client



def hello_world(request):
    vectorize_artifact = Client().get_artifact_version("9f42ba36-0287-4b1e-aaa9-46fbb54d45f4")
    vectorizer = vectorize_artifact .load()


    model_artifact = Client().get_artifact_version("62efc70b-2133-497d-94f5-cfb4ff03f4fa")
    model = model_artifact.load()
    text= 'bad news'
    text = [text]
    prediction =  model.predict(vectorizer.transform(text))
    return HttpResponse(prediction)



#   python  manage.py runserver 