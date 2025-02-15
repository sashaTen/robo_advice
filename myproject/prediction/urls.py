from django.urls import path
from .views import hello_world , prediction_result ,  testing

urlpatterns = [
    path('', hello_world ,    name   =  'hello_world'), 
    path('prediction_result',prediction_result ,  name ='prediction_result') ,# Calls hello_world() when the root URL is accessed
    path('testing' , testing ,name='testing'  )
]
