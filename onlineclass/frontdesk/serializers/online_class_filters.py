from rest_framework import serializers


class OnlineclassFilterSerializer(serializers.Serializer):
    section__name = serializers.CharField(read_only=True)
    section__id = serializers.CharField(read_only=True)
    grade__name = serializers.CharField(read_only=True)
    grade__id = serializers.CharField(read_only=True)
