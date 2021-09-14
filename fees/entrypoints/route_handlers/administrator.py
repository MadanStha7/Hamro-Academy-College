from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from rest_framework.serializers import ValidationError
from rest_framework import exceptions, filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from fees.service_layer import handlers
from fees.service_layer import views
from common.administrator.viewset import CommonInfoViewSet
from fees.service_layer.serializers.fee_setup import (
    FeeSetupSerializer,
    FeeConfigSerializer,
    StudentFeeCollectSerializer,
)
from permissions import administrator
from fees.orm import models as orm
from fees.utils.filter import FeeFilter, FeeConfigFilter
from fees.domain import commands, exceptions
from fees.orm.models import FeeConfig


from common.utils import active_academic_session


class FeeSetupViewSet(CommonInfoViewSet):
    serializer_class = FeeSetupSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = FeeFilter
    search_fields = ["name"]
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]

    def get_queryset(self):
        queryset = handlers.get_fee_setup(institution=self.request.institution)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = FeeSetupSerializer(
            data=request.data, context={"institution": request.institution}
        )
        serializer.is_valid(raise_exception=True)
        cmd = commands.AddFeeSetup(**request.data)
        fee_setup = handlers.add_fee_setup(
            institution=self.request.institution, created_by=self.request.user, cmd=cmd
        )
        return Response(
            FeeSetupSerializer(fee_setup).data, status=status.HTTP_201_CREATED
        )


class FeeConfigView(APIView):
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = FeeConfigFilter

    def get(self, request, *args, **kwargs):
        data = views.get_fee_config(
            institution=self.request.institution,
            grade=request.query_params.get("grade"),
            faculty=request.query_params.get("faculty"),
        )
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = FeeConfigSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        cmds = []
        for data in request.data:
            cmd = commands.AddFeeConfig(**data)
            cmds.append(cmd)
        handlers.add_fee_config(
            instiution=self.request.institution, created_by=self.request.user, cmds=cmds
        )
        return Response(
            {"message": "Fee Configuration success"}, status=status.HTTP_201_CREATED
        )


class ActivateDeactivateFeeConfig(APIView):
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]

    def post(self, request, *args, **kwargs):
        cmd = commands.ActivateDeactivateFeeConfig(fee_config=self.kwargs.get("pk"))
        fee_config = handlers.activate_deactivate_fee_config(cmd=cmd)
        return Response(FeeConfigSerializer(fee_config).data)


class StudentFeeCollectionView(APIView):
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]

    def get(self, request, *args, **kwargs):
        student_academic = request.query_params.get("student_academic")
        if student_academic:
            data = views.get_student_fee_collection(
                student_academic, self.request.institution
            )
            return Response(data)
        raise ValidationError(
            {"error": ["student_academic is required query parameter"]}
        )

    def post(self, request, *args, **kwargs):
        student_academic = request.query_params.get("student_academic")
        if student_academic:
            try:
                serializer = StudentFeeCollectSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                cmd = commands.CollectStudentFee(**request.data)
                handlers.collect_student_fee(
                    cmd=cmd,
                    student_academic=student_academic,
                    institution=self.request.user.institution,
                    created_by=self.request.user,
                )
                return Response(
                    {"message": ["Student fee collected successfully"]},
                    status=status.HTTP_201_CREATED,
                )
            except exceptions.DuplicateFeeConfigPaidException as e:
                return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            except exceptions.PaidAmountExceedException as e:
                return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
