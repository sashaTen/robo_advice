from django.contrib import admin
from .models   import NewsArticle , Count
# Register your models here.
admin.site.register(NewsArticle)
admin.site.register(Count)