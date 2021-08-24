from django.urls import path
from .views import InstitutionInfoView
from core.frontdesk.urls.core import urlpatterns as frontdesk_urls


urlpatterns = [
    path("institution/", InstitutionInfoView.as_view(), name="institution")
] + frontdesk_urls
