from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.employee_routes import employee_router
from .routes.auth_routes import router as auth_router


def create_app():
    app = FastAPI(
        title="Employee Management API",
        description="A simple Employee Management System API built with FastAPI",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(employee_router, prefix="/api/v1")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)