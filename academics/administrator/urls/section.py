from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.section import SectionViewSet, SectionListView

router = routers.DefaultRouter()
router.register("section", SectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("section_list/", SectionListView.as_view()),
]
