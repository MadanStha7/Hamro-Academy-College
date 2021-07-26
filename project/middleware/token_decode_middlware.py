import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from core.models import InstitutionInfo


class HandleJWTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION")
        if access_token:
            token = access_token.split(" ")[1]
            if len(token) > 100:
                decoded = jwt.decode(token, options={"verify_signature": False})
                request.institution = InstitutionInfo(id=decoded.get("institution"))
                request.roles = decoded.get("roles")
                request.password_updated = decoded.get("password_updated")
        return None

    def process_exception(self, request, exception):
        if str(exception) == "'Request' object has no attribute 'general_info'":
            return HttpResponse("requires JWT token to access this API")
        return None
