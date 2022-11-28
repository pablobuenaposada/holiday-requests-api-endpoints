from rest_framework import serializers


class RemainingOutputSerializer(serializers.Serializer):
    days = serializers.IntegerField(min_value=0)
