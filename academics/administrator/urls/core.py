from .section import urlpatterns as section_urls
from .grade import urlpatterns as grade_urls
from .faculty import urlpatterns as faculty_urls
from .shift import urlpatterns as shift_urls
from .class_url import urlpatterns as class_urls

urlpatterns = section_urls + grade_urls + faculty_urls + shift_urls + class_urls
