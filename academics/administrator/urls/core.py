from .section import urlpatterns as section_urls
from .faculty import urlpatterns as faculty_urls

urlpatterns = section_urls + faculty_urls
