from fastapi import FastAPI

def create_app():
    app = FastAPI()

    from app.routes import router
    app.include_router(router)

    return app
