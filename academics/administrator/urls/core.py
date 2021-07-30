from .section import urlpatterns as section_urls
<<<<<<< academics/administrator/urls/core.py
from .grade import urlpatterns as grade_urls
from .subject import urlpatterns as subject_urls
from .faculty import urlpatterns as faculty_urls


urlpatterns = section_urls + grade_urls + faculty_urls + subject_urls


