"""
FastAPI server for ML-based restaurant recommendations
Enhanced with collaborative filtering, search matching, and AI data fetching
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    # Load .env file from python_ml directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded .env file from: {env_path}")
    else:
        # Try loading from current directory
        load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables only.")

# Add parent directory to path to import ml_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.enhanced_recommendation_engine import EnhancedRecommendationEngine
from ml_engine.voice_extractor import VoicePreferenceExtractor

app = FastAPI(title="Mood Munchies ML API", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9002", "http://127.0.0.1:9002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize enhanced recommendation engine
RESTAURANTS_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data',
    'restaurants.json'
)

# Get API keys from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Debug: Print API key status (without showing actual keys)
print("\n=== API Keys Status ===")
if OPENAI_API_KEY:
    print(f"  - OpenAI API Key: Found (length: {len(OPENAI_API_KEY)}, starts with: {OPENAI_API_KEY[:7]}...)")
else:
    print("  - OpenAI API Key: Not found")
if GEMINI_API_KEY:
    print(f"  - Gemini API Key: Found (length: {len(GEMINI_API_KEY)}, starts with: {GEMINI_API_KEY[:7]}...)")
else:
    print("  - Gemini API Key: Not found")
print("======================\n")

try:
    engine = EnhancedRecommendationEngine(
        restaurants_data_path=RESTAURANTS_DATA_PATH,
        user_data_path=None,  # Will use default path
        openai_api_key=OPENAI_API_KEY,
        gemini_api_key=GEMINI_API_KEY
    )
    print("Enhanced recommendation engine initialized successfully")
    
    # Check actual client status from AI fetcher
    if hasattr(engine, 'ai_fetcher'):
        if engine.ai_fetcher.openai_client:
            print("  - OpenAI API: Available and initialized")
        elif engine.ai_fetcher.openai_api_key:
            print(f"  - OpenAI API: Key found but client not initialized (check key validity)")
        
        if engine.ai_fetcher.gemini_model:
            print("  - Gemini API: Available and initialized")
        elif engine.ai_fetcher.gemini_api_key:
            print(f"  - Gemini API: Key found but client not initialized (check key validity)")
        
        if not engine.ai_fetcher.openai_client and not engine.ai_fetcher.gemini_model:
            print("  - AI APIs: Not available (will use local data only)")
            if not OPENAI_API_KEY and not GEMINI_API_KEY:
                print("    → No API keys found in environment variables")
            else:
                print("    → API keys found but clients failed to initialize")
                print("    → Check if API keys are valid and packages are installed")
    
    # Initialize voice preference extractor
    voice_extractor = VoicePreferenceExtractor(
        ai_fetcher=engine.ai_fetcher if hasattr(engine, 'ai_fetcher') else None
    )
    print("Voice preference extractor initialized")
except Exception as e:
    print(f"Error initializing recommendation engine: {e}")
    import traceback
    traceback.print_exc()
    engine = None
    voice_extractor = None


class RecommendationRequest(BaseModel):
    """Request model for recommendations"""
    mood: str
    occasion: str
    cuisine: str
    dietaryPreference: str
    time: str
    location: str
    additionalNotes: Optional[str] = None
    userId: Optional[str] = None
    searchQuery: Optional[str] = None
    useAiFetch: Optional[bool] = True


class RecommendationItem(BaseModel):
    """Individual recommendation item"""
    restaurantName: str
    foodSuggestion: str
    reasonForRecommendation: str
    location: str
    address: str
    contactDetails: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    recommendations: List[RecommendationItem]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mood Munchies ML Recommendation API",
        "version": "2.0.0",
        "features": [
            "content-based filtering",
            "collaborative filtering",
            "search query matching",
            "AI data fetching"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    api_status = {}
    if engine and hasattr(engine, 'ai_fetcher'):
        api_status = {
            "openai_available": engine.ai_fetcher.openai_client is not None,
            "gemini_available": engine.ai_fetcher.gemini_model is not None,
            "openai_key_set": bool(engine.ai_fetcher.openai_api_key),
            "gemini_key_set": bool(engine.ai_fetcher.gemini_api_key),
        }
    return {
        "status": "healthy",
        "engine_loaded": engine is not None,
        "api_status": api_status
    }


@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Generate restaurant recommendations using hybrid ML approach:
    - Content-based filtering (mood, occasion, cuisine)
    - Collaborative filtering (user-based, if userId provided)
    - Search query matching (if searchQuery provided)
    - AI data fetching (if enabled and needed)
    
    Args:
        request: RecommendationRequest with user preferences
    
    Returns:
        RecommendationResponse with list of recommendations
    """
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation engine is not available"
        )
    
    try:
        # Get recommendations from enhanced ML engine
        scored_recommendations = engine.recommend(
            mood=request.mood,
            occasion=request.occasion,
            cuisine=request.cuisine,
            dietary_preference=request.dietaryPreference,
            time=request.time,
            location=request.location,
            additional_notes=request.additionalNotes,
            user_id=request.userId,
            search_query=request.searchQuery,
            use_ai_fetch=request.useAiFetch if request.useAiFetch is not None else True
        )
        
        # Format recommendations
        formatted = engine.format_recommendations(
            scored_recommendations,
            mood=request.mood,
            occasion=request.occasion
        )
        
        # Convert to response model
        recommendations = [
            RecommendationItem(**rec) for rec in formatted
        ]
        
        return RecommendationResponse(recommendations=recommendations)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


