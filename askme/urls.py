from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main, name='main'),
    path('singIn/', views.singin, name='singIn'),
    path('singUp/', views.singup, name='singUp'),
    path('newQuestion/', views.newQuestion, name='newQuestion'),
    path('question/<int:qid>/', views.question, name='question'),
    path('edit/', views.settings, name='settings'),
    path('tagSearch/<str:tag>/', views.tagSearch, name='tagSearch'),
    path('newest/', views.newest, name='newest'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),

    path('like/', views.like, name='like'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
