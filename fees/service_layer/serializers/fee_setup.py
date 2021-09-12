from academics.models import Faculty, Grade
from rest_framework import serializers
import datetime
from common.utils import validate_unique_name
from fees.orm.models import (
    FeeConfig,
    FeeSetup,
    FeeCollection,
    FineType,
    StudentPaidFeeSetup,
)
from academics.administrator.serializers.faculty import FacultySerializer
from academics.administrator.serializers.grade import GradeSerializer


class FeeSetupSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True, many=True)
    grade = GradeSerializer(read_only=True, many=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source="faculty", write_only=True, many=True
    )
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), source="grade", write_only=True, many=True
    )

    class Meta:
        model = FeeSetup
        fields = [
            "id",
            "name",
            "fee_type",
            "faculty",
            "faculty_id",
            "grade",
            "grade_id",
            "due_date",
            "due_day",
            "due_type",
            "description",
        ]

    def validate_name(self, name):
        name = validate_unique_name(
            FeeSetup, name, self.context.get("institution"), self.instance
        )
        return name

    def validate_due_date(self, value):
        if not self.instance:
            if value and value < datetime.date.today():
                raise serializers.ValidationError("Due date cannot be past date.")
        return value


class FeeConfigSerializer(serializers.ModelSerializer):
    fee_type_name = serializers.CharField(read_only=True)

    class Meta:
        model = FeeConfig
        fields = ("id", "subject_group", "fee_type", "fee_type_name", "amount")

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Fee amount cannot have negative value")
        return value


class CollectFeeConfigSerializer(serializers.ModelSerializer):
    fee_config = serializers.UUIDField()
    paid_amount = serializers.FloatField()

    def validate_paid_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "paid amount should not accept negative value"
            )
        return value


class StudentFeeCollectSerializer(serializers.ModelSerializer):
    fee_configs = CollectFeeConfigSerializer(many=True)
    fine_id = serializers.PrimaryKeyRelatedField(
        queryset=FineType.objects.all(),
        source="fine",
        write_only=True,
        many=True,
    )

    class Meta:
        model = FeeCollection
        fields = (
            "id",
            "fee_configs",
            "discount_in",
            "discount",
            "fine_id",
            "fine",
            "payment_method",
            "narration",
        )

    def validate(self, attrs):
        if attrs.get("fee_configs"):
            serializer = CollectFeeConfigSerializer(
                data=attrs.get("fee_config"), many=True
            )
            serializer.is_valid(raise_exception=True)
        else:
            raise serializers.ValidationError("fee_configs is required")
        if attrs.get("discount_in") == "P":
            if attrs.get("discount") > 100 or attrs.get("discount") < 0:
                raise serializers.ValidationError(
                    "discount should be in between 0 and 100"
                )
        elif attrs.get("discount_in") == "A":
            if attrs.get("discount") < 0:
                raise serializers.ValidationError(
                    "discount amount should not be negative value"
                )
        return attrs
