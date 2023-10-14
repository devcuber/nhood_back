from django.contrib import admin
from savings.models import Movement, PaymentConcept, Balance, Payment
from neighborhood.models import Neighborhood, House
from savings.filters import MovementPendingFilter, BalanceHasCreditFilter, BalanceHasDebtFilter

from django.contrib.admin.helpers import ActionForm
from django import forms

class setHouseForm(ActionForm):
    house = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        #TODO get user id
        houses = House.objects.all().values("id","number").order_by("number")
        houses_list = [ (house.get('id'), house.get('number') ) for house in houses ]
        self.base_fields["house"].choices = houses_list
        super().__init__(*args, **kwargs)

class MovementAdmin(admin.ModelAdmin):
    action_form = setHouseForm
    list_display = ["reference","date","time","concept","withdrawal","deposit","house"]
    actions = ["set_house"]
    ordering = ["-date","-time"]
    search_fields = ["concept"]
    list_filter = [MovementPendingFilter, "house"]


    def get_queryset(self, request):
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        if nhood_id:
            return Movement.objects.filter(Neighborhood_id = nhood_id)
        return Movement.objects.all()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(MovementAdmin, self).get_form(request, obj, **kwargs)
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        form.base_fields['Neighborhood'].initial = nhood_id
        form.base_fields['Neighborhood'].disabled = True
        form.base_fields['house'].required = False
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "house":
            nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
            if nhood_id:
                kwargs["queryset"] = House.objects.filter(Neighborhood_id = nhood_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    @admin.action(description="Set house for selected movements")
    def set_house(self, request, queryset):
        house = request.POST['house']
        queryset.update(house_id=house)

admin.site.register(Movement, MovementAdmin)

class PaymentConceptAdmin(admin.ModelAdmin):
    list_display = ["name", "amount", "order"]
    def get_queryset(self, request):
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        if nhood_id:
            return PaymentConcept.objects.filter(Neighborhood_id = nhood_id)
        return PaymentConcept.objects.all()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(PaymentConceptAdmin, self).get_form(request, obj, **kwargs)
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        form.base_fields['Neighborhood'].initial = nhood_id
        form.base_fields['Neighborhood'].disabled = True
        return form
    
admin.site.register(PaymentConcept, PaymentConceptAdmin)

class PaymentAdminInline(admin.TabularInline):
    model = Payment
    list_display = ["house","amount","concept","ispaid"    ]
    readonly_fields=("house","amount","concept" )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        qs = super(PaymentAdminInline, self).get_queryset(request)
        return qs.filter(ispaid=False).order_by("concept__order")

class BalanceAdmin(admin.ModelAdmin):
    list_display = ["house","balance","debt"]
    readonly_fields=('house',"balance","debt" )
    actions = ["update_balances"]
    list_filter = [BalanceHasCreditFilter, BalanceHasDebtFilter]
    search_fields = ["house__number"]
    inlines = (PaymentAdminInline, )
    def get_queryset(self, request):
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        if nhood_id:
            return Balance.objects.filter(house__Neighborhood_id = nhood_id).order_by('house__number')
        return Balance.objects.all().order_by('house__number')

    @admin.action(description="Update balances")
    def update_balances(self, request, queryset):
        for balance in queryset:
            balance.update_balance()        
    
admin.site.register(Balance, BalanceAdmin)