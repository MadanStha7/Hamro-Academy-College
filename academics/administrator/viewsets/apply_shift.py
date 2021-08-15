from django.db.models import F
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from academics.models import ApplyShift, Faculty, Grade
from academics.administrator.serializers.apply_shift import ApplyShiftSerializer
from common.administrator.viewset import CommonInfoViewSet
from academics.administrator.utils.create_applyshift import create_applyshift
from django_filters import rest_framework as filters
from academics.administrator.custom_filter import ApplyShiftFilter


class ApplyShiftViewSet(CommonInfoViewSet):
    serializer_class = ApplyShiftSerializer
    queryset = ApplyShift.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ApplyShiftFilter

    def get_queryset(self):
        queryset = ApplyShift.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            shift_name=F("shift__name"),
            shift_start_time=F("shift__start_time"),
            shift_end_time=F("shift__end_time"),
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name"),
            section_name=F("section__name"),
        )
        return queryset

    @action(detail=False, methods=["POST", "PUT"])
    def save_apply_shift(self, request):
        faculty = self.request.query_params.get("faculty", False)
        grade = self.request.query_params.get("grade", False)

        if faculty:
            faculty_obj = get_object_or_404(Faculty, id=faculty)

        if grade:
            grade_obj = get_object_or_404(Grade, id=grade)

        if faculty_obj and grade_obj:
            list(
                map(
                    lambda data: data.update(
                        {
                            "faculty": faculty_obj.id,
                            "grade": grade_obj.id,
                        }
                    ),
                    request.data,
                )
            )
            serializer = ApplyShiftSerializer(data=request.data, many=True)

            if serializer.is_valid():
                response = create_applyshift(
                    request.data, self.request.user, self.request.institution
                )
                serializer = ApplyShiftSerializer(
                    response["data1"] + response["data2"], many=True
                )
                if response:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            return Response(
                {"error": ["please provide the required field in query params"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
