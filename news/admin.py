from django.contrib import admin
from news.models import News
from neighborhood.models import Neighborhood

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title","date"]
    def get_queryset(self, request):
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        if nhood_id:
            return News.objects.filter(Neighborhood_id = nhood_id)
        return News.objects.all()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
        nhood_id = Neighborhood.objects.filter(user_id = request.user.id).first()
        form.base_fields['Neighborhood'].initial = nhood_id
        form.base_fields['Neighborhood'].disabled = True
        return form

admin.site.register(News, NewsAdmin)