from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rapat/<slug:slug>/', views.rapat_detail, name='rapat_detail'),
    path('rapat/<slug:slug>/edit/', views.rapat_edit, name='rapat_edit'),
    path('rapat/<slug:slug>/delete/', views.rapat_delete, name='rapat_delete'),
    path('rapat/<slug:slug>/qr/', views.rapat_qr, name='rapat_qr'),
    path('rapat/<slug:slug>/pesan/', views.rapat_pesan, name='rapat_pesan'),
    path('rapat/<slug:slug>/pesanan/<int:pesanan_id>/edit/', views.pesanan_edit, name='pesanan_edit'),
    path('rapat/<slug:slug>/pesanan/<int:pesanan_id>/delete/', views.pesanan_delete, name='pesanan_delete'),
    path('rapat/<slug:slug>/menu/', views.menu_kelola, name='menu_kelola'),
    path('rapat/<slug:slug>/menu/<int:menu_id>/edit/', views.menu_edit, name='menu_edit'),
    path('rapat/<slug:slug>/menu/<int:menu_id>/delete/', views.menu_delete, name='menu_delete'),
]
