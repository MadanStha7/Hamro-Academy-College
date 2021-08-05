# from .guardian import urlpatterns as guardian_urls
from .student import urlpatterns as student_urls
# from .category import urlpatterns as category_urls
# from .student_academic import urlpatterns as student_academic_urls
# from .previous_academic import urlpatterns as previous_academic_urls
# from .document import urlpatterns as document_urls

urlpatterns = (
    student_urls
    # + category_urls
    # + student_academic_urls
    # + previous_academic_urls
    # + document_urls
)
