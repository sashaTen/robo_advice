from django.urls import path
from .views import hello_world , prediction_result

urlpatterns = [
    path('', hello_world), 
    path('prediction_result',prediction_result) # Calls hello_world() when the root URL is accessed
]
