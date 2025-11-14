# API Keys Setup Guide

## Overview

The enhanced recommendation system supports both **Gemini** and **OpenAI** APIs for fetching restaurant data. If API keys are available, the system will use AI to fetch and enrich restaurant data. If not available, it will use the local dataset.

## Setting Up API Keys

### Option 1: Environment Variables (Recommended)

#### For OpenAI:
```bash
# Linux/Mac
export OPENAI_API_KEY="your-openai-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-openai-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=your-openai-api-key-here
```

#### For Gemini:
```bash
# Linux/Mac
export GEMINI_API_KEY="your-gemini-api-key-here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Windows (CMD)
set GEMINI_API_KEY=your-gemini-api-key-here
```

### Option 2: .env File

Create a `.env` file in the `python_ml` directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
```

Then load it in your Python code:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

## How It Works

### Priority Order:
1. **Gemini API** - Used first if available
2. **OpenAI API** - Used if Gemini is not available
3. **Local Dataset** - Used if no API keys are available

### Data Flow:
1. User makes a query/recommendation request
2. System checks for API keys
3. If API keys available:
   - Searches in existing AI-fetched data first
   - If no good matches, fetches new data from AI
   - Stores fetched data (with deduplication)
   - Uses fetched data for recommendations
4. If no API keys:
   - Uses local dataset only
   - No new data fetching

## Deduplication

The system automatically prevents duplicate restaurants by:
- Checking restaurant name (normalized, case-insensitive)
- Checking address (if available)
- Fuzzy matching for similar names
- Only storing unique restaurants

## Data Storage

- **Base restaurants**: `data/restaurants.json`
- **AI-fetched restaurants**: `data/ai_fetched_restaurants.json`
- **User interactions**: `data/user_interactions.json`

All AI-fetched data is stored locally and reused for future queries.

## Testing API Keys

When you start the server, you'll see:
```
Enhanced recommendation engine initialized successfully
  - OpenAI API: Available
  - Gemini API: Available
```

Or if no keys:
```
Enhanced recommendation engine initialized successfully
  - AI APIs: Not available (will use local data only)
```

## Cost Considerations

- **OpenAI**: Uses `gpt-4o-mini` model (cost-effective)
- **Gemini**: Uses `gemini-2.0-flash-exp` model (free tier available)
- Data is cached locally, so API calls are only made when needed
- Deduplication prevents fetching the same restaurant multiple times

## Troubleshooting

### "No AI API keys found"
- Check that environment variables are set correctly
- Verify API keys are valid
- Restart the server after setting environment variables

### "Error fetching restaurant data from AI"
- Check API key validity
- Check internet connection
- Check API quota/limits
- Review error messages in console

### Duplicate restaurants appearing
- The deduplication algorithm checks name and address
- Very similar names might still pass through
- You can manually review `ai_fetched_restaurants.json`

