from django.urls import path
from . import views

urlpatterns = [
    path('alloc-lists/', views.AllocationLists, name="alloc-lists"),
    path('alloc-fc-lists/', views.AllocationFCLists, name="alloc-fc-lists"),
    path('alloc-add/<str:uuid>/', views.AllocationAdd, name="alloc-add"),
    path('alloc-lock/<str:uuid>/', views.AllocationLock, name="alloc-lock"),
    path('alloc-delete/<str:uuid>/', views.AllocationDelete, name="alloc-delete"),

    path('trans-lists/', views.TransferenciaLists, name="trans-lists"),
    path('fc/trans-lists/', views.TransferenciaFCLists, name="trans-fc-lists"),
    path('trans-add/<str:uuid>/<str:uuid2>/', views.TransferenciaAdd, name="trans-add"),
    path('trans-lock/<str:uuid>/', views.TransferenciaLock, name="trans-lock"),
    path('trans-delete/<str:uuid>/', views.TransferenciaDelete, name="trans-delete"),
]