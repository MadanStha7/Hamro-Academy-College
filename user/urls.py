from user.administrator.urls.core import urlpatterns as role_urls
from user.common.urls.core import urlpatterns as common_urls
from user.common.urls.core import urlpatterns as change_password_urls


urlpatterns = common_urls + role_urls + change_password_urls
