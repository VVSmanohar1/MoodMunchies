"""
Search Query Matching Module
Matches text search queries to restaurants using semantic similarity
"""

from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class SearchQueryMatcher:
    """
    Matches search queries to restaurants using TF-IDF and keyword matching
    """
    
    def __init__(self, restaurants: List[Dict]):
        """
        Initialize search matcher with restaurant data
        
        Args:
            restaurants: List of restaurant dictionaries
        """
        self.restaurants = restaurants
        self.vectorizer = TfidfVectorizer(max_features=200, stop_words='english', ngram_range=(1, 2))
        self._build_search_index()
    
    def _build_search_index(self):
        """Build searchable text index for all restaurants"""
        search_texts = []
        for restaurant in self.restaurants:
            # Combine all searchable text
            search_text = ' '.join([
                restaurant.get('restaurantName', ''),
                restaurant.get('cuisine', ''),
                restaurant.get('location', ''),
                restaurant.get('address', ''),
                restaurant.get('ambiance', ''),
                ' '.join(restaurant.get('popularDishes', [])),
                ' '.join(restaurant.get('dietaryOptions', [])),
                restaurant.get('priceRange', ''),
            ])
            search_texts.append(search_text.lower())
        
        if search_texts:
            self.restaurant_vectors = self.vectorizer.fit_transform(search_texts)
        else:
            self.restaurant_vectors = None
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from search query"""
        # Remove special characters and split
        query_clean = re.sub(r'[^\w\s]', ' ', query.lower())
        keywords = [word for word in query_clean.split() if len(word) > 2]
        return keywords
    
    def _keyword_match_score(self, restaurant: Dict, keywords: List[str]) -> float:
        """Calculate keyword matching score"""
        if not keywords:
            return 0.0
        
        searchable_text = ' '.join([
            restaurant.get('restaurantName', '').lower(),
            restaurant.get('cuisine', '').lower(),
            restaurant.get('location', '').lower(),
            restaurant.get('ambiance', '').lower(),
            ' '.join([d.lower() for d in restaurant.get('popularDishes', [])]),
        ])
        
        matches = sum(1 for keyword in keywords if keyword in searchable_text)
        return matches / len(keywords) if keywords else 0.0
    
    def search(
        self,
        query: str,
        top_k: int = 9,
        min_score: float = 0.1
    ) -> List[Dict]:
        """
        Search restaurants by query
        
        Args:
            query: Search query text
            top_k: Number of results to return
            min_score: Minimum similarity score threshold
        
        Returns:
            List of matched restaurants with scores
        """
        if not query or not self.restaurant_vectors:
            return []
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query.lower()])
        
        # Calculate similarity scores
        similarities = cosine_similarity(query_vector, self.restaurant_vectors)[0]
        
        # Combine semantic similarity with keyword matching
        scored_restaurants = []
        for idx, restaurant in enumerate(self.restaurants):
            semantic_score = float(similarities[idx])
            keyword_score = self._keyword_match_score(restaurant, keywords)
            
            # Weighted combination: 70% semantic, 30% keyword
            combined_score = semantic_score * 0.7 + keyword_score * 0.3
            
            if combined_score >= min_score:
                scored_restaurants.append({
                    'restaurant': restaurant,
                    'search_score': combined_score,
                    'semantic_score': semantic_score,
                    'keyword_score': keyword_score
                })
        
        # Sort by combined score
        scored_restaurants.sort(key=lambda x: x['search_score'], reverse=True)
        
        return scored_restaurants[:top_k]
    
    def match_query_to_preferences(
        self,
        query: str,
        mood: Optional[str] = None,
        occasion: Optional[str] = None,
        cuisine: Optional[str] = None
    ) -> Dict:
        """
        Extract preferences from search query using keyword matching
        
        Args:
            query: Search query
            mood: Optional mood hint
            occasion: Optional occasion hint
            cuisine: Optional cuisine hint
        
        Returns:
            Dictionary with extracted preferences
        """
        query_lower = query.lower()
        preferences = {
            'mood': mood,
            'occasion': occasion,
            'cuisine': cuisine,
            'dietary': None,
            'price_range': None,
            'keywords': []
        }
        
        # Extract mood from query
        mood_keywords = {
            'happy': ['happy', 'cheerful', 'joyful', 'excited'],
            'sad': ['sad', 'down', 'depressed', 'blue'],
            'stressed': ['stressed', 'tired', 'exhausted', 'busy'],
            'adventurous': ['adventurous', 'exciting', 'new', 'try'],
            'relaxed': ['relaxed', 'calm', 'peaceful', 'chill'],
            'celebratory': ['celebrate', 'celebration', 'special', 'party']
        }
        
        for mood_val, keywords in mood_keywords.items():
            if any(kw in query_lower for kw in keywords):
                preferences['mood'] = mood_val
                break
        
        # Extract occasion
        occasion_keywords = {
            'casual meal': ['casual', 'quick', 'simple'],
            'celebration': ['celebration', 'birthday', 'anniversary', 'special'],
            'quick bite': ['quick', 'fast', 'grab'],
            'date night': ['date', 'romantic', 'dinner date'],
            'family dinner': ['family', 'kids', 'children']
        }
        
        for occ_val, keywords in occasion_keywords.items():
            if any(kw in query_lower for kw in keywords):
                preferences['occasion'] = occ_val
                break
        
        # Extract cuisine
        cuisine_keywords = {
            'italian': ['italian', 'pasta', 'pizza'],
            'mexican': ['mexican', 'taco', 'burrito'],
            'indian': ['indian', 'curry', 'tikka'],
            'japanese': ['japanese', 'sushi', 'ramen'],
            'chinese': ['chinese', 'dim sum'],
            'american': ['american', 'burger', 'bbq']
        }
        
        for cui_val, keywords in cuisine_keywords.items():
            if any(kw in query_lower for kw in keywords):
                preferences['cuisine'] = cui_val
                break
        
        # Extract dietary preferences
        if any(word in query_lower for word in ['vegetarian', 'veggie']):
            preferences['dietary'] = 'vegetarian'
        elif any(word in query_lower for word in ['vegan']):
            preferences['dietary'] = 'vegan'
        elif any(word in query_lower for word in ['gluten-free', 'gluten free']):
            preferences['dietary'] = 'gluten-free'
        
        # Extract price range
        if any(word in query_lower for word in ['cheap', 'affordable', 'budget']):
            preferences['price_range'] = 'affordable'
        elif any(word in query_lower for word in ['expensive', 'fancy', 'upscale', 'fine dining']):
            preferences['price_range'] = 'expensive'
        
        # Extract keywords
        preferences['keywords'] = self._extract_keywords(query)
        
        return preferences

