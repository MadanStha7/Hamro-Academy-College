from django.urls import path
from .views import InstitutionInfoView

urlpatterns = [path("institution/", InstitutionInfoView.as_view(), name="institution")]
