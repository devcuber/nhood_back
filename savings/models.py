from django.db import models
from neighborhood.models import House, Neighborhood
from django.db.models import Sum

class Balance(models.Model):
    house       = models.OneToOneField(House,on_delete=models.CASCADE,primary_key=True, editable=False)
    balance     = models.DecimalField(max_digits=6, decimal_places=2)
    debt        = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.house.number
    
    def update_balance(self):
        house_id    = self.house.id
        deposit     = Movement.objects.filter(house_id = house_id).aggregate(Sum('deposit')).get('deposit__sum' , 0)
        withdrawal  = Movement.objects.filter(house_id = house_id).aggregate(Sum('withdrawal')).get('withdrawal__sum' , 0)
        payments    = Payment.objects.filter(house_id = house_id, ispaid = True).aggregate(Sum('amount')).get('amount__sum' , 0)
        debt        = Payment.objects.filter(house_id = house_id, ispaid = False).aggregate(Sum('amount')).get('amount__sum' , 0)

        deposit     = deposit    if deposit    else 0
        withdrawal  = withdrawal if withdrawal else 0
        payments    = payments   if payments   else 0
        debt        = debt       if debt       else 0

        balance_total   = deposit - withdrawal - payments
        self.balance = balance_total
        self.debt    = debt
        self.save()

    
class Movement(models.Model):
    date        = models.DateTimeField()
    time        = models.TimeField()
    concept	    = models.CharField(max_length= 50)
    withdrawal	= models.DecimalField(max_digits=6, decimal_places=2)
    deposit     = models.DecimalField(max_digits=6, decimal_places=2)
    reference   = models.CharField(max_length= 30)
    house       = models.ForeignKey(House, on_delete=models.CASCADE, null=True)
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference

class PaymentConcept(models.Model):
    Neighborhood= models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    name	    = models.CharField(max_length= 30)
    amount	    = models.DecimalField(max_digits=6, decimal_places=2)     
    order       = models.IntegerField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(PaymentConcept, self).save(*args, **kwargs)
        nhoodid = self.Neighborhood.id
        for house in House.objects.filter(Neighborhood_id = nhoodid):
            payment = Payment(
                house = house,
                amount = self.amount,
                concept = self,
                ispaid = False
            )
            payment.save()


class Payment(models.Model):
    house       = models.ForeignKey(Balance, on_delete=models.CASCADE)
    amount	    = models.DecimalField(max_digits=6, decimal_places=2)
    concept     = models.ForeignKey(PaymentConcept, on_delete=models.CASCADE)
    ispaid      = models.BooleanField(default=False)

    def __str__(self):
        return self.concept.name
    
    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        self.house.update_balance()