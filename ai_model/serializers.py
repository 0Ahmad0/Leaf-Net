from rest_framework import serializers
from .models import PlantDiagnosis


class PlantDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantDiagnosis
        fields = ["image", "plant_name", "disease", "confidence", "treatment", "created_at"]
