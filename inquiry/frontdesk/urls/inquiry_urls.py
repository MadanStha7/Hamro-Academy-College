from django.urls import path, include
from rest_framework import routers
from inquiry.frontdesk.viewsets.inquiry import InquiryViewSet


router = routers.DefaultRouter()
router.register("frontdesk/inquiry", InquiryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
