from django.db import models

# Create your models here.
class News(models.Model):
    title   = models.CharField(max_length= 30)
    text    = models.CharField(max_length= 100)
    link    = models.DateTimeField()
    date    = models.CharField(max_length= 50)
