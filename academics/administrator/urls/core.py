from .section import urlpatterns as section_urls
from .subject import urlpatterns as subject_urls
from .subject_group import urlpatterns as subject_group_urls

urlpatterns = section_urls
urlpatterns += subject_urls
urlpatterns += subject_group_urls
