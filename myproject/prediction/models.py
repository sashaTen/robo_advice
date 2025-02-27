from django.db import models


class NewsArticle(models.Model):
    content = models.TextField()
    sentiment = models.CharField(max_length=50)  # e.g., 'Positive', 'Negative', 'Neutral'
    confidence = models.FloatField()  # Store the confidence score of the prediction
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#     python manage.py migrate
