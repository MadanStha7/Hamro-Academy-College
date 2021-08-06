
from rest_framework.generics import CreateAPIView, get_object_or_404
from common.administrator.viewset import CommonInfoViewSet
from guardian.administrator.serializer.guardianinfo import (
    GuardianInfoSerializer
)
from student.models import StudentGuardianInfo, StudentInfo
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status


class GuardianInfoViewSet(CommonInfoViewSet):
    queryset = StudentGuardianInfo.objects.none()
    serializer_class = GuardianInfoSerializer

    def get_queryset(self):
        """
        filtering guardian based on grade and section
        """
        queryset = StudentGuardianInfo.objects.filter(
            institution=self.request.institution
        )

        return queryset

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """
        Delete guardian based on the db ACID transition
        """
        instance = self.get_object()
        obj = self.get_object().id
        if instance.secondary_guardian:
            instance.secondary_guardian.delete()
        instance.user.delete()
        self.perform_destroy(instance)
        return Response(
            {"message": f"object {obj} successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class StudentGuardianInfoView(CreateAPIView):
    queryset = StudentGuardianInfo.objects.none()
    serializer_class = GuardianInfoSerializer

    def create(self, request, *args, **kwargs):
        new = self.request.query_params.get("new")
        student = self.request.query_params.get("student")
        if student:
            guardian = self.request.data.get("guardian")

            if new == "false":
                student = get_object_or_404(
                    StudentInfo, id=student, institution=self.request.institution
                )
                student = StudentInfo.objects.get(id=student)
                student.guardian_detail = guardian
                student.save()
                return Response({"message": "success"}, status=status.HTTP_200_OK)

            elif new == "true":
                serializer = GuardianInfoSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                guardian = serializer.save(
                    created_by=self.request.user,
                    institution=self.request.institution)
                student = get_object_or_404(
                    StudentInfo, id=student, institution=self.request.institution
                )
                student.guardian_detail = guardian
                student.save()
                return Response({"message": "success"}, status=status.HTTP_200_OK)

            return Response(
                {"message": ["You must be a institute student to perform this action"]}
            )


