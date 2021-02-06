from .models import *
from rest_framework import serializers

class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Videos
        fields='__all__'

class VideosTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model= VideosTopics
        fields='__all__'
 