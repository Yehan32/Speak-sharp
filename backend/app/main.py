import os
import whisper
import librosa
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import traceback
from dotenv import load_dotenv

# Import all our ML models
from app.models import (
    filler_word_detection,
    proficiency_evaluation,
    transcript,
    voice_modulation,
    speech_development,
    speech_effectiveness,
    vocabulary_evaluation
)

# Import Firebase
from app.firebase_config import db

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="VocalLabs API",
    description="Speech analysis and feedback API",
    version="1.0.0"
)

# Configure CORS (allows Flutter app to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for Whisper model
whisper_model = None

@app.on_event("startup")
async def startup_event():
    """Load Whisper model when server starts"""
    global whisper_model
    print("Loading Whisper model...")
    try:
        # Load Whisper base model (good balance of speed and accuracy)
        whisper_model = whisper.load_model("base")
        print("Whisper model loaded successfully!")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint - simple health check"""
    return {
        "message": "VocalLabs API is running!",
        "status": "healthy",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "whisper_model_loaded": whisper_model is not None,
        "firebase_connected": True  # Assumes firebase_config.py ran successfully
    }

@app.post("/analyze")
async def analyze_speech(
    audio: UploadFile = File(...),
    topic: str = Form(...),
    expected_duration: str = Form(...),
    user_id: str = Form(...)
):
    """
    Main endpoint to analyze speech.
    
    Args:
        audio: Audio file (WAV, MP3, etc.)
        topic: Speech topic/title
        expected_duration: Expected duration (e.g., "5-7 minutes")
        user_id: Firebase user ID
        
    Returns:
        Complete analysis with scores and feedback
    """
    temp_audio_path = None
    
    try:
        # Validate inputs
        if not audio.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")
        
        # Check file extension
        allowed_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
        file_ext = os.path.splitext(audio.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        print(f"\n{'='*50}")
        print(f"Starting analysis for user: {user_id}")
        print(f"Topic: {topic}")
        print(f"Expected duration: {expected_duration}")
        print(f"{'='*50}\n")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_audio_path = temp_file.name
            content = await audio.read()
            temp_file.write(content)
        
        print(f"Audio file saved to: {temp_audio_path}")
        
        # === STEP 1: TRANSCRIPTION ===
        print("\nStep 1: Transcribing audio...")
        transcription_result = transcript.transcribe_audio(whisper_model, temp_audio_path)
        transcription_with_pauses, number_of_pauses = transcript.process_transcription(transcription_result)
        print(f"Transcription complete. Found {number_of_pauses} pauses.")
        
        # === STEP 2: GET AUDIO DURATION ===
        print("\nStep 2: Getting audio duration...")
        y, sr = librosa.load(temp_audio_path)
        actual_duration = librosa.get_duration(y=y, sr=sr)
        actual_duration_str = f"{int(actual_duration // 60)}:{int(actual_duration % 60):02d}"
        print(f" Duration: {actual_duration_str} ({actual_duration:.1f} seconds)")
        
        # === STEP 3: FILLER WORD ANALYSIS ===
        print("\nStep 3: Analyzing filler words...")
        filler_analysis = filler_word_detection.analyze_filler_words(transcription_result)
        print(f"Found {filler_analysis['Total Filler Words']} filler words")
        
        # === STEP 4: PAUSE ANALYSIS ===
        print("\nStep 4: Analyzing pauses...")
        pause_analysis = filler_word_detection.analyze_mid_sentence_pauses(transcription_with_pauses)
        print(f"Pause analysis complete")
        
        # === STEP 5: PROFICIENCY SCORE ===
        print("\nStep 5: Calculating proficiency score...")
        proficiency_result = proficiency_evaluation.calculate_proficiency_score(
            filler_analysis,
            pause_analysis,
            actual_duration_str,
            expected_duration
        )
        print(f"Proficiency score: {proficiency_result['final_score']}/20")
        
        # === STEP 6: VOICE MODULATION ===
        print("\nStep 6: Analyzing voice modulation...")
        modulation_result = voice_modulation.analyze_voice_modulation(temp_audio_path)
        
        if 'error' in modulation_result:
            print(f"Voice modulation error: {modulation_result['error']}")
            modulation_score = 10.0  # Default score
        else:
            modulation_score = modulation_result['scores']['total_score']
            print(f"Voice modulation score: {modulation_score}/20")
        
        # === STEP 7: SPEECH DEVELOPMENT ===
        print("\nStep 7: Evaluating speech development...")
        development_result = speech_development.evaluate_speech_development(
            transcription_with_pauses,
            actual_duration,
            expected_duration
        )
        development_score = development_result['structure']['score'] + development_result['time_utilization']['score']
        print(f"Speech development score: {development_score}/20")
        
        # === STEP 8: SPEECH EFFECTIVENESS ===
        print("\nStep 8: Evaluating speech effectiveness...")
        effectiveness_result = speech_effectiveness.evaluate_speech_effectiveness(
            transcription_with_pauses,
            topic,
            expected_duration,
            actual_duration
        )
        effectiveness_score = effectiveness_result['total_score']
        print(f"Speech effectiveness score: {effectiveness_score}/20")
        
        # === STEP 9: VOCABULARY EVALUATION ===
        print("\nStep 9: Evaluating vocabulary...")
        vocabulary_result = vocabulary_evaluation.evaluate_speech(
            transcription_result,
            transcription_with_pauses,
            temp_audio_path,
            topic
        )
        # Convert from 0-100 scale to 0-20 scale
        vocabulary_score = (vocabulary_result['vocabulary_score'] / 100) * 20
        print(f"Vocabulary score: {vocabulary_score}/20")
        
        # === STEP 10: CALCULATE OVERALL SCORE ===
        print("\nStep 10: Calculating overall score...")
        overall_score = (
            proficiency_result['final_score'] +
            modulation_score +
            development_score +
            effectiveness_score +
            vocabulary_score
        )
        print(f"Overall score: {overall_score}/100")
        
        # === STEP 11: COMPILE RESULTS ===
        print("\n Step 11: Compiling results...")
        
        results = {
            "overall_score": round(overall_score, 1),
            "scores": {
                "proficiency": round(proficiency_result['final_score'], 1),
                "voice_modulation": round(modulation_score, 1),
                "speech_development": round(development_score, 1),
                "speech_effectiveness": round(effectiveness_score, 1),
                "vocabulary": round(vocabulary_score, 1)
            },
            "transcription": transcription_with_pauses,
            "duration": {
                "actual": actual_duration_str,
                "expected": expected_duration,
                "seconds": round(actual_duration, 1)
            },
            "filler_analysis": {
                "total_filler_words": filler_analysis['Total Filler Words'],
                "filler_density": round(filler_analysis['Filler Density'], 3),
                "filler_per_minute": filler_analysis['Filler Words Per Minute']
            },
            "pause_analysis": pause_analysis,
            "proficiency_details": proficiency_result,
            "voice_modulation_details": modulation_result if 'error' not in modulation_result else {},
            "speech_development_details": development_result,
            "speech_effectiveness_details": effectiveness_result,
            "vocabulary_details": {
                "lexical_diversity": vocabulary_result.get('lexical_diversity', 0),
                "unique_words": vocabulary_result.get('unique_words', 0),
                "advanced_vocab_count": vocabulary_result.get('advanced_vocab_count', 0),
                "feedback": vocabulary_result.get('feedback', [])
            },
            "topic": topic,
            "user_id": user_id
        }
        
        print(f"\n{'='*50}")
        print("ANALYSIS COMPLETE!")
        print(f"{'='*50}\n")
        
        # === STEP 12: SAVE TO FIREBASE (OPTIONAL) ===
        # Uncomment if you want to save results to Firestore
        # try:
        #     doc_ref = db.collection('speeches').add(results)
        #     print(f"Saved to Firebase with ID: {doc_ref[1].id}")
        # except Exception as e:
        #     print(f" Firebase save error: {e}")
        
        return JSONResponse(content=results)
        
    except Exception as e:
        # Log the full error
        print(f"\nERROR in analysis:")
        print(traceback.format_exc())
        
        # Return error response
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
        
    finally:
        # Clean up temporary file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.unlink(temp_audio_path)
                print(f"Cleaned up temporary file")
            except Exception as e:
                print(f" Could not delete temp file: {e}")

@app.post("/save-speech")
async def save_speech_to_firebase(
    user_id: str = Form(...),
    speech_data: str = Form(...)
):
    """
    Save speech analysis to Firebase Firestore.
    
    Args:
        user_id: Firebase user ID
        speech_data: JSON string of speech data
        
    Returns:
        Success message with document ID
    """
    try:
        import json
        data = json.loads(speech_data)
        
        # Add to Firestore
        doc_ref = db.collection('speeches').document()
        doc_ref.set({
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP,
            **data
        })
        
        return {
            "success": True,
            "document_id": doc_ref.id,
            "message": "Speech saved successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save speech: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)