class SearchRequest(BaseModel):
    """Request model for search queries"""
    query: str
    location: Optional[str] = None
    userId: Optional[str] = None


@app.post("/api/search", response_model=RecommendationResponse)
async def search_restaurants(request: SearchRequest):
    """
    Search restaurants by text query with AI-powered matching
    
    Args:
        request: SearchRequest with query text
    
    Returns:
        RecommendationResponse with matching restaurants
    """
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation engine is not available"
        )
    
    try:
        # Use search matcher to find restaurants
        search_results = engine.search_matcher.search(request.query, top_k=9)
        
        # If search query contains preferences, extract them
        query_prefs = engine.search_matcher.match_query_to_preferences(request.query)
        
        # Get recommendations with extracted preferences
        scored_recommendations = engine.recommend(
            mood=query_prefs.get('mood', 'happy'),
            occasion=query_prefs.get('occasion', 'casual meal'),
            cuisine=query_prefs.get('cuisine', 'any'),
            dietary_preference=query_prefs.get('dietary', 'non-vegetarian'),
            time='dinner',  # Default
            location=request.location,
            search_query=request.query,
            user_id=request.userId,
            use_ai_fetch=True
        )
        
        # Format recommendations
        formatted = engine.format_recommendations(
            scored_recommendations,
            mood=query_prefs.get('mood', ''),
            occasion=query_prefs.get('occasion', '')
        )
        
        recommendations = [
            RecommendationItem(**rec) for rec in formatted
        ]
        
        return RecommendationResponse(recommendations=recommendations)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching restaurants: {str(e)}"
        )


class VoiceExtractRequest(BaseModel):
    """Request model for voice preference extraction"""
    transcript: str
    useAi: Optional[bool] = True


@app.post("/api/voice/extract-preferences")
async def extract_voice_preferences(request: VoiceExtractRequest):
    """
    Extract preferences from voice transcript
    
    Args:
        request: VoiceExtractRequest with transcript text
    
    Returns:
        Dictionary with extracted preferences
    """
    if voice_extractor is None:
        raise HTTPException(
            status_code=503,
            detail="Voice extractor is not available"
        )
    
    try:
        preferences = voice_extractor.extract_preferences(
            transcript=request.transcript,
            use_ai=request.useAi if request.useAi is not None else True
        )
        
        return preferences
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting preferences: {str(e)}"
        )


class InteractionRequest(BaseModel):
    """Request model for tracking user interactions"""
    userId: str
    restaurantId: int
    rating: Optional[float] = None
    clicked: Optional[bool] = False
    viewed: Optional[bool] = False


@app.post("/api/interactions")
async def track_interaction(request: InteractionRequest):
    """
    Track user interaction for collaborative filtering
    
    Args:
        request: InteractionRequest with user interaction data
    
    Returns:
        Success message
    """
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation engine is not available"
        )
    
    try:
        engine.track_interaction(
            user_id=request.userId,
            restaurant_id=request.restaurantId,
            rating=request.rating,
            clicked=request.clicked,
            viewed=request.viewed
        )
        
        return {"status": "success", "message": "Interaction tracked"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error tracking interaction: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

