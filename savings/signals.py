from django.db.models.signals import post_save
from django.dispatch import receiver
from neighborhood.models import House
from savings.models import Balance

@receiver(post_save, sender=House)
def house_created(sender, instance, created, **kwargs):
    if created:
        new_balance = Balance (
            house = instance,
            balance = 0,
            debt = 0
        )
        new_balance.save()