from django.urls import path

from . import views

urlpatterns = [
    path('', views.ViewCompany.as_view(), name='company'),
    path('add_employees/', views.AddEmployees.as_view(), name='company_add_employees'),
    path('remove_employees/', views.RemoveEmployees.as_view(), name='company_remove_employees'),
    path('invite_employee/', views.InviteEmployee.as_view(), name='company_invite_employee'),
    path('add_team/', views.TeamAdd.as_view(), name='company_add_team'),
    path('delete_team/<int:pk>/', views.TeamDelete.as_view(), name='company_delete_team'),
    path('team/<int:pk>/add/', views.AddTeamMembers.as_view(), name='team_add_members'),
]
