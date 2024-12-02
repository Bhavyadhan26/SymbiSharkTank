from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('register/',views.register, name='register'),
    path('round2_register/',views.register_round2, name='register2'),
    path('user_profile/',views.user_profile, name='profile'),
    path('about/',views.about, name='about'),
    path('success_stories/',views.success_stories, name='success_stories'),
    path('home/',views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('meet/', views.meet, name='meeting'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)