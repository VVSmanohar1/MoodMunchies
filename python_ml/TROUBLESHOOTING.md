# Troubleshooting: API Keys Not Detected

## Quick Fix Steps

### Step 1: Check API Keys with Diagnostic Script

Run the diagnostic script to see what's wrong:

```bash
cd python_ml
python check_api_keys.py
```

This will show you:
- If API keys are found
- If packages are installed
- If clients can be initialized
- What errors are occurring

### Step 2: Set Up API Keys Properly

#### Option A: Using .env File (Recommended)

1. Create a `.env` file in the `python_ml` directory:
   ```bash
   cd python_ml
   touch .env
   ```

2. Add your API keys to the `.env` file:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

3. Make sure `python-dotenv` is installed:
   ```bash
   pip install python-dotenv
   ```

4. Restart the server

#### Option B: Using Environment Variables

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export GEMINI_API_KEY="your-gemini-api-key-here"
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:GEMINI_API_KEY="your-gemini-api-key-here"
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=your-openai-api-key-here
set GEMINI_API_KEY=your-gemini-api-key-here
```

**Important**: You must set these in the SAME terminal where you run the server!

### Step 3: Verify Installation

Make sure all required packages are installed:

```bash
cd python_ml
pip install -r requirements.txt
```

This installs:
- `openai` (for OpenAI API)
- `google-generativeai` (for Gemini API)
- `python-dotenv` (for .env file support)

### Step 4: Check Server Output

When you start the server, you should see:

```
=== API Keys Status ===
  - OpenAI API Key: Found (length: 51, starts with: sk-proj...)
  - Gemini API Key: Found (length: 39, starts with: AIzaSy...)
======================

OpenAI client initialized successfully
Gemini client initialized successfully
Enhanced recommendation engine initialized successfully
  - OpenAI API: Available and initialized
  - Gemini API: Available and initialized
```

If you see errors, they will tell you what's wrong.

## Common Issues

### Issue 1: "No API keys found in environment variables"

**Cause**: API keys not set or .env file not loaded

**Solution**:
1. Check if `.env` file exists in `python_ml` directory
2. Check if `.env` file has correct format (no quotes around values)
3. Check if `python-dotenv` is installed
4. Try setting environment variables directly in terminal

### Issue 2: "Key found but client not initialized"

**Cause**: Invalid API key or package not installed

**Solution**:
1. Verify API key is correct (no extra spaces, complete key)
2. Check if `openai` package is installed: `pip install openai`
3. Check if `google-generativeai` package is installed: `pip install google-generativeai`
4. Test API key manually (see below)

### Issue 3: "Failed to initialize OpenAI/Gemini client"

**Cause**: API key is invalid or expired

**Solution**:
1. Get a new API key from the provider
2. Make sure key is not expired
3. Check API key format:
   - OpenAI: Should start with `sk-`
   - Gemini: Should start with `AIzaSy`

### Issue 4: Environment variables not persisting

**Cause**: Variables set in different terminal session

**Solution**:
1. Set variables in the SAME terminal where you run the server
2. Or use `.env` file instead (persists across sessions)

## Testing API Keys Manually

### Test OpenAI Key:
```python
from openai import OpenAI
client = OpenAI(api_key="your-key-here")
# If no error, key is valid
```

### Test Gemini Key:
```python
import google.generativeai as genai
genai.configure(api_key="your-key-here")
model = genai.GenerativeModel('gemini-2.0-flash-exp')
# If no error, key is valid
```

## Check Health Endpoint

After starting the server, check the health endpoint:

```bash
curl http://localhost:8000/health
```

Response should show:
```json
{
  "status": "healthy",
  "engine_loaded": true,
  "api_status": {
    "openai_available": true,
    "gemini_available": true,
    "openai_key_set": true,
    "gemini_key_set": true
  }
}
```

## Still Not Working?

1. **Run the diagnostic script**: `python check_api_keys.py`
2. **Check server logs**: Look for error messages when starting
3. **Verify .env file location**: Should be in `python_ml/` directory
4. **Check file permissions**: Make sure .env file is readable
5. **Try setting variables directly**: Use export/setenv in terminal

## Getting Help

If still having issues, provide:
1. Output from `python check_api_keys.py`
2. Server startup logs
3. Your operating system
4. How you set the API keys (.env file or environment variables)

