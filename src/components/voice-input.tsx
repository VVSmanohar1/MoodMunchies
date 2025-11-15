'use client';

import {useState, useEffect, useCallback} from 'react';
import {useVoiceRecognition} from '@/hooks/use-voice-recognition';
import {Button} from '@/components/ui/button';
import {Mic, MicOff, Loader2, CheckCircle2, XCircle} from 'lucide-react';
import {Alert, AlertDescription} from '@/components/ui/alert';
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from '@/components/ui/card';

export interface ExtractedPreferences {
  mood?: string;
  occasion?: string;
  cuisine?: string;
  dietaryPreference?: string;
  time?: string;
  location?: string;
  additionalNotes?: string;
  emotion?: string;
  emotionConfidence?: number;
}

export interface VoiceInputProps {
  onPreferencesExtracted?: (preferences: ExtractedPreferences) => void;
  onTranscript?: (transcript: string) => void;
  autoExtract?: boolean;
}

/**
 * Voice Input Component
 * Records voice, transcribes it, and extracts mood/preferences using AI
 */
export function VoiceInput({
  onPreferencesExtracted,
  onTranscript,
  autoExtract = true,
}: VoiceInputProps) {
  const [extractedPreferences, setExtractedPreferences] = useState<ExtractedPreferences | null>(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionError, setExtractionError] = useState<string | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [isRecording, setIsRecording] = useState(false);

  const {
    isListening,
    transcript,
    error: recognitionError,
    isSupported,
    startListening,
    stopListening,
    reset,
  } = useVoiceRecognition({
    continuous: true,
    interimResults: true,
    onResult: (text, isFinal) => {
      if (onTranscript) {
        onTranscript(text);
      }
      
      // Auto-extract preferences when user stops speaking
      if (isFinal && autoExtract && text.trim().length > 0) {
        extractPreferences(text);
      }
    },
    onError: (error) => {
      setExtractionError(error);
    },
  });

  /**
   * Extract mood and preferences from voice transcript using AI
   */
  const extractPreferences = async (text: string) => {
    if (!text.trim()) return;

    setIsExtracting(true);
    setExtractionError(null);

    try {
      // Use environment variable or default to localhost
      const apiUrl = process.env.NEXT_PUBLIC_ML_API_URL || 
                     (typeof window !== 'undefined' ? window.location.origin.replace(/:\d+$/, ':8000') : 'http://localhost:8000');
      const response = await fetch(`${apiUrl}/api/voice/extract-preferences`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({transcript: text}),
      });

      if (!response.ok) {
        throw new Error(`Failed to extract preferences: ${response.statusText}`);
      }

      const data = await response.json();
      const preferences: ExtractedPreferences = {
        mood: data.mood,
        occasion: data.occasion,
        cuisine: data.cuisine,
        dietaryPreference: data.dietaryPreference,
        time: data.time,
        location: data.location,
        additionalNotes: data.additionalNotes,
      };

      setExtractedPreferences(preferences);
      
      if (onPreferencesExtracted) {
        onPreferencesExtracted(preferences);
      }
    } catch (error: any) {
      console.error('Error extracting preferences:', error);
      setExtractionError(error.message || 'Failed to extract preferences. Please try again.');
      
      // Fallback: Try to extract basic mood from transcript
      const fallbackMood = extractMoodFallback(text);
      if (fallbackMood) {
        const fallbackPrefs: ExtractedPreferences = {
          mood: fallbackMood,
          additionalNotes: text,
        };
        setExtractedPreferences(fallbackPrefs);
        if (onPreferencesExtracted) {
          onPreferencesExtracted(fallbackPrefs);
        }
      }
    } finally {
      setIsExtracting(false);
    }
  };

  /**
   * Simple fallback mood extraction using keyword matching
   */
  const extractMoodFallback = (text: string): string | null => {
    const lowerText = text.toLowerCase();
    const moodKeywords: Record<string, string[]> = {
      happy: ['happy', 'joyful', 'excited', 'great', 'wonderful', 'amazing'],
      sad: ['sad', 'down', 'depressed', 'unhappy', 'blue'],
      stressed: ['stressed', 'anxious', 'worried', 'tired', 'exhausted'],
      adventurous: ['adventurous', 'explore', 'try something new', 'different'],
      relaxed: ['relaxed', 'calm', 'chill', 'peaceful', 'easy'],
      celebratory: ['celebrate', 'celebration', 'party', 'special', 'anniversary'],
    };

    for (const [mood, keywords] of Object.entries(moodKeywords)) {
      if (keywords.some(keyword => lowerText.includes(keyword))) {
        return mood;
      }
    }

    return null;
  };

  /**
   * Detect emotion from audio blob using voice emotion detection API
   */
  const detectEmotionFromAudio = useCallback(async (audioBlob: Blob) => {
    try {
      setIsExtracting(true);
      
      // Convert blob to base64
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      
      reader.onloadend = async () => {
        const base64Audio = (reader.result as string).split(',')[1]; // Remove data:audio/wav;base64, prefix
        
        const apiUrl = process.env.NEXT_PUBLIC_ML_API_URL || 
                       (typeof window !== 'undefined' ? window.location.origin.replace(/:\d+$/, ':8000') : 'http://localhost:8000');
        
        const response = await fetch(`${apiUrl}/api/voice/detect-emotion`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            audio: base64Audio,
            format: 'webm'  // MediaRecorder typically records in webm format
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to detect emotion: ${response.statusText}`);
        }

        const emotionData = await response.json();
        
        // Update preferences with detected emotion/mood
        const updatedPreferences: ExtractedPreferences = {
          ...extractedPreferences,
          emotion: emotionData.emotion,
          mood: emotionData.mood || extractedPreferences?.mood,
          emotionConfidence: emotionData.confidence,
        };
        
        setExtractedPreferences(updatedPreferences);
        
        if (onPreferencesExtracted) {
          onPreferencesExtracted(updatedPreferences);
        }
      };
    } catch (error: any) {
      console.error('Error detecting emotion from audio:', error);
      setExtractionError(error.message || 'Failed to detect emotion. Using transcript only.');
    } finally {
      setIsExtracting(false);
    }
  }, [extractedPreferences, onPreferencesExtracted]);

  // Initialize MediaRecorder for audio capture
  useEffect(() => {
    if (typeof window !== 'undefined' && navigator.mediaDevices) {
      let stream: MediaStream | null = null;
      let chunks: Blob[] = [];
      
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((audioStream) => {
          stream = audioStream;
          const recorder = new MediaRecorder(audioStream);

          recorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              chunks.push(event.data);
              setAudioChunks([...chunks]);
            }
          };

          recorder.onstop = async () => {
            const audioBlob = new Blob(chunks, { type: 'audio/webm' });
            chunks = []; // Reset chunks
            setAudioChunks([]);
            
            // Detect emotion from audio
            if (audioBlob.size > 0) {
              await detectEmotionFromAudio(audioBlob);
            }
            
            // Stop all tracks
            if (stream) {
              stream.getTracks().forEach(track => track.stop());
            }
          };

          setMediaRecorder(recorder);
        })
        .catch((error) => {
          console.error('Error accessing microphone:', error);
        });
      
      // Cleanup function
      return () => {
        if (stream) {
          stream.getTracks().forEach(track => track.stop());
        }
      };
    }
  }, [detectEmotionFromAudio]);

  const handleToggleListening = async () => {
    if (isListening) {
      stopListening();
      
      // Stop audio recording if active
      if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        setIsRecording(false);
      }
      
      // Extract preferences when stopping
      if (transcript.trim() && autoExtract) {
        await extractPreferences(transcript);
      }
    } else {
      reset();
      startListening();
      
      // Start audio recording for emotion detection
      if (mediaRecorder && (mediaRecorder.state === 'inactive' || mediaRecorder.state === 'paused')) {
        setAudioChunks([]);
        try {
          mediaRecorder.start(100); // Collect data every 100ms
          setIsRecording(true);
        } catch (error) {
          console.error('Error starting recorder:', error);
        }
      }
    }
  };

  if (!isSupported) {
    return (
      <Alert variant="destructive">
        <XCircle className="h-4 w-4" />
        <AlertDescription>
          Voice recognition is not supported in this browser. Please use Chrome, Edge, or Safari.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mic className="h-5 w-5" />
          Voice Input
        </CardTitle>
        <CardDescription>
          Speak your mood and preferences, and we'll extract them automatically
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <Button
            type="button"
            onClick={handleToggleListening}
            variant={isListening ? 'destructive' : 'default'}
            size="lg"
            className="flex items-center gap-2"
          >
            {isListening ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Listening...
              </>
            ) : (
              <>
                <Mic className="h-4 w-4" />
                Start Recording
              </>
            )}
          </Button>
          
          {isListening && (
            <Button
              type="button"
              onClick={stopListening}
              variant="outline"
              size="sm"
            >
              <MicOff className="h-4 w-4" />
              Stop
            </Button>
          )}
        </div>

        {transcript && (
          <div className="p-4 bg-muted rounded-lg">
            <p className="text-sm text-muted-foreground mb-2">Transcript:</p>
            <p className="text-sm">{transcript}</p>
          </div>
        )}

        {isExtracting && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            Extracting preferences...
          </div>
        )}

        {extractionError && (
          <Alert variant="destructive">
            <XCircle className="h-4 w-4" />
            <AlertDescription>{extractionError}</AlertDescription>
          </Alert>
        )}

        {recognitionError && (
          <Alert variant="destructive">
            <XCircle className="h-4 w-4" />
            <AlertDescription>{recognitionError}</AlertDescription>
          </Alert>
        )}

        {extractedPreferences && !isExtracting && (
          <Alert className="border-green-500/50 bg-green-500/10">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-900 dark:text-green-200">
              <div className="space-y-1 mt-2">
                {extractedPreferences.emotion && (
                  <p>
                    <strong>Detected Emotion:</strong> {extractedPreferences.emotion} 
                    {extractedPreferences.emotionConfidence && (
                      <span className="text-xs ml-2">({Math.round(extractedPreferences.emotionConfidence * 100)}% confidence)</span>
                    )}
                  </p>
                )}
                {extractedPreferences.mood && (
                  <p><strong>Mood:</strong> {extractedPreferences.mood}</p>
                )}
                {extractedPreferences.occasion && (
                  <p><strong>Occasion:</strong> {extractedPreferences.occasion}</p>
                )}
                {extractedPreferences.cuisine && (
                  <p><strong>Cuisine:</strong> {extractedPreferences.cuisine}</p>
                )}
                {extractedPreferences.time && (
                  <p><strong>Time:</strong> {extractedPreferences.time}</p>
                )}
                {extractedPreferences.location && (
                  <p><strong>Location:</strong> {extractedPreferences.location}</p>
                )}
              </div>
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}

