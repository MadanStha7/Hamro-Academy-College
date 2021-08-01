from rest_framework import viewsets
from general.models import AcademicSession
from general.administrator.serializers.academic_session import AcademicSessionSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.decorators import action
from rest_framework import status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class AcademicSessionViewSet(CommonInfoViewSet):
    """
    CRUD for academic session of the college.
    """

    serializer_class = AcademicSessionSerializer
    queryset = AcademicSession.objects.none()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = AcademicSession.objects.filter(institution=self.request.institution)
        return queryset

    @action(detail=False, methods=["POST", "PUT"])
    def active_or_inactive_academic_session(self, request):
        """
        API action method to make a academic session active or inactive
        """
        academic_session_id = self.request.query_params.get("session")
        if academic_session_id:
            academic_session = get_object_or_404(
                AcademicSession,
                id=academic_session_id,
                institution=self.request.institution,
            )
            if academic_session.status:
                academic_session.status = False
            else:
                AcademicSession.objects.filter(
                    status=True,
                    institution=self.request.institution,
                    grade=academic_session.grade,
                ).update(status=False)
                academic_session.status = True
            academic_session.save()
            serializer = self.get_serializer(academic_session)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": ["Session id is required"]},
            status=status.HTTP_400_BAD_REQUEST,
        )
