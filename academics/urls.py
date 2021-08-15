from academics.administrator.urls.core import urlpatterns as administrator_urls
from academics.teacher.urls.core import urlpatterns as teacher_urls

urlpatterns = administrator_urls + teacher_urls
