from student.administator.urls.core import urlpatterns as administrator_urls
from student.student.urls.core import urlpatterns as student_urls

urlpatterns = administrator_urls + student_urls
