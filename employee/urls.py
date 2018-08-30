from django.urls import path

from . import views

urlpatterns = [
    path('profile/<slug:username>/', views.ViewProfile.as_view(), name='profile'),
    path('my_profile/update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('my_invitations/', views.ListInvitation.as_view(), name='list_invitation'),
    path('invitation/<int:pk>/accept/', views.AcceptInvitation.as_view(), name='accept_invitation'),
    path('invitation/<int:pk>/delete/', views.DeleteInvitation.as_view(), name='delete_invitation'),
]
