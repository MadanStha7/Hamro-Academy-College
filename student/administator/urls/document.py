from django.urls import include, path
from rest_framework import routers
from student.administator.viewsets.document import StudentDocumentViewSet

router = routers.DefaultRouter()
router.register(r"student_document", StudentDocumentViewSet)

urlpatterns = [path("", include(router.urls))]
