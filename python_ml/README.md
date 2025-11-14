# Mood Munchies - Python ML Recommendation System

This directory contains the Python-based ML recommendation system that replaces the Genkit/Gemini AI implementation.

## Overview

The ML recommendation system uses:
- **Content-based filtering** based on mood, occasion, cuisine, and dietary preferences
- **Collaborative filtering** for user-based recommendations
- **Search query matching** for text-based restaurant search
- **AI data fetching** using OpenAI to enrich restaurant database
- **Feature engineering** for mood mapping and preference scoring
- **TF-IDF vectorization** for text-based similarity matching
- **Cosine similarity** for recommendation ranking
- **Hybrid weighted scoring** algorithm combining all methods

## Architecture

```
python_ml/
├── api/
│   └── main.py                      # FastAPI server
├── ml_engine/
│   ├── recommendation_engine.py      # Base content-based filtering
│   ├── enhanced_recommendation_engine.py  # Hybrid recommendation engine
│   ├── collaborative_filtering.py   # User-based collaborative filtering
│   ├── search_matcher.py            # Text search and query matching
│   └── ai_data_fetcher.py           # OpenAI-based data fetching
├── data/
│   ├── restaurants.json             # Base restaurant dataset
│   ├── user_interactions.json       # User interaction history (auto-created)
│   └── ai_fetched_restaurants.json  # AI-fetched restaurants (auto-created)
├── requirements.txt                # Python dependencies
├── README.md                        # This file
└── ENHANCED_FEATURES.md            # Detailed feature documentation
```

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (if needed):
```python
import nltk
nltk.download('stopwords')
```

## Running the API Server

Start the FastAPI server:
```bash
cd python_ml
python -m uvicorn api.main:app --reload --port 8000
```

Or use the main file directly:
```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Get Recommendations (Enhanced)
```
POST /api/recommendations
Content-Type: application/json

{
  "mood": "happy",
  "occasion": "casual meal",
  "cuisine": "italian",
  "dietaryPreference": "vegetarian",
  "time": "dinner",
  "location": "Downtown",
  "additionalNotes": "Looking for a quiet place",
  "userId": "user123",           // Optional: for collaborative filtering
  "searchQuery": "romantic Italian",  // Optional: for search matching
  "useAiFetch": true              // Optional: enable AI data fetching
}
```

### Search Restaurants
```
POST /api/search
Content-Type: application/json

{
  "query": "Italian restaurant for date night",
  "location": "Downtown",  // Optional
  "userId": "user123"      // Optional
}
```

### Track User Interaction
```
POST /api/interactions
Content-Type: application/json

{
  "userId": "user123",
  "restaurantId": 1,
  "rating": 4.5,      // Optional: 0-5
  "clicked": true,    // Optional
  "viewed": true      // Optional
}
```

Response:
```json
{
  "recommendations": [
    {
      "restaurantName": "Pizza Palace",
      "foodSuggestion": "Margherita Pizza",
      "reasonForRecommendation": "This is an excellent match for your preferences. perfect for your happy mood. ideal for casual meal.",
      "location": "Suburbia",
      "address": "212 Birch St, Anytown, USA",
      "contactDetails": "(555) 234-5678"
    },
    ...
  ]
}
```

## ML Algorithm Details

### Hybrid Scoring System

The enhanced recommendation engine combines multiple methods:

1. **Content-Based Filtering (40%)**:
   - Mood Score: Restaurant's mood compatibility matrix
   - Occasion Score: Restaurant's occasion compatibility
   - Time Score: Restaurant's time-of-day preferences
   - Cuisine Match: Exact match = 1.0, "any" = 1.0, mismatch = 0.3
   - Content Similarity: TF-IDF cosine similarity
   - Additional Notes Score: Keyword-based preference matching

2. **Collaborative Filtering (30%)**:
   - User similarity matrix based on interaction history
   - Recommendations from similar users
   - Weighted by user similarity scores

3. **Search Query Matching (20%)**:
   - Semantic similarity using TF-IDF (70%)
   - Keyword matching (30%)
   - Preference extraction from query text

4. **AI-Fetched Restaurants (10%)**:
   - New restaurants fetched using OpenAI
   - Automatically enriched with features
   - Stored for future recommendations

### Feature Engineering

- **Mood Mapping**: Each restaurant has mood scores (0-1) for different moods
- **Occasion Mapping**: Restaurants scored for different occasions
- **Time Mapping**: Restaurants scored for different meal times
- **Text Features**: Cuisine, ambiance, dishes, dietary options combined for TF-IDF

### Additional Notes Processing

The system extracts preferences from additional notes using keyword matching:
- Spicy, quiet, romantic, family-friendly, healthy, fast, affordable, upscale

## Restaurant Dataset

The `data/restaurants.json` file contains restaurant data with:
- Basic info (name, location, address, contact)
- Mood scores for different moods
- Occasion scores
- Time scores
- Dietary options
- Popular dishes
- Price range and ambiance

## Integration with Next.js

The Next.js frontend calls this Python API instead of the Genkit flows. See `src/app/actions.ts` for the integration.

## Enhanced Features

See [ENHANCED_FEATURES.md](./ENHANCED_FEATURES.md) for detailed documentation on:
- Collaborative filtering implementation
- Search query matching
- AI data fetching
- Hybrid recommendation algorithm
- API usage examples

## API Keys Setup

See [API_SETUP.md](./API_SETUP.md) for:
- Setting up Gemini and OpenAI API keys
- How the system uses API keys
- Data fetching and storage
- Troubleshooting

## Recent Improvements

See [IMPROVEMENTS.md](./IMPROVEMENTS.md) for:
- Better query matching
- Dual API support (Gemini & OpenAI)
- Smart deduplication
- Enhanced scoring algorithm

## Development

To add more restaurants, edit `data/restaurants.json` and ensure each restaurant has:
- Unique ID
- All required fields (moodScores, occasionScores, timeScores, etc.)
- At least one popular dish

To modify the scoring algorithm, edit `ml_engine/recommendation_engine.py` in the `recommend()` method.

## Testing

Test the API using curl:
```bash
curl -X POST "http://localhost:8000/api/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "happy",
    "occasion": "casual meal",
    "cuisine": "italian",
    "dietaryPreference": "vegetarian",
    "time": "dinner",
    "location": "Downtown"
  }'
```

Or use the FastAPI interactive docs at `http://localhost:8000/docs`

