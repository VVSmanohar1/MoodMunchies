'use client';

import {useState, useRef, useCallback, useEffect} from 'react';

export interface VoiceRecognitionState {
  isListening: boolean;
  transcript: string;
  error: string | null;
  isSupported: boolean;
}

export interface VoiceRecognitionOptions {
  continuous?: boolean;
  interimResults?: boolean;
  lang?: string;
  onResult?: (transcript: string, isFinal: boolean) => void;
  onError?: (error: string) => void;
}

/**
 * Custom hook for Web Speech API voice recognition
 * Provides speech-to-text functionality with browser-native API
 */
export function useVoiceRecognition(options: VoiceRecognitionOptions = {}) {
  const {
    continuous = true,
    interimResults = true,
    lang = 'en-US',
    onResult,
    onError,
  } = options;

  const [state, setState] = useState<VoiceRecognitionState>({
    isListening: false,
    transcript: '',
    error: null,
    isSupported: typeof window !== 'undefined' && 'webkitSpeechRecognition' in window,
  });

  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Initialize recognition
  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Check for browser support
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setState(prev => ({
        ...prev,
        isSupported: false,
        error: 'Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.',
      }));
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = continuous;
    recognition.interimResults = interimResults;
    recognition.lang = lang;

    recognition.onstart = () => {
      setState(prev => ({
        ...prev,
        isListening: true,
        error: null,
      }));
    };

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      const fullTranscript = finalTranscript || interimTranscript;
      setState(prev => ({
        ...prev,
        transcript: fullTranscript.trim(),
      }));

      if (onResult) {
        onResult(fullTranscript.trim(), finalTranscript.length > 0);
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      let errorMessage = 'An error occurred with speech recognition.';
      
      switch (event.error) {
        case 'no-speech':
          errorMessage = 'No speech detected. Please try again.';
          break;
        case 'audio-capture':
          errorMessage = 'No microphone found. Please check your microphone settings.';
          break;
        case 'not-allowed':
          errorMessage = 'Microphone permission denied. Please allow microphone access.';
          break;
        case 'network':
          errorMessage = 'Network error. Please check your connection.';
          break;
        case 'aborted':
          errorMessage = 'Speech recognition was aborted.';
          break;
        default:
          errorMessage = `Speech recognition error: ${event.error}`;
      }

      setState(prev => ({
        ...prev,
        isListening: false,
        error: errorMessage,
      }));

      if (onError) {
        onError(errorMessage);
      }
    };

    recognition.onend = () => {
      setState(prev => ({
        ...prev,
        isListening: false,
      }));
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [continuous, interimResults, lang, onResult, onError]);

  const startListening = useCallback(() => {
    if (!recognitionRef.current) {
      setState(prev => ({
        ...prev,
        error: 'Speech recognition is not initialized.',
      }));
      return;
    }

    try {
      setState(prev => ({
        ...prev,
        transcript: '',
        error: null,
      }));
      recognitionRef.current.start();
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        error: error.message || 'Failed to start speech recognition.',
      }));
    }
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current && state.isListening) {
      recognitionRef.current.stop();
    }
  }, [state.isListening]);

  const reset = useCallback(() => {
    stopListening();
    setState(prev => ({
      ...prev,
      transcript: '',
      error: null,
    }));
  }, [stopListening]);

  return {
    ...state,
    startListening,
    stopListening,
    reset,
  };
}

