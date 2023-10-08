from django.db import models
from django.conf import settings

class Neighborhood(models.Model):
    name     = models.CharField(max_length= 30)
    zip_code = models.CharField(max_length= 10)
    address  = models.CharField(max_length= 100)
    city     = models.CharField(max_length= 50)
    user     = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    
class House(models.Model):
    number      = models.CharField(max_length= 30)
    user        = models.CharField(max_length= 30)
    password    = models.CharField(max_length= 30)
    name        = models.CharField(max_length= 50, null=True)
    phone       = models.CharField(max_length= 15, null=True)
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.number