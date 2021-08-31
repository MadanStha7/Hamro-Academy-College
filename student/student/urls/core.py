from django.urls import path, include
from timetable.student.urls.grade_timetable import urlpatterns as grade_urls
from onlineclass.student.urls.attendance import urlpatterns as attendance_urls
from academics.student.urls.subject import urlpatterns as subject_urls
from student.student.urls.teacher import urlpatterns as teacher_urls
from student.student.urls.profile import urlpatterns as profile_urls
from onlineclass.student.urls.regular_class import urlpatterns as regular_class_urls

student_urlpatterns = (
    grade_urls
    + attendance_urls
    + profile_urls
    + subject_urls
    + teacher_urls
    + regular_class_urls
)

urlpatterns = [path("student/", include(student_urlpatterns))]
