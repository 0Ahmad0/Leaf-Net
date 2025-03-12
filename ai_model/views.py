from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import PlantDiagnosis
from .serializers import PlantDiagnosisSerializer
from .services.cnn_model import predict_plant_disease


class IdentifyPlantView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """API to identify plant name from an uploaded image"""
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']

        try:
            result = predict_plant_disease(image, request.user)
            return Response({
                "plant_name": result["plant_name"],
                "confidence": result["confidence"]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DiagnosePlantView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """API to diagnose plant disease from an uploaded image"""
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']

        try:
            result = predict_plant_disease(image, request.user)
            return Response({
                "plant_name": result["plant_name"],
                "disease": result["disease"],
                "confidence": result["confidence"],
                "treatment": result["treatment"]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserImagesView(APIView):
    """API to get all images uploaded by a specific user"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        images = PlantDiagnosis.objects.filter(user=request.user)
        serializer = PlantDiagnosisSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)