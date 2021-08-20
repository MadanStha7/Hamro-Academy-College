from academics.frontdeskofficer.urls.faculty import urlpatterns as faculty_urls
from academics.frontdeskofficer.urls.grade import urlpatterns as grade_urls
from academics.frontdeskofficer.urls.section import urlpatterns as section_urls
from academics.frontdeskofficer.urls.subject import urlpatterns as subject_urls
from academics.frontdeskofficer.urls.class_url import urlpatterns as class_urls
from academics.frontdeskofficer.urls.apply_shift import urlpatterns as applyshift_urls


from academics.frontdeskofficer.urls.subject_group import (
    urlpatterns as subject_group_urls,
)
from academics.frontdeskofficer.urls.shift import (
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
