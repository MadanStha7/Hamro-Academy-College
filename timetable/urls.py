from timetable.administrator.urls.core import urlpatterns as timetable_urls
from timetable.frontdesk.urls.core import urlpatterns as frontdesk_urls


urlpatterns = timetable_urls + frontdesk_urls
