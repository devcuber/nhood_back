from news.serializers import NewsSerializer
from news.models import News
from neighborhood.models import House
from rest_framework.views import APIView
from rest_framework.response import Response

class NewsByUserView(APIView):
    def get(self, request, pk, format=None):
        neighborhood_id = House.objects.get(id = pk).Neighborhood.id
        queryset = News.objects.filter(Neighborhood_id=neighborhood_id)
        serializer = NewsSerializer(queryset, many=True)
        return Response( {'rows' : serializer.data} )

        