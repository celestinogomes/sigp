from django.urls import path
from . import views

urlpatterns = [
    path('amount-add/list/', views.AmandmenAmountList, name="amend-amount-list"),
    path('amount-add/fc-list/', views.AmandmenAmountFCList, name="amend-amount-fc-list"),
    path('amount-add/<str:uuid>/', views.AmendmentAmountAdd, name="amend-amount-add"),
    path('amount-add/<str:uuid>/<int:amendment_amount_id>/update/', views.AmendmentAmountUpdate, name="amend-amount-update"),


    path('time-add/list/', views.AmandmenTimeList, name="amend-time-list"),
    path('time-add/fc-list/', views.AmandmenFCTimeList, name="amend-time-fc-list"),
    path('time-add/<str:uuid>/', views.AmendmentTimeAdd, name="amend-time-add"),
    path('time-add/<str:uuid>/<int:amendment_time_id>/update/', views.AmendmentTimeUpdate, name="amend-time-update"),
]