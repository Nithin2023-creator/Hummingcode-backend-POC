from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users

app = FastAPI()

# Enable CORS (Adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI + React App"}
