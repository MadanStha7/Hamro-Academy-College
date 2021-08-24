from django.urls import path, include
from inquiry.administrator.views.inquiry import InquiryView

administration_urlpatterns = [
    path("inquiry/", InquiryView.as_view({"get": "list"})),
    path("inquiry/<pk>/", InquiryView.as_view({"get": "retrieve"})),
]

urlpatterns = [path("administrator/", include(administration_urlpatterns))]
