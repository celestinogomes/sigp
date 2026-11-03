from django.urls import path
from custom import views




urlpatterns = [
    path('<str:slug>/lists/', views.CustomLists, name='custom-list')
]
