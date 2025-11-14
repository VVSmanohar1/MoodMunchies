"""
Collaborative Filtering Module
Implements user-based collaborative filtering for restaurant recommendations
"""

import json
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFiltering:
    """
    User-based collaborative filtering for restaurant recommendations.
    Uses user interaction history to find similar users and recommend restaurants.
    """
    
    def __init__(self, user_data_path: str):
        """
        Initialize collaborative filtering with user interaction data
        
        Args:
            user_data_path: Path to JSON file storing user interactions
        """
        self.user_data_path = user_data_path
        self.user_interactions = self._load_user_data()
        self.user_similarity_matrix = None
        self._build_similarity_matrix()
    
    def _load_user_data(self) -> Dict:
        """Load user interaction data from JSON file"""
        if os.path.exists(self.user_data_path):
            try:
                with open(self.user_data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'users': {}, 'interactions': []}
        return {'users': {}, 'interactions': []}
    
    def _save_user_data(self):
        """Save user interaction data to JSON file"""
        os.makedirs(os.path.dirname(self.user_data_path), exist_ok=True)
        with open(self.user_data_path, 'w', encoding='utf-8') as f:
            json.dump(self.user_interactions, f, indent=2)
    
    def _build_similarity_matrix(self):
        """Build user similarity matrix based on interaction history"""
        if not self.user_interactions.get('interactions'):
            self.user_similarity_matrix = {}
            return
        
        # Build user-restaurant interaction matrix
        user_restaurant_matrix = defaultdict(lambda: defaultdict(float))
        user_ids = set()
        restaurant_ids = set()
        
        for interaction in self.user_interactions['interactions']:
            user_id = interaction.get('userId')
            restaurant_id = interaction.get('restaurantId')
            rating = interaction.get('rating', 0)  # 0-5 scale
            clicked = interaction.get('clicked', False)
            viewed = interaction.get('viewed', False)
            
            if user_id and restaurant_id:
                # Calculate interaction score (rating weighted more than clicks/views)
                score = rating * 2.0  # Rating is most important
                if clicked:
                    score += 1.0
                if viewed:
                    score += 0.5
                
                user_restaurant_matrix[user_id][restaurant_id] = score
                user_ids.add(user_id)
                restaurant_ids.add(restaurant_id)
        
        if not user_ids:
            self.user_similarity_matrix = {}
            return
        
        # Create matrix for similarity calculation
        user_ids_list = sorted(list(user_ids))
        restaurant_ids_list = sorted(list(restaurant_ids))
        
        # Build user vectors
        user_vectors = []
        for user_id in user_ids_list:
            vector = [user_restaurant_matrix[user_id].get(rest_id, 0.0) 
                     for rest_id in restaurant_ids_list]
            user_vectors.append(vector)
        
        if len(user_vectors) > 1:
            # Calculate cosine similarity between users
            similarity_matrix = cosine_similarity(user_vectors)
            
            # Store similarity matrix as dictionary
            self.user_similarity_matrix = {}
            for i, user_id_i in enumerate(user_ids_list):
                self.user_similarity_matrix[user_id_i] = {}
                for j, user_id_j in enumerate(user_ids_list):
                    if i != j:
                        self.user_similarity_matrix[user_id_i][user_id_j] = similarity_matrix[i][j]
        else:
            self.user_similarity_matrix = {}
    
    def add_interaction(
        self,
        user_id: str,
        restaurant_id: int,
        rating: Optional[float] = None,
        clicked: bool = False,
        viewed: bool = False
    ):
        """
        Add a user interaction (rating, click, view)
        
        Args:
            user_id: Unique user identifier
            restaurant_id: Restaurant ID
            rating: Rating (0-5)
            clicked: Whether user clicked on the restaurant
            viewed: Whether user viewed the restaurant
        """
        interaction = {
            'userId': user_id,
            'restaurantId': restaurant_id,
            'timestamp': datetime.now().isoformat(),
        }
        
        if rating is not None:
            interaction['rating'] = max(0.0, min(5.0, rating))
        if clicked:
            interaction['clicked'] = True
        if viewed:
            interaction['viewed'] = True
        
        if 'interactions' not in self.user_interactions:
            self.user_interactions['interactions'] = []
        
        self.user_interactions['interactions'].append(interaction)
        self._save_user_data()
        self._build_similarity_matrix()
    
    def get_similar_users(self, user_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Get users similar to the given user
        
        Args:
            user_id: User ID
            top_k: Number of similar users to return
        
        Returns:
            List of (user_id, similarity_score) tuples
        """
        if not self.user_similarity_matrix or user_id not in self.user_similarity_matrix:
            return []
        
        similar_users = list(self.user_similarity_matrix[user_id].items())
        similar_users.sort(key=lambda x: x[1], reverse=True)
        return similar_users[:top_k]
    
    def get_collaborative_recommendations(
        self,
        user_id: str,
        restaurants: List[Dict],
        top_k: int = 9
    ) -> List[Dict]:
        """
        Get restaurant recommendations using collaborative filtering
        
        Args:
            user_id: User ID
            restaurants: List of all available restaurants
            top_k: Number of recommendations to return
        
        Returns:
            List of recommended restaurants with collaborative scores
        """
        if not self.user_similarity_matrix or user_id not in self.user_similarity_matrix:
            return []
        
        # Get similar users
        similar_users = self.get_similar_users(user_id, top_k=10)
        
        if not similar_users:
            return []
        
        # Get restaurants that similar users liked
        restaurant_scores = defaultdict(float)
        user_restaurant_interactions = defaultdict(set)
        
        # Build user-restaurant interaction map
        for interaction in self.user_interactions.get('interactions', []):
            uid = interaction.get('userId')
            rid = interaction.get('restaurantId')
            rating = interaction.get('rating', 0)
            if uid and rid:
                user_restaurant_interactions[uid].add(rid)
                if rating > 0:
                    restaurant_scores[rid] += rating
        
        # Calculate weighted scores based on similar users
        collaborative_scores = {}
        for similar_user_id, similarity in similar_users:
            similar_user_restaurants = user_restaurant_interactions.get(similar_user_id, set())
            for restaurant_id in similar_user_restaurants:
                # Weight by similarity
                if restaurant_id not in collaborative_scores:
                    collaborative_scores[restaurant_id] = 0.0
                collaborative_scores[restaurant_id] += similarity
        
        # Get user's already interacted restaurants
        user_restaurants = user_restaurant_interactions.get(user_id, set())
        
        # Filter and score restaurants
        scored_restaurants = []
        restaurant_dict = {r['id']: r for r in restaurants}
        
        for restaurant_id, score in collaborative_scores.items():
            if restaurant_id in restaurant_dict and restaurant_id not in user_restaurants:
                scored_restaurants.append({
                    'restaurant': restaurant_dict[restaurant_id],
                    'collaborative_score': score
                })
        
        # Sort by score and return top k
        scored_restaurants.sort(key=lambda x: x['collaborative_score'], reverse=True)
        return scored_restaurants[:top_k]

