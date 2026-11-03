from django.urls import path
from main import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('dash-list/<str:slug>/',views.RDashboardListAll, name='r-pay-today'),
]