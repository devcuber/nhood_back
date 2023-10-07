from django.contrib import admin
from neighborhood.models import Neighborhood, House


class NeighborhoodAdmin(admin.ModelAdmin):
    pass

class HouseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(House, HouseAdmin)