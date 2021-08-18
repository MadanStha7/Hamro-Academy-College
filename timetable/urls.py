from timetable.administrator.urls.core import urlpatterns as timetable_urls
from timetable.frontdeskofficer.urls.core import urlpatterns as frontdeskofficer_urls


urlpatterns = timetable_urls + frontdeskofficer_urls
