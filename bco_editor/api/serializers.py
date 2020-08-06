from rest_framework import serializers
from .models import bco_object

class BcoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id', 'schema', 'payload', 'state']

class BcoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id', 'payload', 'schema', 'state']

class BcoPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id', 'payload', 'schema', 'state']

class BcoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id']