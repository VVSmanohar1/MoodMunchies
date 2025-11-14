"""
Enhanced Recommendation Engine
Combines content-based filtering, collaborative filtering, search matching, and AI data fetching
"""

import os
from typing import List, Dict, Optional
from .recommendation_engine import RestaurantRecommendationEngine
from .collaborative_filtering import CollaborativeFiltering
from .search_matcher import SearchQueryMatcher
from .ai_data_fetcher import AIDataFetcher


class EnhancedRecommendationEngine:
    """
    Enhanced recommendation engine that combines:
    1. Content-based filtering (mood, occasion, cuisine matching)
    2. Collaborative filtering (user-based recommendations)
    3. Search query matching (text-based search)
    4. AI data fetching (enrich restaurant database)
    """
    
    def __init__(
        self,
        restaurants_data_path: str,
        user_data_path: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ):
        """
        Initialize enhanced recommendation engine
        
        Args:
            restaurants_data_path: Path to restaurant data JSON
            user_data_path: Path to user interaction data JSON
            openai_api_key: OpenAI API key for data fetching
            gemini_api_key: Gemini API key for data fetching
        """
        # Initialize base content-based engine
        self.base_engine = RestaurantRecommendationEngine(restaurants_data_path)
        
        # Initialize collaborative filtering
        if user_data_path is None:
            user_data_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data',
                'user_interactions.json'
            )
        self.collab_filter = CollaborativeFiltering(user_data_path)
        
        # Initialize search matcher
        all_restaurants = self.base_engine.restaurants
        self.search_matcher = SearchQueryMatcher(all_restaurants)
        
        # Initialize AI data fetcher with both API keys
        ai_storage_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'ai_fetched_restaurants.json'
        )
        self.ai_fetcher = AIDataFetcher(
            openai_api_key=openai_api_key,
            gemini_api_key=gemini_api_key,
            data_storage_path=ai_storage_path,
            base_restaurants_path=restaurants_data_path
        )
        
        # Load AI-fetched restaurants and merge with base restaurants
        self._merge_ai_restaurants()
    
    def _merge_ai_restaurants(self):
        """Merge AI-fetched restaurants with base restaurants"""
        ai_restaurants = self.ai_fetcher.get_fetched_restaurants()
        if ai_restaurants:
            # Add AI restaurants to base engine
            self.base_engine.restaurants.extend(ai_restaurants)
            # Rebuild feature vectors with new restaurants
            self.base_engine._build_feature_vectors()
            # Update search matcher with new restaurants
            self.search_matcher = SearchQueryMatcher(self.base_engine.restaurants)
    
    def recommend(
        self,
        mood: str,
        occasion: str,
        cuisine: str,
        dietary_preference: str,
        time: str,
        location: Optional[str] = None,
        additional_notes: Optional[str] = None,
        user_id: Optional[str] = None,
        search_query: Optional[str] = None,
        use_ai_fetch: bool = True
    ) -> List[Dict]:
        """
        Generate recommendations using hybrid approach
        
        Args:
            mood: User's mood
            occasion: Occasion
            cuisine: Preferred cuisine
            dietary_preference: Dietary restrictions
            time: Time of day
            location: Location
            additional_notes: Additional notes
            user_id: User ID for collaborative filtering
            search_query: Optional search query for text matching
            use_ai_fetch: Whether to use AI to fetch new restaurants
        
        Returns:
            List of recommended restaurants with scores
        """
        # If search query provided, try to match it first
        search_results = []
        if search_query:
            search_results = self.search_matcher.search(search_query, top_k=9)
            # Extract preferences from search query
            query_prefs = self.search_matcher.match_query_to_preferences(
                search_query, mood, occasion, cuisine
            )
            # Override preferences if found in query
            if query_prefs.get('mood'):
                mood = query_prefs['mood']
            if query_prefs.get('occasion'):
                occasion = query_prefs['occasion']
            if query_prefs.get('cuisine'):
                cuisine = query_prefs['cuisine']
            if query_prefs.get('dietary'):
                dietary_preference = query_prefs['dietary']
        
        # Get content-based recommendations
        content_results = self.base_engine.recommend(
            mood=mood,
            occasion=occasion,
            cuisine=cuisine,
            dietary_preference=dietary_preference,
            time=time,
            location=location,
            additional_notes=additional_notes
        )
        
        # Get collaborative filtering recommendations if user_id provided
        collab_results = []
        if user_id:
            collab_results = self.collab_filter.get_collaborative_recommendations(
                user_id=user_id,
                restaurants=self.base_engine.restaurants,
                top_k=9
            )
        
        # Prepare user preferences for AI fetching
        user_preferences = {
            'mood': mood,
            'occasion': occasion,
            'cuisine': cuisine,
            'dietaryPreference': dietary_preference,
            'time': time,
            'location': location,
            'additionalNotes': additional_notes
        }
        
        # Try AI fetching if search query provided or if we need better matches
        ai_restaurants = []
        should_fetch_ai = False
        
        # Fetch from AI if:
        # 1. Search query provided and few matches
        # 2. Or if use_ai_fetch is True and we want to enrich results
        if use_ai_fetch:
            if search_query and len(search_results) < 3:
                should_fetch_ai = True
            elif search_query:  # Even with matches, try to get more relevant ones
                should_fetch_ai = True
        
        if should_fetch_ai:
            # First search in existing AI-fetched data
            ai_restaurants_data = self.ai_fetcher.search_fetched_restaurants(
                search_query or f"{cuisine} {occasion} {mood}",
                location,
                user_preferences=user_preferences,
                fetch_if_not_found=True
            )
            
            if ai_restaurants_data:
                # Score AI restaurants based on how well they match
                for ai_rest in ai_restaurants_data:
                    # Calculate match score
                    match_score = 0.5  # Base score
                    
                    # Check cuisine match
                    if ai_rest.get('cuisine', '').lower() == cuisine.lower() or cuisine.lower() == 'any':
                        match_score += 0.2
                    
                    # Check mood scores
                    mood_scores = ai_rest.get('moodScores', {})
                    if mood_scores.get(mood.lower(), 0) > 0.7:
                        match_score += 0.2
                    
                    # Check occasion scores
                    occasion_scores = ai_rest.get('occasionScores', {})
                    if occasion_scores.get(occasion.lower(), 0) > 0.7:
                        match_score += 0.1
                    
                    ai_restaurants.append({
                        'restaurant': ai_rest,
                        'score': min(1.0, match_score),
                        'source': 'ai'
                    })
                
                # Merge AI restaurants if new ones were fetched
                self._merge_ai_restaurants()
        
        # Combine and rank all results
        combined_results = self._combine_recommendations(
            content_results=content_results,
            collab_results=collab_results,
            search_results=search_results,
            ai_results=ai_restaurants,
            user_id=user_id
        )
        
        return combined_results[:9]
    
    def _combine_recommendations(
        self,
        content_results: List[Dict],
        collab_results: List[Dict],
        search_results: List[Dict],
        ai_results: List[Dict],
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Combine recommendations from different sources with weighted scoring
        
        Args:
            content_results: Content-based filtering results
            collab_results: Collaborative filtering results
            search_results: Search query matching results
            ai_results: AI-fetched restaurant results
            user_id: User ID
        
        Returns:
            Combined and ranked recommendations
        """
        # Create restaurant score dictionary
        restaurant_scores = {}
        restaurant_data = {}
        
        # Weight for different sources
        # If search results exist, prioritize them more
        has_search = len(search_results) > 0
        has_ai = len(ai_results) > 0
        
        if has_search or has_ai:
            # Prioritize search and AI results when query-based
            content_weight = 0.3
            collab_weight = 0.2
            search_weight = 0.3 if has_search else 0.0
            ai_weight = 0.2 if has_ai else 0.0
        else:
            # Default weights for content-based recommendations
            content_weight = 0.4
            collab_weight = 0.3
            search_weight = 0.2
            ai_weight = 0.1
        
        # Add content-based results
        for item in content_results:
            rest_id = item['restaurant']['id']
            restaurant_data[rest_id] = item['restaurant']
            if rest_id not in restaurant_scores:
                restaurant_scores[rest_id] = {
                    'content_score': 0.0,
                    'collab_score': 0.0,
                    'search_score': 0.0,
                    'ai_score': 0.0,
                    'final_score': 0.0
                }
            restaurant_scores[rest_id]['content_score'] = item['score']
        
        # Add collaborative filtering results
        for item in collab_results:
            rest_id = item['restaurant']['id']
            restaurant_data[rest_id] = item['restaurant']
            if rest_id not in restaurant_scores:
                restaurant_scores[rest_id] = {
                    'content_score': 0.0,
                    'collab_score': 0.0,
                    'search_score': 0.0,
                    'ai_score': 0.0,
                    'final_score': 0.0
                }
            restaurant_scores[rest_id]['collab_score'] = item['collaborative_score']
        
        # Add search results (prioritize these)
        for item in search_results:
            rest_id = item['restaurant']['id']
            restaurant_data[rest_id] = item['restaurant']
            if rest_id not in restaurant_scores:
                restaurant_scores[rest_id] = {
                    'content_score': 0.0,
                    'collab_score': 0.0,
                    'search_score': 0.0,
                    'ai_score': 0.0,
                    'final_score': 0.0
                }
            # Boost search score for query matches
            search_score = item.get('search_score', 0.0)
            # If search score is high, it's a good match
            restaurant_scores[rest_id]['search_score'] = min(1.0, search_score * 1.2)
        
        # Add AI results (prioritize these too)
        for item in ai_results:
            rest_id = item['restaurant']['id']
            restaurant_data[rest_id] = item['restaurant']
            if rest_id not in restaurant_scores:
                restaurant_scores[rest_id] = {
                    'content_score': 0.0,
                    'collab_score': 0.0,
                    'search_score': 0.0,
                    'ai_score': 0.0,
                    'final_score': 0.0
                }
            # AI-fetched restaurants are likely good matches
            ai_score = item.get('score', 0.5)
            restaurant_scores[rest_id]['ai_score'] = min(1.0, ai_score * 1.1)
        
        # Calculate final weighted scores
        for rest_id, scores in restaurant_scores.items():
            # Normalize scores to 0-1 range
            content_norm = min(1.0, scores['content_score'])
            collab_norm = min(1.0, scores['collab_score'] / 5.0) if scores['collab_score'] > 0 else 0.0
            search_norm = min(1.0, scores['search_score'])
            ai_norm = min(1.0, scores['ai_score'])
            
            # Adjust weights if certain sources are missing
            total_weight = content_weight + collab_weight + search_weight + ai_weight
            if collab_norm == 0:
                # Redistribute collaborative weight to content
                adjusted_content_weight = content_weight + collab_weight
                adjusted_collab_weight = 0.0
            else:
                adjusted_content_weight = content_weight
                adjusted_collab_weight = collab_weight
            
            if search_norm == 0:
                adjusted_search_weight = 0.0
                adjusted_content_weight += search_weight
            else:
                adjusted_search_weight = search_weight
            
            if ai_norm == 0:
                adjusted_ai_weight = 0.0
                adjusted_content_weight += ai_weight
            else:
                adjusted_ai_weight = ai_weight
            
            # Normalize weights
            weight_sum = adjusted_content_weight + adjusted_collab_weight + adjusted_search_weight + adjusted_ai_weight
            if weight_sum > 0:
                adjusted_content_weight /= weight_sum
                adjusted_collab_weight /= weight_sum
                adjusted_search_weight /= weight_sum
                adjusted_ai_weight /= weight_sum
            
            scores['final_score'] = (
                content_norm * adjusted_content_weight +
                collab_norm * adjusted_collab_weight +
                search_norm * adjusted_search_weight +
                ai_norm * adjusted_ai_weight
            )
        
        # Create final results list
        final_results = []
        for rest_id, scores in restaurant_scores.items():
            final_results.append({
                'restaurant': restaurant_data[rest_id],
                'score': scores['final_score'],
                'content_score': scores['content_score'],
                'collab_score': scores['collab_score'],
                'search_score': scores['search_score'],
                'ai_score': scores['ai_score']
            })
        
        # Sort by final score
        final_results.sort(key=lambda x: x['score'], reverse=True)
        
        return final_results
    
    def format_recommendations(
        self,
        scored_recommendations: List[Dict],
        mood: str = '',
        occasion: str = ''
    ) -> List[Dict]:
        """Format recommendations (delegate to base engine)"""
        return self.base_engine.format_recommendations(scored_recommendations, mood, occasion)
    
    def track_interaction(
        self,
        user_id: str,
        restaurant_id: int,
        rating: Optional[float] = None,
        clicked: bool = False,
        viewed: bool = False
    ):
        """Track user interaction for collaborative filtering"""
        self.collab_filter.add_interaction(
            user_id=user_id,
            restaurant_id=restaurant_id,
            rating=rating,
            clicked=clicked,
            viewed=viewed
        )

