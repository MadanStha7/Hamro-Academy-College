from academics.teacher.urls.subject import urlpatterns as subject_urls
from academics.teacher.urls.academic import urlpatterns as academic_urls
from academics.teacher.urls.timetable import urlpatterns as timetable_urls
from academics.teacher.urls.profile import urlpatterns as profile_urls
from academics.teacher.urls.online_class import urlpatterns as online_class


urlpatterns = subject_urls + academic_urls + timetable_urls + profile_urls
