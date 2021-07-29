from django.urls import path
from user.common.views.user import UserProfileView

urlpatterns = [path("profile/", UserProfileView.as_view(), name="user_profile")]
