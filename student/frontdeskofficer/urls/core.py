from .student import urlpatterns as student_urls
from .category import urlpatterns as category_urls


urlpatterns = student_urls + category_urls
