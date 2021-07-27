from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.section import SectionViewSet


router = routers.DefaultRouter()
router.register("section", SectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
