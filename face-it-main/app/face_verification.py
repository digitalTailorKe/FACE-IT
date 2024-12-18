import cv2
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from flask import json
import numpy as np
from deepface import DeepFace
import tensorflow as tf
from tensorflow.python.framework.ops import disable_eager_execution

# tf.config.threading.set_intra_op_parallelism_threads(2)
# tf.config.threading.set_inter_op_parallelism_threads(2)

# tf.config.optimizer.set_jit(True)  # Enable XLA
# disable_eager_execution()

models = ["Facenet512"]
backends = ['retinaface']
alignment_modes = [True, False]

def load_image_with_opencv(file):
    try:
        # Convert file to bytes and then to a NumPy array
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        
        # Decode the image array
        image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Check if the image was loaded successfully
        if image_array is None:
            raise ValueError("Unsupported image format or image could not be read")
        
        return image_array
    except Exception as e:
        raise ValueError(f"Unsupported image format: {e}")
    
def extract_faces(known_image_data, compared_image_data):
    print("extracting faces")

    # Check if images are provided
    if known_image_data is None or known_image_data.size == 0:
        raise HTTPException(status_code=400, detail="No known image provided")
    if compared_image_data is None or compared_image_data.size == 0:
        raise HTTPException(status_code=400, detail="No comparison image provided")
    
    print("extracting face3")

    # Extract faces with DeepFace
    face_obj_known = DeepFace.extract_faces(img_path=known_image_data, anti_spoofing=True, detector_backend=backends[0], align=alignment_modes[0], enforce_detection=False)
    face_obj_of_comparison = DeepFace.extract_faces(img_path=compared_image_data, anti_spoofing=True, detector_backend=backends[0], align=alignment_modes[0], enforce_detection=False)

    print(face_obj_known)
    print(face_obj_of_comparison)
    print("extracting face4")

    # Check if faces were detected
    if not face_obj_known:
        raise HTTPException(status_code=404, detail="No face detected in known image")
    if not face_obj_of_comparison:
        raise HTTPException(status_code=404, detail="No face detected in comparison image")
    print("extracting face5")
    
    try:
        # Handle spoofing detection
        if face_obj_of_comparison[0].get("is_real") is False:
            return JSONResponse(content={"response": "Spoof attack detected on image2" })
    except Exception as e:
        # Add a more specific handling for exceptions if needed
        return JSONResponse(content={"response": f"Error during face extraction: {str(e)}"})

    # If everything is successful, return success message
    return JSONResponse(content={"response": "Face extracted successfully"})


def verify_faces(known_image, compared_image, similarity_percentage):
    response = extract_faces(known_image, compared_image)
    
    if response is None:
        raise HTTPException(status_code=500, detail="Face extraction failed")

    if isinstance(response, JSONResponse):
        # Decode and parse the response content to get the dictionary
        response_content = json.loads(response.body.decode("utf-8"))
        print(response_content, "Face extraction response")
        response_extract = response_content.get("response")

        # Check if the face extraction was successful
        if response_extract != "Face extracted successfully":
            raise HTTPException(status_code=400, detail=response_extract)
    else:
        raise HTTPException(status_code=500, detail="Invalid response type")
        
    # Perform face verification
    result = DeepFace.verify(
        known_image, 
        compared_image, 
        model_name=models[0],
        detector_backend=backends[0],
        align=alignment_modes[0],
        anti_spoofing=True,
        enforce_detection=False,
        expand_percentage=50,
        silent=True
    )

    print(result)
    
    # Custom response formatting
    ai_response = {
        "verified": result["verified"],
        "distance": result["distance"],
        "similarity_metric": result["similarity_metric"],
        "time": result.get("time", 0.0)
    }

    distance = ai_response["distance"]

    # If distance is negative or very close to zero, treat it as zero
    if distance < 0:
        distance = 0

    # Calculate percentage distance and similarity percentage
    overall = 1 - distance
    current_percentage = overall * 100

    # Ensure the similarity percentage is bounded between 0 and 100
    current_percentage = max(0, min(current_percentage, 100))

    # Set verification based on similarity percentage
    percentage_verification = current_percentage >= similarity_percentage

    # Format the match response
    match_response = {
        "verified": percentage_verification,
        "distance": result["distance"],
        "percentage_distance": current_percentage,
        "percentage_verification": percentage_verification,
        "similarity_metric": result["similarity_metric"],
        "time": result.get("time", 0.0)
    }

    return {"match": match_response}

