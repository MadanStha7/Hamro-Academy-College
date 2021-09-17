from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from rest_framework.serializers import ValidationError
from rest_framework import filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
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
    FeeCollectionSerializer,
    StudentPaidFeeSetupSerializer,
    UpdateStudentPaidFeeConfigSerializer,
    StudentPaidFeeSetupLogSerializer,
)
from permissions import administrator
from fees.orm import models as orm
from fees.utils.filter import FeeFilter, FeeConfigFilter
from fees.domain import commands, exceptions as domain_exceptions
from fees.orm.models import FeeConfig, StudentPaidFeeSetup


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
            except domain_exceptions.DuplicateFeeConfigPaidException as e:
                return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            except domain_exceptions.PaidAmountExceedException as e:
                return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            except domain_exceptions.SameFeeConfigMultipleTimeException as e:
                return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)


class StudentCollectedFeeInvoiceViewset(CommonInfoViewSet):
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]
    http_method_names = ["get", "delete"]
    serializer_class = FeeCollectionSerializer

    def get_queryset(self):
        student_academic = self.request.query_params.get("student_academic")
        if student_academic:
            data = views.get_student_collected_fee_invoices(
                student_academic, self.request.user.institution
            )
            return data
        raise ValidationError({"error": ["student_academic is required query param"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        paid_fee_setup = StudentPaidFeeSetup.objects.filter(
            fee_collection=instance
        ).select_related("fee_config", "fee_collection")
        paid_fee_setup_serializer = StudentPaidFeeSetupSerializer(
            paid_fee_setup, many=True, context={"request": request}
        )
        context = {
            "fee_collection": serializer.data,
            "paid_fee_config": paid_fee_setup_serializer.data,
        }
        return Response(context)

    @action(detail=False, methods=["GET"])
    def student_paid_fee_logs(self, request, *args, **kwargs):
        student_academic = request.query_params.get("student_academic")
        if student_academic:
            logs = (
                orm.StudentPaidFeeSetupUpdateLog.objects.filter(
                    paid_fee_setup__fee_collection__student_academic=student_academic
                )
                .annotate(fee_type_name=F("paid_fee_setup__fee_config__fee_type__name"))
                .select_related("paid_fee_setup")
            )
            serializer = StudentPaidFeeSetupLogSerializer(logs, many=True)
            return Response(serializer.data)
        raise ValidationError(
            {"error": ["student_academic is required query parameter"]}
        )


class UpdateStudentPaidFeeConfigView(APIView):
    permission_classes = [IsAuthenticated, administrator.AdministratorPermission]

    def post(self, request, *args, **kwargs):
        serializer = UpdateStudentPaidFeeConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cmd = commands.UpdateStudentPaidFeeConfig(**request.data)
            handlers.update_student_paid_fee_config(cmd, self.request.user)
            return Response({"message": ["Fee updated successfully"]})
        except domain_exceptions.NoChangeException as e:
            return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

        except domain_exceptions.PaidAmountExceedException as e:
            return Response({"error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
