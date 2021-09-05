from staff.administrator.urls.core import urlpatterns as administrator_urls
from staff.frontdesk.urls.core import urlpatterns as frontdesk_urls


urlpatterns = administrator_urls + frontdesk_urls
