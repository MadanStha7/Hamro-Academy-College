from django.urls import path
from onlineclass.student.views.regular_class import StudentRegularClassView

urlpatterns = [path("regular_class/", StudentRegularClassView.as_view())]
