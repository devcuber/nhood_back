from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from news.serializers import NewsSerializer
from news.models import News


# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = News.objects.filter(Neighborhood_id=1)
    serializer_class = NewsSerializer
    #permission_classes = [permissions.IsAuthenticated]
