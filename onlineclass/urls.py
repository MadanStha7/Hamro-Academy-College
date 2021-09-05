from onlineclass.administrator.urls.core import urlpatterns as administrator_urls
from onlineclass.frontdesk.urls.core import urlpatterns as frontdesk_urls


urlpatterns = administrator_urls + frontdesk_urls
