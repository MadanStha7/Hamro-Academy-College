from .student import urlpatterns as student_urls
from .category import urlpatterns as category_urls
from .academic import urlpatterns as student_academic_urls
from .previous_academic import urlpatterns as previous_academic_urls
from .document import urlpatterns as document_urls
from .student_enable_disable import urlpatterns as student_enable_disable_urls
from .parse_sheet import urlpatterns as parse_sheet_urls

urlpatterns = (
    student_urls
    + category_urls
    + student_academic_urls
    + previous_academic_urls
    + document_urls
    + student_enable_disable_urls
    + parse_sheet_urls
)
