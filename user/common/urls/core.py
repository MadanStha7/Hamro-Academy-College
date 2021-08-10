from .user import urlpatterns as user_urls
from .user import urlpatterns as change_password_urls

urlpatterns = user_urls + change_password_urls
