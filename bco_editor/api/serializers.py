from rest_framework import serializers
from .models import bco_object


# Model-based serializer for POST.
class BcoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id', 'schema', 'bco', 'state']


# Non-model based serializer for GET.
class BcoGetSerializer(serializers.Serializer):
    class Meta:
        model = bco_object
        fields = ['object_id']


# Non-model based serializer for PATCH.
class BcoPatchSerializer(serializers.Serializer):
    class Meta:
        model = bco_object
        fields = ['object_id']


# Model-based serializer for DELETE.
class BcoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = bco_object
        fields = ['object_id']