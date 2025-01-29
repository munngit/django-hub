from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from gameplay import views  # ✅ Import views as a module

urlpatterns = [
    path('detail/<int:id>/', views.game_detail, name="gameplay_detail"),
    path('make_move/<int:id>/', views.make_move, name='gameplay_make_move'),
]
