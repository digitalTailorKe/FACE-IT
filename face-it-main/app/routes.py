from fastapi import APIRouter, Form,  UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.face_recognition import  compare_faces
from app.face_verification import verify_faces, load_image_with_opencv


router = APIRouter()

@router.post("/verify")
async def compare_faces_endpoint(known_image: UploadFile = File(...), compared_image: UploadFile = File(...), similarity_percentage: float = Form(0.6)):
    if not known_image or not compared_image:
        raise HTTPException(status_code=400, detail="Missing image files")

    known_image_data = known_image.file
    compared_image_data = compared_image.file
    
    imageLoad1 = load_image_with_opencv(known_image_data)
    imageLoad2 = load_image_with_opencv(compared_image_data)
    
    response = verify_faces(imageLoad1, imageLoad2, similarity_percentage)
    try:
        return JSONResponse(content={"status": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/compare_pictures")
async def face_comparison(
    first_image: UploadFile = File(...), 
    second_image: UploadFile = File(...),
    tolerance: float = Form(0.6)):
        
    if not first_image or not second_image:
        raise HTTPException(status_code=400, detail="Missing image files")

    try:
        # Asynchronously read the image files as binary data
        first_image_data = await first_image.read()
        second_image_data = await second_image.read()

        # Pass the binary data to the compare_faces function
        comparison_result = compare_faces(first_image_data, second_image_data, tolerance)
        
        # Return both matching and distance in the response
        return JSONResponse(content=comparison_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
