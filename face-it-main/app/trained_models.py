from deepface import DeepFace

# List of models to download
models = ["Facenet512"]

# Download each model
for model_name in models:
    print(f"Downloading model: {model_name}")
    model = DeepFace.build_model(model_name)
    print(f"{model_name} model is downloaded and loaded.")
