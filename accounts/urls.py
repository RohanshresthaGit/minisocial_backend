from .views import RegistrationView, LoginView
from django.urls import path

urlpatterns = [
    path('register', RegistrationView.as_view()),
    path('login', LoginView.as_view()),
]