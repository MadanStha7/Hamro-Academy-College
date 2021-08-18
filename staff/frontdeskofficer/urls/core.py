from .designation import urlpatterns as designation_urls
from .staff import urlpatterns as staff_urls
from .profile import urlpatterns as profile_urls

urlpatterns = designation_urls + staff_urls + profile_urls
