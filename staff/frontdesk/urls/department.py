from django.urls import path, include
from staff.frontdesk.views.department import DepartmentView

frontdesk_urlpatterns = [
    path("department/", DepartmentView.as_view({"get": "list"})),
    path("department/<pk>/", DepartmentView.as_view({"get": "retrieve"})),
]

urlpatterns = [path("frontdesk/", include(frontdesk_urlpatterns))]
