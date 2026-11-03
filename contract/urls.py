from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.ContractLists, name="contract-lists"),
    path('fc/lists/', views.ContractFCLists, name="contract-fc-lists"),
]