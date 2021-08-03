from django.db.models import ProtectedError
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status
from permissions.administrator import AdministratorPermission


class CommonInfoViewSet(viewsets.ModelViewSet):
    """
    viewing exam list and saving the new exam
    """

    permission_classes = (IsAuthenticated, AdministratorPermission)

    def get_object(self):
        queryset = self.filter_queryset(
            self.get_queryset().filter(institution=self.request.institution)
        )
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_context(self):
        context = super(CommonInfoViewSet, self).get_serializer_context()
        context["institution"] = self.request.institution
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(institution=self.request.institution)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.institution:
            serializer.save(
                created_by=self.request.user,
                institution=self.request.institution,
            )
        else:
            raise ValidationError(
                {
                    "error": [
                        "You must be a authenticated school staff to perform this action"
                    ]
                }
            )

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object().id
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(
                {"message": [f"object {obj} successfully  deleted"]},
                status=status.HTTP_200_OK,
            )
        except ProtectedError:
            raise ValidationError({"failed": ["Protected! unable to delete object"]})
