# System Improvements - Query Matching & AI Integration

## Overview

The system has been enhanced to:
1. **Better match user queries** to restaurant recommendations
2. **Support both Gemini and OpenAI** API keys
3. **Fetch data from AI** when API keys are available
4. **Use local data** when API keys are not available
5. **Store fetched data without duplication**

## Key Improvements

### 1. Dual API Support (Gemini & OpenAI)

The system now supports both APIs with automatic fallback:
- **Priority**: Gemini → OpenAI → Local Data
- If Gemini API key is available, it's used first
- If not, OpenAI is used
- If neither is available, local dataset is used

### 2. Smart Deduplication

Restaurants are checked for duplicates before storage:
- **Name matching**: Normalized, case-insensitive comparison
- **Address matching**: If addresses match, it's a duplicate
- **Fuzzy matching**: Similar names are detected
- **Prevents storage** of duplicate restaurants

### 3. Enhanced Query Matching

The system now better matches user queries:

#### Search Query Priority
- When a search query is provided, it gets **higher weight (30%)**
- AI-fetched results get **higher weight (20%)** when available
- Content-based results adjusted accordingly

#### Query Enhancement
- User preferences (mood, occasion, cuisine) are included in AI queries
- This helps AI fetch more relevant restaurants
- Extracted preferences from search queries override manual inputs

### 4. Improved Scoring Algorithm

#### Dynamic Weight Adjustment
- **With search query**: Search (30%), AI (20%), Content (30%), Collab (20%)
- **Without search query**: Content (40%), Collab (30%), Search (20%), AI (10%)

#### Score Boosting
- Search results get **1.2x boost** for better ranking
- AI-fetched results get **1.1x boost** for relevance
- Matches are prioritized over general recommendations

### 5. Data Storage & Retrieval

#### Storage Locations
- **Base restaurants**: `data/restaurants.json` (original dataset)
- **AI-fetched**: `data/ai_fetched_restaurants.json` (newly fetched)
- **User interactions**: `data/user_interactions.json` (for collaborative filtering)

#### Retrieval Strategy
1. First searches in **existing AI-fetched data**
2. If no good matches, **fetches from AI** (if API keys available)
3. Stores new data **without duplication**
4. Merges with base restaurants for recommendations

## How It Works

### Request Flow

```
User Request (with query/preferences)
    ↓
Check API Keys Available?
    ↓
Yes → Search Existing AI Data → Found? → Use It
    ↓ No
    ↓
Fetch from AI (Gemini/OpenAI)
    ↓
Check Duplicates → Store New Data
    ↓
Merge with Base Restaurants
    ↓
Generate Recommendations (with improved matching)
```

### Matching Process

1. **Search Query Processing**:
   - Extracts preferences from query text
   - Matches to restaurants using TF-IDF
   - Scores based on semantic + keyword matching

2. **AI Data Fetching**:
   - Enhances query with user preferences
   - Fetches restaurants matching the query
   - Scores based on cuisine, mood, occasion match

3. **Combined Scoring**:
   - Combines all sources with dynamic weights
   - Prioritizes query matches
   - Returns top 9 recommendations

## Configuration

### Environment Variables

```bash
# Set one or both API keys
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
```

### API Behavior

- **With API keys**: Fetches new data, enriches recommendations
- **Without API keys**: Uses local data only, still provides good recommendations

## Example Scenarios

### Scenario 1: User searches "Italian restaurant for date night"

1. System extracts: cuisine=Italian, occasion=date night
2. Searches existing AI data
3. If not found, fetches from AI with enhanced query
4. Scores restaurants based on:
   - Italian cuisine match
   - Date night occasion score
   - Search query relevance
5. Returns top matches

### Scenario 2: User enters manual details (mood, occasion, etc.)

1. System uses entered preferences
2. If `useAiFetch=True`, also fetches relevant restaurants
3. Combines local + AI-fetched data
4. Scores based on all criteria
5. Returns best matches

### Scenario 3: No API keys available

1. System uses local dataset only
2. Still provides good recommendations
3. Uses content-based + collaborative filtering
4. No new data fetching

## Benefits

1. **Better Matching**: Query-based recommendations are more relevant
2. **Data Enrichment**: AI fetches new restaurants automatically
3. **No Duplicates**: Smart deduplication prevents data bloat
4. **Flexible**: Works with or without API keys
5. **Cost-Effective**: Caches data, minimizes API calls
6. **Scalable**: Local storage grows with usage

## Performance

- **First request**: May take longer if fetching from AI
- **Subsequent requests**: Fast (uses cached data)
- **Deduplication**: Minimal overhead
- **Storage**: JSON files (can be upgraded to database)

## Future Enhancements

1. **Database Integration**: Replace JSON with PostgreSQL/MongoDB
2. **Caching Layer**: Redis for faster lookups
3. **Batch Processing**: Fetch multiple queries at once
4. **Location-Based**: Use actual location data for better matching
5. **Real-time Updates**: WebSocket for live recommendations

