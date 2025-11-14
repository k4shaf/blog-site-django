from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('dashboard/', views.AuthorDashboardView.as_view(), name='dashboard'),
    path('request-author/', views.request_author_role, name='request_author'),
    path('request-status/', views.request_status, name='request_status'),
]
