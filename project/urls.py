from django.urls import path
from project import views
urlpatterns = [
    path('',views.ProjectLists, name='proj-lists'),
    path('fc/',views.ProjectFCLists, name='proj-fc-lists'),
    path('add/',views.ProjectAdd, name='proj-add'),
    path('update/<str:uuid>/',views.ProjectUpdate, name='proj-update'),
    path('detail/<str:uuid>/',views.ProjectDetail, name='proj-detail'),
    path('status/update/<str:uuid>/',views.ProjectStatusUpdate, name='proj-status-update'),
    path('justification/update/<str:uuid>/',views.ProjectJustificationUpdate, name='proj-justification-update'),
    path('bank-guarantee/update/<str:uuid>/',views.ProjectBankGuaranteeUpdate, name='proj-bank-guarantee-update'),
]
