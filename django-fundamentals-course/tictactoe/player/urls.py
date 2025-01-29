from tkinter.font import names

from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import home, new_invitation,accept_invitation

urlpatterns = [
path('home/', home, name='player_home'),  # Route for the home page
    path('login/', LoginView.as_view(template_name='player/login_form.html'), name='player_login'),  # Route for login page
    path('logout/', LogoutView.as_view(), name='player_logout'),  # Route for logout
    path('new_invitation',new_invitation,name="player_new_invitation"),
    path('accept_invitation/<int:id>/', accept_invitation, name="player_accept_invitation"),
]