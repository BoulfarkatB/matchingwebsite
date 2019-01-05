from django.urls import path
from mainapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    # signup page
    path('signup/', views.signup, name='signup'),

## https://www.youtube.com/watch?v=p_n7g6tVloU
    # login page
    path('login/', auth_views.LoginView.as_view(template_name='mainapp/login.html'), name='login'),
    # logout page
    path('logout/', auth_views.LogoutView.as_view(template_name='mainapp/not-logged-in.html'), name='logout'),
    # user profile
    path('profile/', views.profile, name='profile'),
    # member's profile
    path('profile/<int:pk>/', views.profile, name='profile_with_pk'),
    # user profile edit page
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # members page
    path('members/', views.members, name='members'),
]
