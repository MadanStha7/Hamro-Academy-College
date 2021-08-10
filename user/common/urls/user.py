from django.urls import path
from user.common.views.user import UserProfileView, UserChangePasswordView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path(
        "change_password/",
        UserChangePasswordView.as_view(),
        name="auth_change_password",
    ),
]
