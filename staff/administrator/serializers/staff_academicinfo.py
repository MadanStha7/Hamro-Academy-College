from rest_framework import serializers
from staff.models import StaffAcademicInfo

# from common.utils import validate_unique_name


class StaffAcademicInfoSerializer(serializers.ModelSerializer):
    contract_type_name = serializers.CharField(
        source="get_contract_type_display", read_only=True
    )

    class Meta:
        model = StaffAcademicInfo
        read_only_fields = ["institution", "created_by"]
        fields = [
            "id",
            "contract_type",
            "staff",
            "highest_degree",
            "experience",
            "working_days",
            "leave",
            "contract_type_name",
        ]
