from guardian.administrator.urls.core import urlpatterns as administrator_urls
from guardian.frontdesk.urls.core import urlpatterns as frontdesk


urlpatterns = administrator_urls + frontdesk
