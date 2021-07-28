from rest_framework import serializers

from academics.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="get_subject_type_display", read_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Subject
        read_only_fields = ["created_by", "institution"]
        fields = [
            "id",
            "name",
            "credit_hour",
            "subject_code",
            "subject_type",
            "subject",
            "created_by",
            "institution",
        ]

    def validate_name(self, name):
        if not self.instance:
            if Subject.objects.filter(name=name.title()).exists():
                raise serializers.ValidationError("Subject name is already exists")
        return name
