from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    logout_then_login,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout_then_login/", logout_then_login, name="logout_then_login"),
    path("", views.dashboard, name="dashboard"),
    # Password change (requires old password)
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Password reset (forgotten password)
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # 🔥 This is where the reset link in email points!
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # ✅ This is shown *after* password is successfully changed
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Create account
    path("register/", views.register, name="register"),
    # Edit profile
    path("edit/", views.edit, name="edit"),
]
