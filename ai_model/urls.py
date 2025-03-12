from django.urls import path
from .views import IdentifyPlantView, DiagnosePlantView, UserImagesView

urlpatterns = [
    path("identify/", IdentifyPlantView.as_view(), name="identify_plant"),
    path("diagnose/", DiagnosePlantView.as_view(), name="diagnose_plant"),
    path("user-images/", UserImagesView.as_view(), name="user-images"),

]
