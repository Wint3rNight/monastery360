"""
URL configuration for tours app.
"""

from django.urls import path

from . import views

app_name = 'tours'

urlpatterns = [
    # Virtual tours gallery
    path('', views.virtual_tours_gallery, name='virtual_tours_gallery'),
    path('list/', views.panorama_list, name='panorama_list'),
    path('map/', views.tour_map, name='tour_map'),
    path('test/', views.test_view, name='test_view'),  # Simple test URL
    path('monastery/<slug:slug>/', views.monastery_tour, name='monastery_tour'),
    path('pano/<str:pano_id>/', views.monastery_detail_by_pano, name='monastery_detail_by_pano'),
    path('panorama/<slug:monastery_slug>/<int:panorama_id>/', views.panorama_detail, name='panorama_detail'),
]
