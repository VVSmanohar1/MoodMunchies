export type Recommendation = {
  restaurantName: string;
  foodSuggestion: string;
  reasonForRecommendation: string;
  location: string;
  address: string;
  contactDetails?: string;
  photoReference?: string; // This is now for AI-suggested image hints
};

export type ActionState = {
  recommendations: Recommendation[] | null;
  error: string | null;
};
