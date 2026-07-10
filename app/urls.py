from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_page, name='search_page'),
    path('api/companies/', views.get_companies),
    path('question/<str:company_name>/', views.company_questions, name='company_questions'),
    path('roadmap_30/<str:company_name>/', views.roadmap_30, name="roadmap_30"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('save-company/<str:company_name>/', views.save_company, name='save_company'),
    path('toggle-solve/<str:company_name>/<str:question_name>/', views.toggle_solve, name='toggle_solve'),
]