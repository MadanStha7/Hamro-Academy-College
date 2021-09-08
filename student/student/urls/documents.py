from django.urls import path
from student.student.viewsets.documents import StudentDocumentAPIView

urlpatterns = [path("document/", StudentDocumentAPIView.as_view())]
