from django.urls import path
from . import views

urlpatterns = [
    path('load-posts/', views.load_posts, name='ajax_load_posts'),
    path('load-villages/', views.load_villages, name='ajax_load_villages'),
    path('load-aldeia/', views.load_aldeia, name='ajax_load_aldeia'),
]