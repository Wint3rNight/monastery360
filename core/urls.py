"""
URL configuration for core app.
"""

from django.urls import path

from . import auth_views, views
from .pwa_views import manifest_view, service_worker_view

app_name = 'core'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_redirect, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('profile/update/', auth_views.profile_update_view, name='profile_update'),

    # Monastery views
    path('monasteries/', views.monastery_list, name='monastery_list'),
    path('monasteries/map/', views.monastery_map, name='monastery_map'),
    path('monastery/<slug:slug>/', views.monastery_detail, name='monastery_detail'),

    # Search
    path('search/', views.search, name='search'),

    # PWA URLs
    path('manifest.json', manifest_view, name='manifest'),
    path('sw.js', service_worker_view, name='service_worker'),
    path('offline/', views.offline_view, name='offline'),
]
