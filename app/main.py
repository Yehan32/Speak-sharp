"""
VocalLabs Backend API - Main Application Entry Point
A modern speech analysis and feedback system for Toastmasters and public speakers
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import tempfile
import os
from typing import Optional

from app.core.config import get_settings
from app.services.speech_analyzer_service import SpeechAnalyzerService
from app.services.firebase_service import FirebaseService
from app.utils.logger import get_logger

# Initialize settings and logger
settings = get_settings()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Speak Sharp API",
    description="AI-Powered Speech Analysis and Feedback Platform",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
speech_service = SpeechAnalyzerService()
firebase_service = FirebaseService()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Speak Sharp API starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Speak Sharp API shutting down...")


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "online",
        "service": "Speak Sharp API",
        "version": "2.0.0",
        "message": "Speech Analysis API is running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "ml_engine": "operational",
            "firebase": "operational"
        }
    }


@app.post("/api/v2/analyze")
async def analyze_speech(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    topic: str = Form(...),
    speech_type: str = Form(...),
    expected_duration: str = Form(...),
    actual_duration: str = Form(...),
    gender: Optional[str] = Form(None)
):
    """
    Analyze uploaded speech audio
    
    Args:
        file: Audio file (wav, mp3, m4a, ogg)
        user_id: User identifier
        topic: Speech topic
        speech_type: Type of speech
        expected_duration: Expected duration range (e.g., "5-7 minutes")
        actual_duration: Actual recording duration
        gender: Speaker gender (optional, auto-detected if not provided)
    
    Returns:
        Comprehensive speech analysis results
    """
    temp_file_path = None
    
    try:
        logger.info(f"Received analysis request from user: {user_id}")
        logger.info(f"Topic: {topic}, Type: {speech_type}")
        
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.wav', '.mp3', '.m4a', '.ogg']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: .wav, .mp3, .m4a, .ogg"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Saved temporary file: {temp_file_path}")
        
        # Perform speech analysis
        logger.info("Starting speech analysis...")
        analysis_result = await speech_service.analyze_speech(
            audio_path=temp_file_path,
            user_id=user_id,
            topic=topic,
            speech_type=speech_type,
            expected_duration=expected_duration,
            actual_duration=actual_duration,
            gender=gender or 'auto'
        )
        
        logger.info("Analysis completed successfully")
        
        # Upload audio to Firebase Storage
        logger.info("Uploading audio to Firebase...")
        audio_url = await firebase_service.upload_audio(
            file_path=temp_file_path,
            user_id=user_id,
            filename=file.filename
        )
        analysis_result['audio_url'] = audio_url
        
        # Save analysis to Firestore
        logger.info("Saving analysis to Firestore...")
        await firebase_service.save_speech_analysis(
            user_id=user_id,
            analysis_data=analysis_result,
            topic=topic,
            speech_type=speech_type,
            actual_duration=actual_duration
        )
        
        logger.info("Speech analysis pipeline completed successfully")
        
        return JSONResponse(content=analysis_result, status_code=200)
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file: {e}")


@app.post("/api/v2/quick-analyze")
async def quick_analyze(
    file: UploadFile = File(...),
    gender: Optional[str] = Form(None)
):
    """
    Quick speech analysis without saving to database
    Useful for testing and preview
    """
    temp_file_path = None
    
    try:
        # Save file temporarily
        file_ext = Path(file.filename).suffix.lower() if file.filename else '.wav'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        # Quick analysis (subset of full analysis)
        result = await speech_service.quick_analyze(
            audio_path=temp_file_path,
            gender=gender or 'auto'
        )
        
        return JSONResponse(content=result, status_code=200)
    
    except Exception as e:
        logger.error(f"Quick analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass


@app.get("/api/v2/user/{user_id}/speeches")
async def get_user_speeches(user_id: str, limit: int = 20):
    """Retrieve user's speech history"""
    try:
        speeches = await firebase_service.get_user_speeches(user_id, limit=limit)
        return JSONResponse(content={"speeches": speeches}, status_code=200)
    except Exception as e:
        logger.error(f"Failed to retrieve speeches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v2/user/{user_id}/stats")
async def get_user_stats(user_id: str):
    """Get user statistics and progress"""
    try:
        stats = await firebase_service.get_user_statistics(user_id)
        return JSONResponse(content=stats, status_code=200)
    except Exception as e:
        logger.error(f"Failed to retrieve stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
