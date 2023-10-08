from django.db import models
from neighborhood.models import House, Neighborhood

class Balance(models.Model):
    house       = models.OneToOneField(House,on_delete=models.CASCADE,primary_key=True)
    balance     = models.DecimalField(max_digits=6, decimal_places=2)
    debt        = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.house}:${self.balance}'
    
class Movement(models.Model):
    date        = models.DateTimeField()
    time        = models.TimeField()
    branch	    = models.CharField(max_length= 30)          
    concept	    = models.CharField(max_length= 50)
    withdrawal	= models.DecimalField(max_digits=6, decimal_places=2)
    deposit     = models.DecimalField(max_digits=6, decimal_places=2)
    balance	    = models.DecimalField(max_digits=6, decimal_places=2)
    reference   = models.CharField(max_length= 30)
    house       = models.ForeignKey(House, on_delete=models.CASCADE, null=True)
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference

class PaymentConcept(models.Model):
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    name	    = models.CharField(max_length= 30)
    amount	    = models.DecimalField(max_digits=6, decimal_places=2)     

class Payment(models.Model):
    house       = models.ForeignKey(House, on_delete=models.CASCADE)
    amount	    = models.DecimalField(max_digits=6, decimal_places=2)
    concept     = models.ForeignKey(PaymentConcept, on_delete=models.CASCADE)
    ispaid      = models.BooleanField(default=False)