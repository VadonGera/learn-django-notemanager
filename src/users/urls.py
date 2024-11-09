from django.urls import path
from .views import UserRegistrationView, UserListView, UserUpdateView


urlpatterns = [
    path("api/register/", UserRegistrationView.as_view(), name="user-register"),
    path("api/users/", UserListView.as_view(), name="user-list"),
    path("api/users/<int:pk>/", UserUpdateView.as_view(), name="user-detail"),
]
