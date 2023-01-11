from django.urls import path

from . import views

urlpatterns = [
    path("login/sms/", views.LoginView.as_view(), name="account_login_sms"),
]
