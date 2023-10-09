from django.urls import path
from . import views

urlpatterns = [
    path('get-by-user/<int:pk>/', views.NewsByUserView.as_view()),
]