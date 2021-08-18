from student.administator.urls.core import urlpatterns as administrator_urls
from student.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls

urlpatterns = administrator_urls + frontdeskofficer_urls
