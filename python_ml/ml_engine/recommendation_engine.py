"""
ML-based Restaurant Recommendation Engine
Uses content-based filtering and mood-based feature engineering
"""

import json
import os
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class RestaurantRecommendationEngine:
    """
    ML-based recommendation engine that uses:
    1. Content-based filtering based on mood, occasion, cuisine, dietary preferences
    2. Feature engineering for mood mapping
    3. TF-IDF vectorization for text-based features
    4. Cosine similarity for recommendation scoring
    """
    
    def __init__(self, restaurants_data_path: str):
        """Initialize the recommendation engine with restaurant data"""
        self.restaurants_data_path = restaurants_data_path
        self.restaurants = self._load_restaurants()
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self._build_feature_vectors()
    
    def _load_restaurants(self) -> List[Dict]:
        """Load restaurant data from JSON file"""
        with open(self.restaurants_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('restaurants', [])
    
    def _build_feature_vectors(self):
        """Build feature vectors for all restaurants"""
        # Create text features for each restaurant
        restaurant_texts = []
        for restaurant in self.restaurants:
            # Combine all text features
            text_features = [
                restaurant.get('cuisine', ''),
                restaurant.get('ambiance', ''),
                ' '.join(restaurant.get('popularDishes', [])),
                ' '.join(restaurant.get('dietaryOptions', [])),
                restaurant.get('priceRange', ''),
            ]
            restaurant_texts.append(' '.join(text_features))
        
        # Fit TF-IDF vectorizer
        if restaurant_texts:
            self.restaurant_vectors = self.vectorizer.fit_transform(restaurant_texts)
        else:
            self.restaurant_vectors = None
    
    def _calculate_mood_score(self, restaurant: Dict, mood: str) -> float:
        """Calculate mood compatibility score for a restaurant"""
        mood_scores = restaurant.get('moodScores', {})
        return mood_scores.get(mood.lower(), 0.5)
    
    def _calculate_occasion_score(self, restaurant: Dict, occasion: str) -> float:
        """Calculate occasion compatibility score"""
        occasion_scores = restaurant.get('occasionScores', {})
        return occasion_scores.get(occasion.lower(), 0.5)
    
    def _calculate_time_score(self, restaurant: Dict, time: str) -> float:
        """Calculate time compatibility score"""
        time_scores = restaurant.get('timeScores', {})
        return time_scores.get(time.lower(), 0.5)
    
    def _check_dietary_compatibility(self, restaurant: Dict, dietary_preference: str) -> bool:
        """Check if restaurant supports the dietary preference"""
        dietary_options = [opt.lower() for opt in restaurant.get('dietaryOptions', [])]
        dietary_preference_lower = dietary_preference.lower()
        
        # Handle special cases
        if dietary_preference_lower == 'non-vegetarian':
            return 'non-vegetarian' in dietary_options or 'vegetarian' not in dietary_options
        return dietary_preference_lower in dietary_options
    
    def _check_cuisine_match(self, restaurant: Dict, preferred_cuisine: str) -> float:
        """Check cuisine compatibility (returns 1.0 for exact match, 0.5 for 'any', 0.0 otherwise)"""
        if preferred_cuisine.lower() == 'any':
            return 1.0
        return 1.0 if restaurant.get('cuisine', '').lower() == preferred_cuisine.lower() else 0.3
    
    def _process_additional_notes(self, notes: Optional[str]) -> Dict[str, float]:
        """Process additional notes to extract preferences using keyword matching"""
        if not notes:
            return {}
        
        notes_lower = notes.lower()
        preferences = {
            'spicy': 0.0,
            'quiet': 0.0,
            'romantic': 0.0,
            'family_friendly': 0.0,
            'healthy': 0.0,
            'fast': 0.0,
            'affordable': 0.0,
            'upscale': 0.0,
        }
        
        # Keyword matching for preferences
        if any(word in notes_lower for word in ['spicy', 'hot', 'heat', 'fiery']):
            preferences['spicy'] = 1.0
        if any(word in notes_lower for word in ['quiet', 'peaceful', 'calm', 'serene']):
            preferences['quiet'] = 1.0
        if any(word in notes_lower for word in ['romantic', 'date', 'intimate', 'cozy']):
            preferences['romantic'] = 1.0
        if any(word in notes_lower for word in ['family', 'kids', 'children']):
            preferences['family_friendly'] = 1.0
        if any(word in notes_lower for word in ['healthy', 'fresh', 'light', 'nutritious']):
            preferences['healthy'] = 1.0
        if any(word in notes_lower for word in ['fast', 'quick', 'quickly', 'hurry']):
            preferences['fast'] = 1.0
        if any(word in notes_lower for word in ['cheap', 'affordable', 'budget', 'inexpensive']):
            preferences['affordable'] = 1.0
        if any(word in notes_lower for word in ['fancy', 'upscale', 'elegant', 'fine dining']):
            preferences['upscale'] = 1.0
        
        return preferences
    
    def _calculate_notes_score(self, restaurant: Dict, notes_preferences: Dict[str, float]) -> float:
        """Calculate score based on additional notes preferences"""
        if not notes_preferences:
            return 1.0
        
        score = 0.0
        total_weight = 0.0
        
        ambiance = restaurant.get('ambiance', '').lower()
        price_range = restaurant.get('priceRange', '').lower()
        
        # Match preferences with restaurant features
        if notes_preferences.get('spicy', 0) > 0:
            # Check if restaurant serves spicy food (cuisine-based heuristic)
            cuisine = restaurant.get('cuisine', '').lower()
            if cuisine in ['indian', 'mexican', 'thai', 'chinese']:
                score += 0.3
            total_weight += 0.3
        
        if notes_preferences.get('quiet', 0) > 0:
            if any(word in ambiance for word in ['quiet', 'peaceful', 'serene', 'calm']):
                score += 0.2
            total_weight += 0.2
        
        if notes_preferences.get('romantic', 0) > 0:
            if any(word in ambiance for word in ['romantic', 'intimate', 'cozy', 'elegant']):
                score += 0.2
            total_weight += 0.2
        
        if notes_preferences.get('family_friendly', 0) > 0:
            if any(word in ambiance for word in ['family', 'casual', 'friendly']):
                score += 0.2
            total_weight += 0.2
        
        if notes_preferences.get('healthy', 0) > 0:
            if any(word in ambiance for word in ['healthy', 'fresh', 'light']):
                score += 0.2
            total_weight += 0.2
        
        if notes_preferences.get('affordable', 0) > 0:
            if price_range == 'affordable':
                score += 0.2
            total_weight += 0.2
        
        if notes_preferences.get('upscale', 0) > 0:
            if price_range in ['expensive', 'moderate']:
                score += 0.2
            total_weight += 0.2
        
        # Normalize score
        return score / total_weight if total_weight > 0 else 1.0
    
    def _calculate_content_similarity(self, user_preferences: Dict, restaurant: Dict) -> float:
        """Calculate content-based similarity using TF-IDF"""
        if self.restaurant_vectors is None:
            return 0.5
        
        # Create user preference text
        user_text = ' '.join([
            user_preferences.get('cuisine', ''),
            user_preferences.get('dietaryPreference', ''),
            user_preferences.get('mood', ''),
            user_preferences.get('occasion', ''),
        ])
        
        # Transform user preferences
        user_vector = self.vectorizer.transform([user_text])
        
        # Find restaurant index
        restaurant_idx = next(
            (i for i, r in enumerate(self.restaurants) if r['id'] == restaurant['id']),
            None
        )
        
        if restaurant_idx is None:
            return 0.5
        
        # Calculate cosine similarity
        similarity = cosine_similarity(user_vector, self.restaurant_vectors[restaurant_idx:restaurant_idx+1])[0][0]
        return max(0.0, similarity)  # Ensure non-negative
    
    def recommend(
        self,
        mood: str,
        occasion: str,
        cuisine: str,
        dietary_preference: str,
        time: str,
        location: Optional[str] = None,
        additional_notes: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate restaurant recommendations using ML-based scoring
        
        Args:
            mood: User's current mood
            occasion: Occasion for the meal
            cuisine: Preferred cuisine
            dietary_preference: Dietary restrictions
            time: Time of day
            location: User's location (optional, for future location-based filtering)
            additional_notes: Additional preferences (optional)
        
        Returns:
            List of recommended restaurants with scores
        """
        user_preferences = {
            'mood': mood,
            'occasion': occasion,
            'cuisine': cuisine,
            'dietaryPreference': dietary_preference,
            'time': time,
        }
        
        notes_preferences = self._process_additional_notes(additional_notes)
        
        scored_restaurants = []
        
        for restaurant in self.restaurants:
            # Filter by dietary preference
            if not self._check_dietary_compatibility(restaurant, dietary_preference):
                continue
            
            # Calculate weighted scores
            mood_score = self._calculate_mood_score(restaurant, mood)
            occasion_score = self._calculate_occasion_score(restaurant, occasion)
            time_score = self._calculate_time_score(restaurant, time)
            cuisine_score = self._check_cuisine_match(restaurant, cuisine)
            notes_score = self._calculate_notes_score(restaurant, notes_preferences)
            content_similarity = self._calculate_content_similarity(user_preferences, restaurant)
            
            # Weighted combination of scores
            # Mood and occasion are most important (30% each)
            # Time, cuisine, and content similarity (10% each)
            # Notes score (10%)
            final_score = (
                mood_score * 0.30 +
                occasion_score * 0.30 +
                time_score * 0.10 +
                cuisine_score * 0.10 +
                content_similarity * 0.10 +
                notes_score * 0.10
            )
            
            scored_restaurants.append({
                'restaurant': restaurant,
                'score': final_score
            })
        
        # Sort by score (descending)
        scored_restaurants.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top 9 recommendations
        return scored_restaurants[:9]
    
    def format_recommendations(
        self, 
        scored_recommendations: List[Dict],
        mood: str = '',
        occasion: str = ''
    ) -> List[Dict]:
        """
        Format recommendations to match the expected output structure
        
        Args:
            scored_recommendations: List of scored restaurant recommendations
            mood: User's mood (for generating reasons)
            occasion: User's occasion (for generating reasons)
        
        Returns:
            List of formatted recommendation dictionaries
        """
        formatted = []
        
        for item in scored_recommendations:
            restaurant = item['restaurant']
            score = item['score']
            
            # Select a food suggestion from popular dishes
            popular_dishes = restaurant.get('popularDishes', [])
            food_suggestion = popular_dishes[0] if popular_dishes else "Chef's Special"
            
            # Generate reason for recommendation based on scores
            reasons = []
            if score > 0.8:
                reasons.append("This is an excellent match for your preferences")
            elif score > 0.6:
                reasons.append("This is a great match for your preferences")
            else:
                reasons.append("This matches your preferences")
            
            # Add specific reasons based on high scores
            if mood and restaurant.get('moodScores', {}).get(mood.lower(), 0) > 0.7:
                reasons.append(f"perfect for your {mood.lower()} mood")
            
            if occasion and restaurant.get('occasionScores', {}).get(occasion.lower(), 0) > 0.7:
                reasons.append(f"ideal for {occasion.lower()}")
            
            reason_text = ". ".join(reasons) + "."
            
            formatted.append({
                'restaurantName': restaurant.get('restaurantName', 'Unknown Restaurant'),
                'foodSuggestion': food_suggestion,
                'reasonForRecommendation': reason_text,
                'location': restaurant.get('location', ''),
                'address': restaurant.get('address', ''),
                'contactDetails': restaurant.get('contactDetails', ''),
            })
        
        return formatted

