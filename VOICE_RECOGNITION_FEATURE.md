# Voice-Based Mood Recognition Feature

## Overview

This feature adds voice-based mood recognition to the MoodMunchies application, allowing users to speak their preferences instead of manually filling out forms. The system uses browser-native Web Speech API for speech-to-text conversion and AI-powered extraction to parse mood, occasion, cuisine, and other preferences from voice transcripts.

## Architecture

### Frontend Components

1. **`src/hooks/use-voice-recognition.ts`**
   - Custom React hook that wraps the Web Speech API
   - Handles speech recognition lifecycle (start, stop, error handling)
   - Provides real-time transcript updates
   - Browser compatibility checks

2. **`src/components/voice-input.tsx`**
   - Voice input UI component
   - Records audio and displays transcript
   - Calls backend API to extract preferences from transcript
   - Shows extracted preferences with visual feedback
   - Fallback mood extraction using keyword matching

3. **`src/app/components/recommendation-wizard.tsx`** (Updated)
   - Integrated voice input component
   - Form fields are now controlled components
   - Auto-populates form fields from extracted voice preferences
   - Toggle button to show/hide voice input

4. **`src/types/speech-recognition.d.ts`**
   - TypeScript type definitions for Web Speech API
   - Ensures type safety for speech recognition features

### Backend Components

1. **`python_ml/ml_engine/voice_extractor.py`**
   - Voice preference extraction module
   - AI-powered extraction using OpenAI or Gemini
   - Keyword-based fallback extraction
   - Normalizes extracted preferences to match form schema

2. **`python_ml/api/main.py`** (Updated)
   - New endpoint: `POST /api/voice/extract-preferences`
   - Accepts voice transcript and returns extracted preferences
   - Integrates with existing AI infrastructure

## How It Works

### User Flow

1. User clicks "Use Voice" button in the recommendation wizard
2. Voice input component appears
3. User clicks "Start Recording" and grants microphone permission
4. User speaks their preferences (e.g., "I'm feeling happy and want Italian food for dinner in downtown")
5. Speech is transcribed in real-time using Web Speech API
6. When user stops recording, transcript is sent to backend
7. Backend extracts preferences using AI (or keyword matching as fallback)
8. Extracted preferences auto-populate the form fields
9. User reviews and submits the form to get recommendations

### Technical Flow

```
User Voice Input
    ↓
Web Speech API (Browser)
    ↓
Speech-to-Text Transcription
    ↓
POST /api/voice/extract-preferences
    ↓
VoicePreferenceExtractor
    ├─→ AI Extraction (OpenAI/Gemini) [Primary]
    └─→ Keyword Matching [Fallback]
    ↓
Extracted Preferences (JSON)
    ↓
Frontend Form Auto-Population
    ↓
User Review & Submit
    ↓
Recommendations Generated
```

## API Endpoint

### `POST /api/voice/extract-preferences`

**Request:**
```json
{
  "transcript": "I'm feeling happy and want Italian food for dinner in downtown",
  "useAi": true
}
```

**Response:**
```json
{
  "mood": "happy",
  "occasion": null,
  "cuisine": "italian",
  "dietaryPreference": "non-vegetarian",
  "time": "dinner",
  "location": "downtown",
  "additionalNotes": "I'm feeling happy and want Italian food for dinner in downtown"
}
```

## Browser Compatibility

The Web Speech API is supported in:
- ✅ Chrome/Edge (Chromium-based)
- ✅ Safari (with `webkitSpeechRecognition`)
- ❌ Firefox (not supported)

The feature gracefully handles unsupported browsers by showing an error message.

## Configuration

### Environment Variables

**Frontend:**
- `NEXT_PUBLIC_ML_API_URL` - Backend API URL (defaults to `http://localhost:8000`)

**Backend:**
- `OPENAI_API_KEY` - For AI-powered extraction (optional)
- `GEMINI_API_KEY` - Alternative AI provider (optional)

If AI keys are not provided, the system falls back to keyword-based extraction.

## Usage Example

```typescript
// In a React component
import { VoiceInput } from '@/components/voice-input';

function MyComponent() {
  const handlePreferences = (prefs) => {
    console.log('Extracted preferences:', prefs);
    // Auto-populate form fields
  };

  return (
    <VoiceInput
      onPreferencesExtracted={handlePreferences}
      autoExtract={true}
    />
  );
}
```

## Features

### ✅ Implemented

- [x] Browser-native speech recognition
- [x] Real-time transcription
- [x] AI-powered preference extraction
- [x] Keyword-based fallback extraction
- [x] Form auto-population
- [x] Error handling and user feedback
- [x] Browser compatibility checks
- [x] Visual feedback for recording state
- [x] Extracted preferences display

### 🔄 Future Enhancements

- [ ] Multi-language support
- [ ] Voice command shortcuts
- [ ] Offline speech recognition
- [ ] Voice feedback/confirmation
- [ ] Continuous listening mode
- [ ] Voice history/recording playback

## Testing

### Manual Testing Steps

1. Start the backend server:
   ```bash
   cd python_ml
   python -m uvicorn api.main:app --reload
   ```

2. Start the frontend:
   ```bash
   npm run dev
   ```

3. Navigate to the recommendation wizard
4. Click "Use Voice" button
5. Grant microphone permission when prompted
6. Click "Start Recording"
7. Speak: "I'm feeling happy and want Italian food for dinner in downtown"
8. Click "Stop"
9. Verify that form fields are auto-populated
10. Submit the form and verify recommendations are generated

### Test Cases

- ✅ Voice recognition in Chrome
- ✅ Voice recognition in Safari
- ✅ Fallback message in unsupported browsers
- ✅ AI extraction with OpenAI
- ✅ AI extraction with Gemini
- ✅ Keyword fallback when AI unavailable
- ✅ Form auto-population
- ✅ Error handling for API failures
- ✅ Microphone permission denied handling

## Troubleshooting

### Issue: "Speech recognition is not supported"

**Solution:** Use Chrome, Edge, or Safari. Firefox does not support Web Speech API.

### Issue: "Microphone permission denied"

**Solution:** 
1. Check browser settings for microphone permissions
2. Ensure the site has permission to access microphone
3. Try refreshing the page and granting permission again

### Issue: "Failed to extract preferences"

**Solution:**
1. Check backend server is running
2. Verify API endpoint is accessible
3. Check browser console for errors
4. System will fallback to keyword matching if AI unavailable

### Issue: No preferences extracted

**Solution:**
- Ensure you speak clearly and include relevant keywords
- Try phrases like: "I'm feeling [mood]" or "I want [cuisine] food"
- Check that backend API is responding correctly

## Security Considerations

- Microphone access requires explicit user permission
- Voice transcripts are sent to backend for processing
- No voice recordings are stored permanently
- API keys should be kept secure and not exposed in frontend code

## Performance

- Speech recognition runs entirely in the browser (no external services)
- AI extraction adds ~1-2 seconds latency (depends on API response time)
- Keyword fallback is instant (<100ms)
- Real-time transcription has minimal performance impact

## Dependencies

### Frontend
- React 18+
- Next.js 15+
- Web Speech API (browser-native)

### Backend
- FastAPI
- OpenAI API (optional)
- Google Gemini API (optional)
- Python 3.8+

## License

Same as the main MoodMunchies project.

