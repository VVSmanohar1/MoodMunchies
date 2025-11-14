# Enhanced ML Recommendation System Features

## Overview

The enhanced recommendation system now includes:
1. **Collaborative Filtering** - User-based recommendations
2. **Search Query Matching** - Text-based restaurant search
3. **AI Data Fetching** - OpenAI-powered restaurant data enrichment
4. **Hybrid Recommendation Engine** - Combines all methods for optimal results

## New Components

### 1. Collaborative Filtering (`collaborative_filtering.py`)

**Purpose**: Recommend restaurants based on similar users' preferences

**How it works**:
- Tracks user interactions (ratings, clicks, views)
- Builds user similarity matrix using cosine similarity
- Finds users with similar preferences
- Recommends restaurants liked by similar users

**Usage**:
```python
# Track user interaction
engine.track_interaction(
    user_id="user123",
    restaurant_id=1,
    rating=4.5,
    clicked=True,
    viewed=True
)

# Get collaborative recommendations
collab_results = collab_filter.get_collaborative_recommendations(
    user_id="user123",
    restaurants=all_restaurants,
    top_k=9
)
```

**Data Storage**: `data/user_interactions.json`

### 2. Search Query Matcher (`search_matcher.py`)

**Purpose**: Match text search queries to restaurants

**How it works**:
- Uses TF-IDF vectorization for semantic matching
- Keyword extraction and matching
- Extracts preferences from search queries (mood, occasion, cuisine)
- Combines semantic and keyword scores

**Usage**:
```python
# Search restaurants
results = search_matcher.search("Italian restaurant for date night", top_k=9)

# Extract preferences from query
prefs = search_matcher.match_query_to_preferences(
    "happy mood, vegetarian Italian food"
)
```

**Features**:
- Semantic similarity (70% weight)
- Keyword matching (30% weight)
- Automatic preference extraction

### 3. AI Data Fetcher (`ai_data_fetcher.py`)

**Purpose**: Fetch restaurant data using OpenAI API

**How it works**:
- Uses OpenAI GPT-4o-mini to generate restaurant information
- Fetches restaurants based on search queries
- Stores fetched data for future use
- Enriches restaurant database automatically

**Usage**:
```python
# Fetch restaurant data
restaurants = ai_fetcher.fetch_restaurant_data(
    query="Italian restaurants in downtown",
    location="Downtown",
    max_results=5
)

# Search in fetched data
matching = ai_fetcher.search_fetched_restaurants(
    query="pizza place",
    location="Downtown"
)
```

**Data Storage**: `data/ai_fetched_restaurants.json`

**Requirements**: OpenAI API key in `OPENAI_API_KEY` environment variable

### 4. Enhanced Recommendation Engine (`enhanced_recommendation_engine.py`)

**Purpose**: Combines all recommendation methods

**How it works**:
- Content-based filtering (40% weight)
- Collaborative filtering (30% weight)
- Search matching (20% weight)
- AI-fetched restaurants (10% weight)
- Dynamically adjusts weights based on available data

**Usage**:
```python
# Get hybrid recommendations
results = engine.recommend(
    mood="happy",
    occasion="date night",
    cuisine="italian",
    dietary_preference="vegetarian",
    time="dinner",
    location="Downtown",
    user_id="user123",  # For collaborative filtering
    search_query="romantic Italian restaurant",  # For search matching
    use_ai_fetch=True  # Enable AI data fetching
)
```

## API Endpoints

### 1. Enhanced Recommendations
```
POST /api/recommendations
```

**Request Body**:
```json
{
  "mood": "happy",
  "occasion": "date night",
  "cuisine": "italian",
  "dietaryPreference": "vegetarian",
  "time": "dinner",
  "location": "Downtown",
  "additionalNotes": "Looking for a quiet place",
  "userId": "user123",  // Optional: for collaborative filtering
  "searchQuery": "romantic Italian",  // Optional: for search matching
  "useAiFetch": true  // Optional: enable AI data fetching
}
```

### 2. Search Restaurants
```
POST /api/search
```

**Request Body**:
```json
{
  "query": "Italian restaurant for date night",
  "location": "Downtown",  // Optional
  "userId": "user123"  // Optional
}
```

### 3. Track User Interaction
```
POST /api/interactions
```

**Request Body**:
```json
{
  "userId": "user123",
  "restaurantId": 1,
  "rating": 4.5,  // Optional: 0-5
  "clicked": true,  // Optional
  "viewed": true  // Optional
}
```

## Configuration

### Environment Variables

```bash
# OpenAI API Key (for AI data fetching)
export OPENAI_API_KEY="your-api-key-here"

# ML API URL (for Next.js frontend)
export ML_API_URL="http://localhost:8000"
```

### Data Files

- `data/restaurants.json` - Base restaurant data
- `data/user_interactions.json` - User interaction history (auto-created)
- `data/ai_fetched_restaurants.json` - AI-fetched restaurant data (auto-created)

## Algorithm Details

### Scoring Weights

1. **Content-Based (40%)**: Mood, occasion, cuisine, dietary preferences
2. **Collaborative (30%)**: Similar users' preferences
3. **Search Matching (20%)**: Query text similarity
4. **AI-Fetched (10%)**: New restaurants from AI

### Dynamic Weight Adjustment

If a source has no data:
- Collaborative weight redistributed to content-based
- Search weight redistributed to content-based
- AI weight redistributed to content-based

### Search Query Processing

1. **Semantic Matching**: TF-IDF cosine similarity
2. **Keyword Extraction**: Important words from query
3. **Preference Extraction**: Mood, occasion, cuisine from query
4. **AI Fetching**: If no good matches, fetch new restaurants

## Example Use Cases

### 1. New User (No History)
- Uses content-based filtering only
- Can use search query matching
- AI fetching enabled for new restaurants

### 2. Returning User (With History)
- Uses collaborative filtering
- Combines with content-based
- Learns from user interactions

### 3. Search Query
- Matches query to restaurants
- Extracts preferences from query
- Fetches new restaurants if needed

### 4. Manual Details Entry
- Uses all entered details (mood, occasion, etc.)
- Combines with search query if provided
- Uses collaborative filtering if userId provided

## Performance Considerations

- **Caching**: User similarity matrix rebuilt on new interactions
- **Lazy Loading**: AI fetching only when needed
- **Batch Processing**: Multiple restaurants fetched in one API call
- **Storage**: JSON files for simplicity (can be upgraded to database)

## Future Enhancements

1. **Item-Based Collaborative Filtering**: Restaurant-to-restaurant similarity
2. **Deep Learning**: Neural network for recommendation
3. **Real-time Updates**: WebSocket for live recommendations
4. **Database Integration**: PostgreSQL/MongoDB for production
5. **A/B Testing**: Compare recommendation strategies

