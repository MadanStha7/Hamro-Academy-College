from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import InstitutionInfoSerializers
from permissions.administrator import AdministratorPermission
from .models import InstitutionInfo


class InstitutionInfoView(RetrieveUpdateAPIView):
    serializer_class = InstitutionInfoSerializers
    permission_classes = (IsAuthenticated, AdministratorPermission)

    def get_object(self):
        object = InstitutionInfo.objects.get(id=self.request.institution.id)
        return object
