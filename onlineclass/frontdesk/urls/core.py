from .online_class import urlpatterns as online_class_urls
from .online_class_filters import urlpatterns as online_class_filters_urls


urlpatterns = online_class_urls + online_class_filters_urls
