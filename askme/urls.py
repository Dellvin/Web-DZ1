from django.http import HttpResponse
from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main, name='main'),
    path('singIn/', views.singin, name='singIn'),
    path('singUp/', views.singup, name='singUp'),
    path('newQuestion/', views.newQuestion, name='newQuestion'),
    path('question/<int:qid>/', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('tagSearch/<str:tag>/', views.tagSearch, name='tagSearch'),
    path('newest/', views.newest, name='newest'),
    path('logout/', views.logout_view, name='logout'),
]