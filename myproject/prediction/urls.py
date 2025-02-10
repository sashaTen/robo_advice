from django.urls import path
from .views import hello_world

urlpatterns = [
    path('', hello_world),  # Calls hello_world() when the root URL is accessed
]
