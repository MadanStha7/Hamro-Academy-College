from student.models import StudentInfo
from staff.administrator.serializers.staff import UserSerializer
from rest_framework import serializers


class StudentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category_name = serializers.CharField(read_only=True)
    student_first_name = serializers.CharField(read_only=True, source="user.first_name")
    student_last_name = serializers.CharField(read_only=True, source="user.last_name")
    blood_group_display = serializers.CharField(
        read_only=True, source="get_blood_group_display"
    )
    religion_display = serializers.CharField(
        read_only=True, source="get_religion_display"
    )
    gender_display = serializers.CharField(read_only=True, source="get_gender_display")
    photo = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentInfo
        read_only_fields = [
            "institution",
            "created_by",
            "created_on",
            "admission_number",
        ]
        fields = [
            "id",
            "photo",
            "admission_number",
            "user",
            "student_first_name",
            "student_last_name",
            "permanent_address",
            "temporary_address",
            "dob",
            "gender",
            "gender_display",
            "blood_group",
            "blood_group_display",
            "religion",
            "religion_display",
            "student_category",
            "category_name",
            "guardian_detail",
            "disable",
            "institution",
            "created_by",
            "created_on",
        ]
