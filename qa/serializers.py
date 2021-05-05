from rest_framework import serializers
from .models import Request, Correspondence


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'status', 'registration_date']


class CorrespondenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondence
        exclude = ['id']
