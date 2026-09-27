from rest_framework import serializers
from rest_framework.serializers import Serializer


class DownloadSerializer(Serializer):
    format=serializers.CharField()
    link=serializers.CharField()
    resolution=serializers.CharField(required=False)