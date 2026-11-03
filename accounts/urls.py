from django.urls import path
from . import views

urlpatterns = [
    path('', views.userList, name='user_list'),
    path('deleteUsers/<int:hamosID>', views.deleteUsers, name='deleteUsers'),
    path('resetUsersPassword/<int:id>', views.resetUsersPassword, name='resetUsersPassword'),
    path('ativu-user/<str:id>', views.ativuUser, name="ativuUser"),
    path('desativu-user/<str:id>', views.desativuUser, name="desativuUser"),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]