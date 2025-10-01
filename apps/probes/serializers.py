from rest_framework import serializers
from .models import Probe, Direction

class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = ["id", "pos_x", "pos_y", "direction", "mesh_x", "mesh_y", "created_at"]
        read_only_fields = ["id", "pos_x", "pos_y", "created_at"]

class ProbeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = ["direction", "mesh_x", "mesh_y"]

    def create(self, validated_data):
        return Probe.objects.create(
            pos_x=0,
            pos_y=0,
            **validated_data
        )

class ProbeMoveSerializer(serializers.Serializer):
    commands = serializers.CharField(max_length=100)