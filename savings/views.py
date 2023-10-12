from django.shortcuts import render
from rest_framework.views import APIView
from savings.models import Balance, Movement, Payment
from rest_framework.response import Response
from django.db.models import Sum

class SavingsSummaryView(APIView):
    def get(self, request, pk, format=None):
        balance = Balance.objects.get(house_id = pk)
        nhood_id = balance.house.Neighborhood_id

        last_movement = Movement.objects.filter(Neighborhood_id = nhood_id).order_by('-date','-time').first()
        
        nhood_payments_in  = Payment.objects.filter(house__house__Neighborhood_id = nhood_id, ispaid = True).aggregate(Sum('amount'))
        nhood_payments_out = {'amount__sum':0} 
        nhood_balance = nhood_payments_in.get('amount__sum',0) - nhood_payments_out.get('amount__sum',0)

        nhood_debt = Payment.objects.filter(house__house__Neighborhood_id = nhood_id, ispaid = False).aggregate(Sum('amount'))
        nhood_debt = nhood_debt['amount__sum']

        return Response({
            "my_current_balance"           : "${:,.2f}".format(balance.balance),
            "my_current_balance_label"     : f"Saldo {balance.house.number}",
            "my_outstanding_balance"       : "${:,.2f}".format(balance.debt),
            "my_outstanding_balance_label" : f"Deuda {balance.house.number}",
            "our_current_balance"          : "${:,.2f}".format(nhood_balance),
            "our_current_balance_label"    : f"Saldo {balance.house.Neighborhood.name}",
            "our_outstanding_balance"      : "${:,.2f}".format(nhood_debt),
            "our_outstanding_balance_label": f"Pendiente {balance.house.Neighborhood.name}",
            "updated_at"                   : f'{last_movement.date.strftime("%d/%m/%Y")} {last_movement.time}',
            "updated_at_label"             : "Actualizado"
        })

class SavingsResumeView(APIView):
    def get(self, request, pk, format=None):
        neighborhood_id = Balance.objects.get(house_id = pk).house.Neighborhood.id
        balances = Balance.objects.filter(house__Neighborhood_id = neighborhood_id).order_by('house__number')
        rows = []

        for balance in balances:
            payments = Payment.objects.filter(house_id = balance.house.id).order_by('-concept__order')
            fields = [ {
                "id"     : payment.id,
                "label"  : payment.concept.name,
                "value"  : "${:,.2f}".format(payment.amount),
                "status" : "paid" if payment.ispaid else "debt"
            } for payment in payments]
            
            rows.append({
                "id"          : balance.house.id,
                "name"        : balance.house.number,
                "total_label" : "Deuda",
                "total"       : "${:,.2f}".format(balance.debt),
                "total_status": "debt" if balance.debt else "no-debt",
                "fields"      : fields
            })

        return Response({'rows':rows})