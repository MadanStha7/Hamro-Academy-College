from .section import urlpatterns as section_urls
from .grade import urlpatterns as grade_urls
from .faculty import urlpatterns as faculty_urls
from .shift import urlpatterns as shift_urls
from .class_url import urlpatterns as class_urls
from .subject import urlpatterns as subject_urls
from .subject_group import urlpatterns as subject_group_urls
from .apply_shift import urlpatterns as apply_shift_url


urlpatterns = (
    section_urls
    + grade_urls
    + faculty_urls
    + shift_urls
    + class_urls
    + subject_urls
    + subject_group_urls
    + apply_shift_url
)
