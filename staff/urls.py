from staff.administrator.urls.core import urlpatterns as administrator_urls
from staff.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls


urlpatterns = administrator_urls + frontdeskofficer_urls
