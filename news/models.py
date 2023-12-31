from django.db import models
from neighborhood.models import Neighborhood

class News(models.Model):
    title       = models.CharField(max_length= 30)
    text        = models.TextField(max_length= 100)
    link        = models.URLField(max_length= 50, null=True, blank=True)
    date        = models.DateTimeField()
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "News"