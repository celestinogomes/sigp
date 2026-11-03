from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.PaymentLists, name="payment-lists"),
    path('fc-lists/', views.PaymentFCLists, name="payment-fc-lists"),
    path('add/<str:uuid>/', views.PaymentAdd, name="payment-add"),
    path('update/<str:uuid>/', views.PaymentUpdate, name="payment-update"),
    path('refresh/<str:uuid>/', views.PaymentArchivedAndRefresh, name="payment-refresh"),
    path('history/<str:uuid>/', views.PaymentHistoryLists, name="payment-history"),
]