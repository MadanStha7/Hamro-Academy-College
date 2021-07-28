from .section import urlpatterns as section_urls
from .subject import urlpatterns as subject_urls

urlpatterns = section_urls
urlpatterns += subject_urls
