from academics.administrator.urls.core import urlpatterns as administrator_urls
from academics.teacher.urls.core import urlpatterns as teacher_urls
from academics.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls


urlpatterns = administrator_urls + teacher_urls + frontdeskofficer_urls
