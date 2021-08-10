from rest_framework import viewsets
from staff.models import Staff
from staff.administrator.serializers.staff import (
    StaffSerializer,
    StaffListSerializer,
    StaffAssignSerialzer,
)
from common.administrator.viewset import CommonInfoViewSet
from staff.administrator.custom.filters import StaffFilter
from django.db.models import F
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import ValidationError

User = get_user_model()


class StaffViewSet(CommonInfoViewSet):
    """
    CRUD of the staff of college
    """

    serializer_class = StaffSerializer
    queryset = Staff.objects.none()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone",
    ]
    filter_class = StaffFilter

    def get_queryset(self):
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            designation__name=F("designation__name"),
        )
        return queryset

    def list(self, request):
        """api to get list of serializer of staff"""
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = self.filter_queryset(queryset)
        queryset = queryset.annotate(
            designation__name=F("designation__name"),
            staff_contact_number=F("user__phone"),
            staff_email=F("user__email"),
            staff_first_name=F("user__first_name"),
            staff_last_name=F("user__last_name"),
        )
        page = self.paginate_queryset(queryset)
        serializer = StaffListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["post", "get"])
    def assign_role(self, request):
        with transaction.atomic():
            user = self.request.data.get("user", False)
            roles = self.request.data.get("roles", False)
            for item in roles:
                if roles.count(item) > 1:
                    raise ValidationError(
                        {"error": ["Similar roles cannot be assigned"]}
                    )
            if user:
                user_id = get_object_or_404(User, id=user)
                if user_id:
                    for role in roles:
                        user = User(id=user_id.id).roles.add(role)
                        user = User.objects.get(id=user_id.id)
                        data = StaffAssignSerialzer(user)
                    return Response(data.data, status=status.HTTP_200_OK)
            return Response(
                {"error": ["User id is required"]},
                status=status.HTTP_404_NOT_FOUND,
            )
