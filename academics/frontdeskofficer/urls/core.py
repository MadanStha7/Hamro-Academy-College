from academics.frontdeskofficer.urls.faculty import urlpatterns as faculty_urls
from academics.frontdeskofficer.urls.grade import urlpatterns as grade_urls
from academics.frontdeskofficer.urls.section import urlpatterns as section_urls
from academics.frontdeskofficer.urls.subject import urlpatterns as subject_urls
from academics.frontdeskofficer.urls.subject_group import (
    urlpatterns as subject_group_urls,
)


urlpatterns = (
    faculty_urls + grade_urls + section_urls + subject_urls + subject_group_urls
)
