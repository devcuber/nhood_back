from django.contrib import admin
from neighborhood.models import Neighborhood, House


class NeighborhoodAdmin(admin.ModelAdmin):
    pass

class HouseAdmin(admin.ModelAdmin):
    list_display = ["number","name"]

    def get_queryset(self, request):
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        if nhood_id:
            return House.objects.filter(Neighborhood_id = nhood_id)
        return House.objects.all()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(HouseAdmin, self).get_form(request, obj, **kwargs)
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        form.base_fields['Neighborhood'].initial = nhood_id
        form.base_fields['Neighborhood'].disabled = True
        return form



admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(House, HouseAdmin)