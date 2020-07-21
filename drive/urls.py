from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('drive/', views.DriveView.as_view(), name='drive'),
    path('public-delete/<int:pk>/', views.PublicDeleteView.as_view(), name='pubdel'),
    path('private-delete/<int:pk>/', views.PrivateDeleteView.as_view(), name='privdel'),
]
