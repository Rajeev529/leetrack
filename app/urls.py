from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path('searchpage', views.search_page),
    path('api/companies/', views.get_companies),
    path('question/<str:company_name>/', views.company_questions, name='company_questions'),
    path('roadmap_30/<str:company_name>/', views.roadmap_30, name="roadmap_30"),
]