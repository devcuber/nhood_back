from django.shortcuts import render
from rest_framework.views import APIView
from savings.models import Balance, Movement, Payment
from rest_framework.response import Response

class SavingsSummaryView(APIView):
    def get(self, request, pk, format=None):
        balance = Balance.objects.get(house_id = pk)
        last_movement = Movement.objects.filter(Neighborhood_id = balance.house.Neighborhood_id).order_by('-date','-time').first()
        return Response({
            "current_balance"           : "${:,.2f}".format(balance.balance),
            "current_balance_label"     : f"Saldo {balance.house.number}",
            "outstanding_balance"       : "${:,.2f}".format(balance.debt),
            "outstanding_balance_label" : f"Deuda {balance.house.number}",
            "month_income"              : "$0.00",
            "month_income_label"        : "Ingreso del mes",
            "month_expenses"            : "$0.00",
            "month_expenses_label"      : "Gastos del mes",
            "updated_at"                : f'{last_movement.date.strftime("%d/%m/%Y")} {last_movement.time}',
            "updated_at_label"          : "Actualizado"
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