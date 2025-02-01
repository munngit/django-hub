from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from gameplay.views import game_detail, make_move, AllGamesList  # Import the class-based view

urlpatterns = [
    path('detail/<int:id>/', game_detail, name="gameplay_detail"),
    path('make_move/<int:id>/', make_move, name="gameplay_make_move"),
    path('all/', AllGamesList.as_view(), name="all_games"),  # Added URL for AllGamesList
]
