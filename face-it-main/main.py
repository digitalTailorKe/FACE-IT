from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    # Correct way to run a FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # reload=True for dev environment
