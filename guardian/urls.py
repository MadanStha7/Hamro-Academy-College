from guardian.administrator.urls.core import urlpatterns as administrator_urls
from guardian.frontdeskofficer.urls.core import urlpatterns as frontenddesk_urls


urlpatterns = administrator_urls + frontenddesk_urls
