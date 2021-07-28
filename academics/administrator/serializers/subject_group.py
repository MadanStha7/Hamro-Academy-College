from django.db import transaction
from rest_framework import serializers

from academics.administrator.serializers.section import SectionSerializer
from academics.administrator.serializers.subject import SubjectSerializer
from academics.models import SubjectGroup


class SubjectGroupSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True, many=True)
    section = SectionSerializer(read_only=True, many=True)
    grade_name = serializers.CharField(source="grade.get_name_display", read_only=True)

    class Meta:
        model = SubjectGroup
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "subject",
            "section",
            "grade",
            "faculty",
            "grade_name",
            "description",
            "created_by",
            "institution",
        ]

    def validate_name(self, name):
        if not self.instance:
            if SubjectGroup.objects.filter(name=name.title()).exists():
                raise serializers.ValidationError("Subject name is already exists")
        return name

    def validate_subject(self, subject):
        if SubjectGroup.objects.filter(subject=subject.title()).exists():
            raise serializers.ValidationError(
                "Subject Group with subject is already exists"
            )
        return subject

    @transaction.atomic
    def create(self, validated_data):
        subject = validated_data.pop("subject")
        section = validated_data.pop("section")
        subject_obj = SubjectGroup.objects.create(**validated_data)
        subject_obj.subject.set(subject)
        if section:
            subject_obj.section.set(section)
        subject_obj.save()
        return subject_obj

    def update(self, instance, validated_data):
        subject = validated_data.pop("subject")
        instance.name = validated_data.get("name", instance.name)
        instance.name = validated_data.get("section", instance.name)
        instance.garde = validated_data.get("grade", instance.grade)
        instance.faculty = validated_data.get("faculty", instance.grade)
        instance.description = validated_data.get("description")
        instance.subject.set(subject)
        instance.save()
        return instance
