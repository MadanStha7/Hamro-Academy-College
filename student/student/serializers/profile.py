from guardian.models import StudentGuardianInfo
from student.models import StudentAcademicDetail, StudentInfo
from staff.administrator.serializers.staff import UserSerializer
from rest_framework import serializers
from student.administator.serializer.previous_academic import PreviousAcademicSerializer


class StudentAcademicSerializer(serializers.ModelSerializer):

    section_name = serializers.CharField(read_only=True, source="section.name")
    grade_name = serializers.CharField(read_only=True, source="grade.name")
    faculty_name = serializers.CharField(read_only=True, source="faculty.name")
    shift_name = serializers.CharField(read_only=True, source="shift.name")

    class Meta:
        model = StudentAcademicDetail
        fields = [
            "grade_name",
            "section_name",
            "faculty_name",
            "shift_name",
        ]


class GuardianInfoSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    photo = serializers.SerializerMethodField(
        read_only=True, required=False, allow_null=True
    )
    relation_display = serializers.CharField(
        read_only=True, source="get_relation_display"
    )

    def get_photo(self, obj):
        return obj.photo.url if obj.photo else None

    class Meta:
        model = StudentGuardianInfo
        fields = [
            "user",
            "address",
            "relation",
            "relation_display",
            "photo",
            "occupation",
        ]


class StudentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
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
    student_academic_detail = StudentAcademicSerializer(many=True, read_only=True)
    previous_academic_detail = PreviousAcademicSerializer(many=True, read_only=True)

    guardian_detail = GuardianInfoSerializer(read_only=True)
    category_name = serializers.CharField(source="student_category.name")

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
            "student_academic_detail",
            "previous_academic_detail",
        ]
