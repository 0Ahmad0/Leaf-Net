from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PlantDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="compressed_images/")
    plant_name = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    confidence = models.FloatField()
    treatment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant_name} - {self.disease}"
