from inquiry.frontdesk.urls.core import urlpatterns as frontdesk_urls
from inquiry.administrator.urls.core import urlpatterns as administrator_urls


urlpatterns = frontdesk_urls + administrator_urls
