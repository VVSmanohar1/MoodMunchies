"""
AI Data Fetcher Module
Supports both Gemini and OpenAI APIs for fetching restaurant information
Includes deduplication and smart data storage
"""

import json
import os
from typing import List, Dict, Optional
import re

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Try to import Google Generative AI (Gemini)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIDataFetcher:
    """
    Fetches restaurant data using AI (Gemini or OpenAI) and stores it with deduplication
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        data_storage_path: str = None,
        base_restaurants_path: str = None
    ):
        """
        Initialize AI data fetcher
        
        Args:
            openai_api_key: OpenAI API key (or from environment)
            gemini_api_key: Gemini API key (or from environment)
            data_storage_path: Path to store fetched restaurant data
            base_restaurants_path: Path to base restaurants for deduplication
        """
        # Get API keys from environment if not provided
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        # Initialize clients
        self.openai_client = None
        self.gemini_model = None
        
        if self.openai_api_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                print("OpenAI client initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
        
        if self.gemini_api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                print("Gemini client initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini client: {e}")
        
        if not self.openai_client and not self.gemini_model:
            print("Warning: No AI API keys found. AI data fetching disabled.")
        
        # Set up data storage paths
        if data_storage_path is None:
            data_storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data',
                'ai_fetched_restaurants.json'
            )
        self.data_storage_path = data_storage_path
        
        if base_restaurants_path is None:
            base_restaurants_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data',
                'restaurants.json'
            )
        self.base_restaurants_path = base_restaurants_path
        
        self.fetched_data = self._load_fetched_data()
        self.base_restaurants = self._load_base_restaurants()
    
    def _load_fetched_data(self) -> Dict:
        """Load previously fetched restaurant data"""
        if os.path.exists(self.data_storage_path):
            try:
                with open(self.data_storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'restaurants': [], 'metadata': {}}
        return {'restaurants': [], 'metadata': {}}
    
    def _load_base_restaurants(self) -> List[Dict]:
        """Load base restaurants for deduplication"""
        if os.path.exists(self.base_restaurants_path):
            try:
                with open(self.base_restaurants_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('restaurants', [])
            except:
                return []
        return []
    
    def _save_fetched_data(self):
        """Save fetched restaurant data to file"""
        os.makedirs(os.path.dirname(self.data_storage_path), exist_ok=True)
        with open(self.data_storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.fetched_data, f, indent=2)
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison (lowercase, remove special chars)"""
        if not text:
            return ""
        text = text.lower().strip()
        # Remove special characters and extra spaces
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _is_duplicate(self, new_restaurant: Dict, existing_restaurants: List[Dict]) -> bool:
        """
        Check if restaurant is duplicate based on name and address
        
        Args:
            new_restaurant: New restaurant to check
            existing_restaurants: List of existing restaurants
        
        Returns:
            True if duplicate found
        """
        new_name = self._normalize_text(new_restaurant.get('restaurantName', ''))
        new_address = self._normalize_text(new_restaurant.get('address', ''))
        
        if not new_name:
            return False
        
        for existing in existing_restaurants:
            existing_name = self._normalize_text(existing.get('restaurantName', ''))
            existing_address = self._normalize_text(existing.get('address', ''))
            
            # Check name match (exact or very similar)
            if new_name == existing_name:
                return True
            
            # Check if names are very similar (fuzzy match)
            if new_name and existing_name:
                # Simple similarity check: if one name contains the other
                if new_name in existing_name or existing_name in new_name:
                    # Also check address if available
                    if new_address and existing_address:
                        if new_address == existing_address:
                            return True
                    else:
                        # If addresses not available, consider it duplicate if names are very similar
                        if len(new_name) > 5 and len(existing_name) > 5:
                            return True
        
        return False
    
    def _fetch_with_openai(self, query: str, location: Optional[str], max_results: int) -> List[Dict]:
        """Fetch restaurant data using OpenAI"""
        if not self.openai_client:
            return []
        
        try:
            prompt = f"""Based on the following search query, provide restaurant recommendations with detailed information.

Search Query: {query}
Location: {location or "Not specified"}

For each restaurant (provide {max_results} restaurants), return the following information in JSON format:
{{
  "restaurantName": "Name of the restaurant",
  "cuisine": "Type of cuisine (e.g., italian, mexican, indian, japanese, chinese, american)",
  "location": "General area or neighborhood",
  "address": "Full street address",
  "contactDetails": "Phone number or website",
  "popularDishes": ["Dish 1", "Dish 2", "Dish 3"],
  "dietaryOptions": ["vegetarian", "non-vegetarian", "vegan", "gluten-free"],
  "priceRange": "affordable/moderate/expensive",
  "ambiance": "Description of ambiance (e.g., cozy, casual, romantic, elegant)",
  "moodScores": {{
    "happy": 0.0-1.0,
    "sad": 0.0-1.0,
    "stressed": 0.0-1.0,
    "adventurous": 0.0-1.0,
    "relaxed": 0.0-1.0,
    "celebratory": 0.0-1.0
  }},
  "occasionScores": {{
    "casual meal": 0.0-1.0,
    "celebration": 0.0-1.0,
    "quick bite": 0.0-1.0,
    "date night": 0.0-1.0,
    "family dinner": 0.0-1.0
  }},
  "timeScores": {{
    "breakfast": 0.0-1.0,
    "brunch": 0.0-1.0,
    "lunch": 0.0-1.0,
    "dinner": 0.0-1.0,
    "snack": 0.0-1.0
  }}
}}

Return only a valid JSON array of restaurant objects. Do not include any markdown formatting or code blocks."""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a restaurant data expert. Provide accurate restaurant information in JSON format. Match the query exactly."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            restaurants_data = json.loads(content)
            if not isinstance(restaurants_data, list):
                restaurants_data = [restaurants_data]
            
            return restaurants_data
        
        except Exception as e:
            print(f"Error fetching with OpenAI: {e}")
            return []
    
    def _fetch_with_gemini(self, query: str, location: Optional[str], max_results: int) -> List[Dict]:
        """Fetch restaurant data using Gemini"""
        if not self.gemini_model:
            return []
        
        try:
            prompt = f"""Based on the following search query, provide restaurant recommendations with detailed information.

Search Query: {query}
Location: {location or "Not specified"}

For each restaurant (provide {max_results} restaurants), return the following information in JSON format:
{{
  "restaurantName": "Name of the restaurant",
  "cuisine": "Type of cuisine (e.g., italian, mexican, indian, japanese, chinese, american)",
  "location": "General area or neighborhood",
  "address": "Full street address",
  "contactDetails": "Phone number or website",
  "popularDishes": ["Dish 1", "Dish 2", "Dish 3"],
  "dietaryOptions": ["vegetarian", "non-vegetarian", "vegan", "gluten-free"],
  "priceRange": "affordable/moderate/expensive",
  "ambiance": "Description of ambiance (e.g., cozy, casual, romantic, elegant)",
  "moodScores": {{
    "happy": 0.0-1.0,
    "sad": 0.0-1.0,
    "stressed": 0.0-1.0,
    "adventurous": 0.0-1.0,
    "relaxed": 0.0-1.0,
    "celebratory": 0.0-1.0
  }},
  "occasionScores": {{
    "casual meal": 0.0-1.0,
    "celebration": 0.0-1.0,
    "quick bite": 0.0-1.0,
    "date night": 0.0-1.0,
    "family dinner": 0.0-1.0
  }},
  "timeScores": {{
    "breakfast": 0.0-1.0,
    "brunch": 0.0-1.0,
    "lunch": 0.0-1.0,
    "dinner": 0.0-1.0,
    "snack": 0.0-1.0
  }}
}}

Return only a valid JSON array of restaurant objects. Do not include any markdown formatting or code blocks."""
            
            response = self.gemini_model.generate_content(prompt)
            content = response.text.strip()
            
            # Remove markdown code blocks
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            restaurants_data = json.loads(content)
            if not isinstance(restaurants_data, list):
                restaurants_data = [restaurants_data]
            
            return restaurants_data
        
        except Exception as e:
            print(f"Error fetching with Gemini: {e}")
            return []
    
    def fetch_restaurant_data(
        self,
        query: str,
        location: Optional[str] = None,
        max_results: int = 5,
        user_preferences: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Fetch restaurant data using available AI API (Gemini or OpenAI)
        
        Args:
            query: Search query (e.g., "Italian restaurants in downtown")
            location: Location hint
            max_results: Maximum number of restaurants to fetch
            user_preferences: Optional user preferences to include in query
        
        Returns:
            List of restaurant dictionaries with AI-generated data (without duplicates)
        """
        # Enhance query with user preferences if provided
        enhanced_query = query
        if user_preferences:
            pref_parts = []
            if user_preferences.get('mood'):
                pref_parts.append(f"mood: {user_preferences['mood']}")
            if user_preferences.get('occasion'):
                pref_parts.append(f"occasion: {user_preferences['occasion']}")
            if user_preferences.get('cuisine'):
                pref_parts.append(f"cuisine: {user_preferences['cuisine']}")
            if user_preferences.get('dietaryPreference'):
                pref_parts.append(f"dietary: {user_preferences['dietaryPreference']}")
            if pref_parts:
                enhanced_query = f"{query}. Preferences: {', '.join(pref_parts)}"
        
        # Try Gemini first, then OpenAI
        restaurants_data = []
        if self.gemini_model:
            print(f"Fetching data using Gemini for query: {query}")
            restaurants_data = self._fetch_with_gemini(enhanced_query, location, max_results)
        elif self.openai_client:
            print(f"Fetching data using OpenAI for query: {query}")
            restaurants_data = self._fetch_with_openai(enhanced_query, location, max_results)
        else:
            print("No AI API available. Returning empty list.")
            return []
        
        if not restaurants_data:
            return []
        
        # Get all existing restaurants (base + fetched)
        all_existing = self.base_restaurants + self.fetched_data.get('restaurants', [])
        
        # Filter out duplicates and assign IDs
        new_restaurants = []
        existing_ids = [r.get('id', 0) for r in all_existing]
        next_id = max(existing_ids) + 1 if existing_ids else 1000
        
        for restaurant in restaurants_data:
            # Check for duplicates
            if not self._is_duplicate(restaurant, all_existing):
                restaurant['id'] = next_id
                restaurant['source'] = 'ai_fetched'
                restaurant['query'] = query
                restaurant['location_hint'] = location
                if user_preferences:
                    restaurant['user_preferences'] = user_preferences
                next_id += 1
                new_restaurants.append(restaurant)
            else:
                print(f"Skipping duplicate restaurant: {restaurant.get('restaurantName', 'Unknown')}")
        
        # Store new restaurants
        if new_restaurants:
            if 'restaurants' not in self.fetched_data:
                self.fetched_data['restaurants'] = []
            
            self.fetched_data['restaurants'].extend(new_restaurants)
            self._save_fetched_data()
            print(f"Stored {len(new_restaurants)} new restaurants (skipped {len(restaurants_data) - len(new_restaurants)} duplicates)")
        
        return new_restaurants
    
    def get_fetched_restaurants(self) -> List[Dict]:
        """Get all previously fetched restaurants"""
        return self.fetched_data.get('restaurants', [])
    
    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants (base + fetched)"""
        return self.base_restaurants + self.get_fetched_restaurants()
    
    def search_fetched_restaurants(
        self,
        query: str,
        location: Optional[str] = None,
        user_preferences: Optional[Dict] = None,
        fetch_if_not_found: bool = True
    ) -> List[Dict]:
        """
        Search in previously fetched restaurants, or fetch new ones if not found
        
        Args:
            query: Search query
            location: Location hint
            user_preferences: User preferences for better matching
            fetch_if_not_found: Whether to fetch new data if no matches found
        
        Returns:
            List of matching restaurants
        """
        # First, search in existing fetched data
        fetched = self.get_fetched_restaurants()
        matching = []
        query_lower = query.lower()
        
        for restaurant in fetched:
            restaurant_text = ' '.join([
                restaurant.get('restaurantName', ''),
                restaurant.get('cuisine', ''),
                restaurant.get('location', ''),
                restaurant.get('ambiance', ''),
            ]).lower()
            
            # Check if query matches
            if query_lower in restaurant_text or any(
                word in restaurant_text for word in query_lower.split() if len(word) > 2
            ):
                matching.append(restaurant)
        
        # If no matches found and AI is available, fetch new data
        if not matching and fetch_if_not_found and (self.gemini_model or self.openai_client):
            print(f"No matches found in existing data. Fetching new restaurants for: {query}")
            new_restaurants = self.fetch_restaurant_data(
                query, location, max_results=5, user_preferences=user_preferences
            )
            matching.extend(new_restaurants)
        
        return matching
