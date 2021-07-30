from rest_framework import serializers
from academics.administrator.serializers.section import SectionSerializer
from academics.administrator.serializers.subject import SubjectSerializer
from academics.models import SubjectGroup, Subject, Section
from common.utils import return_grade_name_of_value, validate_unique_name


class SubjectGroupSerializer(serializers.ModelSerializer):
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject", write_only=True, many=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), source="section", write_only=True, many=True
    )
    subject = SubjectSerializer(read_only=True, many=True)
    section = SectionSerializer(read_only=True, many=True)
    name_value = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = SubjectGroup
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "name_value",
            "subject",
            "subject_id",
            "section",
            "section_id",
            "grade",
            "faculty",
            "description",
            "created_by",
            "institution",
        ]

    def to_representation(self, data):
        data = super(SubjectGroupSerializer, self).to_representation(data)
        data["name"] = return_grade_name_of_value(data["name"])
        return data

    def validate_name(self, name):
        name = validate_unique_name(
            SubjectGroup, name, self.context.get("institution"), self.instance
        )
        return name

    def validate(self, attrs):
        """
        check if the provided subject is same
        """
        no_of_section = []
        no_of_subject = []

        for item in attrs["subject"]:
            no_of_subject.append(item)

        for value in no_of_subject:
            if no_of_subject.count(value) > 1:
                raise serializers.ValidationError("Same Subject cannot be selected!")

        for item in attrs["section"]:
            no_of_section.append(item)

        for value in no_of_section:
            if no_of_section.count(value) > 1:
                raise serializers.ValidationError("Same Section cannot be selected!")

        return attrs

    def validate_subject_grade(self, subject, grade):
        institution = self.request.institution
        if SubjectGroup.objects.filter(
            subject=subject, grade__id=grade, institution=institution
        ).exists():
            raise serializers.ValidationError(
                "Subject Group with subject is already exists"
            )
        return subject

    # def validate(self, section):
    #     section_id = []
    #     for i in section:
    #         print(i)
    #         if i not in section_id:
    #             a = section_id.append(i)
    #             print(a)
    #     return section
    #     return list(self(section))
