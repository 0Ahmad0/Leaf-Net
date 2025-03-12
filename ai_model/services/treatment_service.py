TREATMENT_DATABASE = {
    "Bacterial spot": "Use copper-based fungicides and avoid overhead watering.",
    "Early blight": "Apply fungicides containing chlorothalonil or copper.",
    "Late blight": "Remove infected plants immediately and apply systemic fungicides.",
    "Leaf Mold": "Ensure proper ventilation and apply sulfur-based fungicides.",
    "Septoria leaf spot": "Use copper sprays and rotate crops regularly.",
    "Spider mites Two spotted spider mite": "Spray neem oil or insecticidal soap.",
    "Target Spot": "Remove affected leaves and apply copper-based fungicides.",
    "Tomato YellowLeaf Curl Virus": "Control whiteflies with insecticidal soap or neem oil.",
    "Tomato mosaic virus": "Destroy infected plants and sanitize tools.",
}


def get_treatment(disease_name):
    """Returns the treatment recommendation for a given disease"""
    return TREATMENT_DATABASE.get(disease_name, "No specific treatment available. Consult an expert.")
