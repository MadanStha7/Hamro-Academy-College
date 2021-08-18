from general.administrator.urls.core import urlpatterns as academic_session_urls
from general.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls


urlpatterns = academic_session_urls + frontdeskofficer_urls
