"""
Voice Transcript Preference Extractor
Uses AI to extract mood, occasion, cuisine, and other preferences from voice transcripts
"""

from typing import Dict, Optional
import json
import re


class VoicePreferenceExtractor:
    """
    Extracts preferences from voice transcripts using AI and keyword matching
    """
    
    def __init__(self, ai_fetcher=None):
        """
        Initialize voice preference extractor
        
        Args:
            ai_fetcher: Optional AIDataFetcher instance for AI-powered extraction
        """
        self.ai_fetcher = ai_fetcher
    
    def extract_preferences(
        self,
        transcript: str,
        use_ai: bool = True
    ) -> Dict[str, Optional[str]]:
        """
        Extract preferences from voice transcript
        
        Args:
            transcript: Voice transcript text
            use_ai: Whether to use AI for extraction (falls back to keyword matching)
        
        Returns:
            Dictionary with extracted preferences
        """
        if not transcript or not transcript.strip():
            return self._empty_preferences()
        
        # Try AI extraction first if available
        if use_ai and self.ai_fetcher:
            ai_result = self._extract_with_ai(transcript)
            if ai_result:
                return ai_result
        
        # Fallback to keyword matching
        return self._extract_with_keywords(transcript)
    
    def _extract_with_ai(self, transcript: str) -> Optional[Dict[str, Optional[str]]]:
        """
        Extract preferences using AI (OpenAI or Gemini)
        
        Args:
            transcript: Voice transcript text
        
        Returns:
            Dictionary with extracted preferences or None if AI unavailable
        """
        if not self.ai_fetcher:
            return None
        
        # Check if AI clients are actually available
        has_openai = hasattr(self.ai_fetcher, 'openai_client') and self.ai_fetcher.openai_client is not None
        has_gemini = hasattr(self.ai_fetcher, 'gemini_model') and self.ai_fetcher.gemini_model is not None
        
        if not has_openai and not has_gemini:
            return None
        
        prompt = f"""Extract the following information from this voice transcript about food preferences:

Transcript: "{transcript}"

Extract and return ONLY a JSON object with these exact keys (use null if not found):
{{
    "mood": "happy|sad|stressed|adventurous|relaxed|celebratory" or null,
    "occasion": "casual meal|celebration|quick bite|date night|family dinner" or null,
    "cuisine": "any|italian|mexican|indian|japanese|chinese|american" or null,
    "dietaryPreference": "vegetarian|non-vegetarian|vegan|gluten-free" or null,
    "time": "breakfast|brunch|lunch|dinner|snack" or null,
    "location": city or area name or null,
    "additionalNotes": any additional context or null
}}

Return ONLY the JSON object, no other text."""

        try:
            # Try OpenAI first
            if self.ai_fetcher.openai_client:
                response = self.ai_fetcher.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts structured data from voice transcripts. Always return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=200
                )
                result_text = response.choices[0].message.content.strip()
                # Remove markdown code blocks if present
                result_text = re.sub(r'```json\s*', '', result_text)
                result_text = re.sub(r'```\s*', '', result_text)
                result = json.loads(result_text)
                return self._normalize_preferences(result)
            
            # Try Gemini if OpenAI not available
            elif self.ai_fetcher.gemini_model:
                response = self.ai_fetcher.gemini_model.generate_content(prompt)
                result_text = response.text.strip()
                # Remove markdown code blocks if present
                result_text = re.sub(r'```json\s*', '', result_text)
                result_text = re.sub(r'```\s*', '', result_text)
                result = json.loads(result_text)
                return self._normalize_preferences(result)
        
        except Exception as e:
            print(f"AI extraction failed: {e}, falling back to keyword matching")
            return None
        
        return None
    
    def _extract_with_keywords(self, transcript: str) -> Dict[str, Optional[str]]:
        """
        Extract preferences using keyword matching (fallback method)
        
        Args:
            transcript: Voice transcript text
        
        Returns:
            Dictionary with extracted preferences
        """
        transcript_lower = transcript.lower()
        preferences = self._empty_preferences()
        
        # Extract mood
        mood_keywords = {
            'happy': ['happy', 'cheerful', 'joyful', 'excited', 'great', 'wonderful', 'amazing', 'good'],
            'sad': ['sad', 'down', 'depressed', 'unhappy', 'blue', 'feeling low'],
            'stressed': ['stressed', 'tired', 'exhausted', 'busy', 'overwhelmed', 'anxious'],
            'adventurous': ['adventurous', 'exciting', 'new', 'try', 'explore', 'different'],
            'relaxed': ['relaxed', 'calm', 'peaceful', 'chill', 'easy', 'laid back'],
            'celebratory': ['celebrate', 'celebration', 'special', 'party', 'anniversary', 'birthday']
        }
        
        for mood, keywords in mood_keywords.items():
            if any(kw in transcript_lower for kw in keywords):
                preferences['mood'] = mood
                break
        
        # Extract occasion
        occasion_keywords = {
            'casual meal': ['casual', 'quick', 'simple', 'regular'],
            'celebration': ['celebration', 'birthday', 'anniversary', 'special occasion'],
            'quick bite': ['quick', 'fast', 'grab', 'snack'],
            'date night': ['date', 'romantic', 'dinner date', 'with my partner'],
            'family dinner': ['family', 'kids', 'children', 'with family']
        }
        
        for occ, keywords in occasion_keywords.items():
            if any(kw in transcript_lower for kw in keywords):
                preferences['occasion'] = occ
                break
        
        # Extract cuisine
        cuisine_keywords = {
            'italian': ['italian', 'pasta', 'pizza', 'spaghetti'],
            'mexican': ['mexican', 'taco', 'burrito', 'quesadilla'],
            'indian': ['indian', 'curry', 'tikka', 'naan', 'biryani'],
            'japanese': ['japanese', 'sushi', 'ramen', 'tempura'],
            'chinese': ['chinese', 'dim sum', 'fried rice', 'lo mein'],
            'american': ['american', 'burger', 'bbq', 'steak', 'grill']
        }
        
        for cui, keywords in cuisine_keywords.items():
            if any(kw in transcript_lower for kw in keywords):
                preferences['cuisine'] = cui
                break
        
        # Extract dietary preference
        if any(word in transcript_lower for word in ['vegetarian', 'veggie', 'no meat']):
            preferences['dietaryPreference'] = 'vegetarian'
        elif any(word in transcript_lower for word in ['vegan', 'no dairy', 'no animal']):
            preferences['dietaryPreference'] = 'vegan'
        elif any(word in transcript_lower for word in ['gluten-free', 'gluten free', 'no gluten']):
            preferences['dietaryPreference'] = 'gluten-free'
        else:
            preferences['dietaryPreference'] = 'non-vegetarian'  # Default
        
        # Extract time
        time_keywords = {
            'breakfast': ['breakfast', 'morning', 'early'],
            'brunch': ['brunch', 'late morning'],
            'lunch': ['lunch', 'noon', 'midday'],
            'dinner': ['dinner', 'evening', 'night', 'tonight'],
            'snack': ['snack', 'bite', 'quick']
        }
        
        for time, keywords in time_keywords.items():
            if any(kw in transcript_lower for kw in keywords):
                preferences['time'] = time
                break
        
        # Extract location (look for common location patterns)
        location_patterns = [
            r'\b(in|at|near|around)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+\s+(?:Street|Avenue|Road|Boulevard|Park|Square))',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                location = match.group(2) if match.group(2) else match.group(1)
                if location and len(location) > 2:
                    preferences['location'] = location
                    break
        
        # Additional notes - use transcript if it contains useful info
        if len(transcript) > 20:
            # Only include if it's not just extracted keywords
            preferences['additionalNotes'] = transcript
        
        return preferences
    
    def _normalize_preferences(self, prefs: Dict) -> Dict[str, Optional[str]]:
        """
        Normalize extracted preferences to match expected format
        
        Args:
            prefs: Raw preferences dictionary
        
        Returns:
            Normalized preferences dictionary
        """
        normalized = self._empty_preferences()
        
        # Normalize mood
        mood = prefs.get('mood', '').lower() if prefs.get('mood') else None
        valid_moods = ['happy', 'sad', 'stressed', 'adventurous', 'relaxed', 'celebratory']
        if mood and mood in valid_moods:
            normalized['mood'] = mood
        
        # Normalize occasion
        occasion = prefs.get('occasion', '').lower() if prefs.get('occasion') else None
        valid_occasions = ['casual meal', 'celebration', 'quick bite', 'date night', 'family dinner']
        if occasion:
            # Try to match to valid occasion
            for valid_occ in valid_occasions:
                if valid_occ in occasion or occasion in valid_occ:
                    normalized['occasion'] = valid_occ
                    break
        
        # Normalize cuisine
        cuisine = prefs.get('cuisine', '').lower() if prefs.get('cuisine') else None
        valid_cuisines = ['any', 'italian', 'mexican', 'indian', 'japanese', 'chinese', 'american']
        if cuisine and cuisine in valid_cuisines:
            normalized['cuisine'] = cuisine
        
        # Normalize dietary preference
        dietary = prefs.get('dietaryPreference', '').lower() if prefs.get('dietaryPreference') else None
        valid_dietary = ['vegetarian', 'non-vegetarian', 'vegan', 'gluten-free']
        if dietary and dietary in valid_dietary:
            normalized['dietaryPreference'] = dietary
        
        # Normalize time
        time = prefs.get('time', '').lower() if prefs.get('time') else None
        valid_times = ['breakfast', 'brunch', 'lunch', 'dinner', 'snack']
        if time and time in valid_times:
            normalized['time'] = time
        
        # Location and notes (pass through as-is)
        if prefs.get('location'):
            normalized['location'] = prefs['location']
        if prefs.get('additionalNotes'):
            normalized['additionalNotes'] = prefs['additionalNotes']
        
        return normalized
    
    def _empty_preferences(self) -> Dict[str, Optional[str]]:
        """Return empty preferences dictionary"""
        return {
            'mood': None,
            'occasion': None,
            'cuisine': None,
            'dietaryPreference': None,
            'time': None,
            'location': None,
            'additionalNotes': None
        }

