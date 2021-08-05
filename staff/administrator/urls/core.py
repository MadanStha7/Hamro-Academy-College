from .designation import urlpatterns as designation_urls
from .staff import urlpatterns as staff_urls
from .staff_academicinfo import urlpatterns as staff_academicinfo_urls
from .document import urlpatterns as document_urls


urlpatterns = designation_urls + staff_urls + staff_academicinfo_urls + document_urls
