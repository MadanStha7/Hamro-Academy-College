from academics.frontdesk.urls.faculty import urlpatterns as faculty_urls
from academics.frontdesk.urls.grade import urlpatterns as grade_urls
from academics.frontdesk.urls.section import urlpatterns as section_urls
from academics.frontdesk.urls.subject import urlpatterns as subject_urls
from academics.frontdesk.urls.class_url import urlpatterns as class_urls
from academics.frontdesk.urls.apply_shift import urlpatterns as applyshift_urls


from academics.frontdesk.urls.subject_group import (
    urlpatterns as subject_group_urls,
)
from academics.frontdesk.urls.shift import (
    urlpatterns as shift_group_urls,
)


urlpatterns = (
    faculty_urls
    + grade_urls
    + section_urls
    + subject_urls
    + subject_group_urls
    + shift_group_urls
    + class_urls
    + applyshift_urls
)
