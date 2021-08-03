from django.db.models import F
from rest_framework.response import Response

from academics.models import ApplyShift
from academics.administrator.serializers.apply_shift import ApplyShiftSerializer
from common.administrator.viewset import CommonInfoViewSet


class ApplyShiftViewSet(CommonInfoViewSet):
    serializer_class = ApplyShiftSerializer
    queryset = ApplyShift.objects.none()

    def get_queryset(self):
        queryset = ApplyShift.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            shift_name=F("shift__name"),
            shift_start_time=F("shift__start_time"),
            shift_end_time=F("shift__end_time"),
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name"),
        )
        return queryset

    # def perform_create(self, serializer):
    #     grade = self.request.data.get("grade")
    #     shift = self.request.data.get("shift")
    #     faculty = self.request.data.get("faculty")
    #     section = self.request.data.get("section")
    #     applyshift = ApplyShift.objects.filter(grade__id=grade, shift__id=shift, faculty__id=faculty)
    #     print(applyshift)
    #
    #     if applyshift:
    #         return Response(
    #             {"message": ["ApplyShift with this data already exists."]}
    #         )
    #     else:
    #         ApplyShift.objects.filter(grade=grade, shift=shift, faculty=faculty).update(section=section)
