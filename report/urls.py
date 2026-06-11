from django.urls import path
from report import views
urlpatterns = [
    path('',views.RDashboard, name='r-dashboard'),
    path('program/<int:year>/',views.RProgramDashboard, name='r-program-dashboard'),
    path('owner/<int:year>/',views.ROwnerDashboard, name='r-owner-dashboard'),
    path('all/list/<int:year>/',views.RListAll, name='r-list-all'),
    path('owner/list/<int:year>/<int:pk>/',views.RSubOwnerListAll, name='r-owner-list-all'),
    path('program/list/<int:year>/<int:pk>/',views.RProgramListAll, name='r-program-list-all'),
    path('sub-program/list/<int:year>/<int:pk>/',views.RSubProgramListAll, name='r-sub-program-list-all'),



    
]
