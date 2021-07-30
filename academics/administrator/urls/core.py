from .section import urlpatterns as section_urls


from .grade import urlpatterns as grade_urls
from .faculty import urlpatterns as faculty_urls
from .subject import urlpatterns as subject_urls

urlpatterns = section_urls + grade_urls + faculty_urls + subject_urls
