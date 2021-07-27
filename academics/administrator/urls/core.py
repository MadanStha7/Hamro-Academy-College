from .section import urlpatterns as section_urls
from .grade import urlpatterns as grade_urls

urlpatterns = section_urls + grade_urls
