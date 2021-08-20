from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from core.frontdeskofficer.serializers.institution import InstitutionInfoSerializers
from permissions.front_desk_officer import FrontDeskOfficerPermission
from core.models import InstitutionInfo


class InstitutionAPIView(RetrieveUpdateAPIView):
    serializer_class = InstitutionInfoSerializers
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        return InstitutionInfo.objects.get(id=self.request.institution.id)
