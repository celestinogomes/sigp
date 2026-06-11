from django.urls import path
from funsionariu import views

urlpatterns = [
    path('',views.ListFunsionariu, name='funsionario'),
    path('addfunsionario/',views.AddFunsionariu, name='add-funsionariu'),
    path('updatefunsionario/<str:id_update>/',views.UpdateFunsionariu, name='update-funsionariu'),
    path('deletefunsionario/<str:id_delete>/',views.DeleteFunsionariu, name='delete-funsionariu'),
    path('kria_user_funsionariu/<str:pk>/', views.kriaUser, name='kria_user_fun'),
]