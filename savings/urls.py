from django.urls import path
from . import views

urlpatterns = [
    path('get-savings-summary/<int:pk>/', views.SavingsSummaryView.as_view()),
    path('get-savings-resume/<int:pk>/', views.SavingsResumeView.as_view()),
]