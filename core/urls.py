from django.urls import path
from .views import InstitutionInfoView
from core.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls


urlpatterns = [
    path("institution/", InstitutionInfoView.as_view(), name="institution")
] + frontdeskofficer_urls
