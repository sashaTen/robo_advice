from django.db import models


class NewsArticle(models.Model):
    content = models.TextField()
    sentiment = models.FloatField()   # e.g., 'Positive', 'Negative', 'Neutral'
    real_price_change = models.FloatField()  # Store the confidence score of the prediction
    scraped_at = models.DateTimeField(auto_now_add=True)

   

#     python manage.py   makemigrations     migrate 
