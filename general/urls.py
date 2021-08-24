from general.administrator.urls.core import urlpatterns as academic_session_urls
from general.frontdesk.urls.core import urlpatterns as frontdesk_urls


urlpatterns = academic_session_urls + frontdesk_urls
