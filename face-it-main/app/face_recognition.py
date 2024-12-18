import face_recognition
from io import BytesIO

def compare_faces(known_image_data, unknown_image_data, tolerance):
    # Convert binary data to file-like object using BytesIO
    known_image_file = BytesIO(known_image_data)
    unknown_image_file = BytesIO(unknown_image_data)

    # Load the images from the file-like objects
    first_pic = face_recognition.load_image_file(known_image_file)
    known_face_encoding = face_recognition.face_encodings(first_pic)[0]

    second_pic = face_recognition.load_image_file(unknown_image_file)
    face_encoding_to_check = face_recognition.face_encodings(second_pic)[0]
    
   # Calculate face distance (NumPy float array) and convert to Python float
    distance = float(face_recognition.face_distance([known_face_encoding], face_encoding_to_check)[0])
    print(distance)
    
    # Compare faces (NumPy boolean array) and convert to Python bool
    results = face_recognition.compare_faces([known_face_encoding], face_encoding_to_check, tolerance=tolerance)
    print(results)
    
    
    # Return both matching result and distance
    return {"matching": bool(results[0]), "distance": distance}

