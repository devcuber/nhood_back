from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from neighborhood.models import House

class LoginView(APIView):    
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            house = House.objects.get(user = username)
            if house.password == password:
                return Response({
                    'id' : house.id,
                    'username' : house.user,
                    'name' : house.number,
                    'token' : 'dummy-auth-token'
                })      
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except:       
            return Response({}, status=status.HTTP_400_BAD_REQUEST)