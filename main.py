from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.campaign import router as campaign_router
from app.api.voice import router as voice_router
from app.api.twilio import router as twilio_router

app = FastAPI()

app.include_router(campaign_router, prefix="/api")
app.include_router(voice_router, prefix="/api")
app.include_router(twilio_router, prefix="/api/twilio")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
