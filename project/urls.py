"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from authentication.views import CustomTokenObtainPairView
from common.utils import encode_image

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path(
        "api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/v1/encode-image/", encode_image),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/", include("user.urls")),
    path("api/v1/", include("core.urls")),
    path("api/v1/", include("academics.urls")),
    path("api/v1/", include("general.urls")),
    path("api/v1/", include("user.urls")),
    path("api/v1/", include("student.urls")),
    path("api/v1/", include("guardian.urls")),
    path("api/v1/", include("staff.urls")),
    path("api/v1/", include("timetable.urls")),
    # path("api/v1/", include("onlineclass.urls")),
]
