export type Recommendation = {
  restaurantName: string;
  foodSuggestion: string;
  reasonForRecommendation: string;
  location: string;
  address: string;
  contactDetails?: string;
  photoReference?: string;
};

export type ActionState = {
  recommendations: Recommendation[] | null;
  error: string | null;
  isFallback: boolean;
};
