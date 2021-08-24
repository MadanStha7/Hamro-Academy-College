
from .discount_type import urlpatterns as discount_type_urls
from .fine_type import urlpatterns as fine_type_urls


urlpatterns = discount_type_urls + fine_type_urls
