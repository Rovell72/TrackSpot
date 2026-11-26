from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_track, name='upload_track'),
    path('<int:pk>/edit/', views.edit_track, name='edit_track'),
    path('<int:pk>/delete/', views.delete_track, name='delete_track'),
]
