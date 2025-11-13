export type Recommendation = {
  restaurantName: string;
  foodSuggestion: string;
  description: string;
  photoReference?: string;
};

export type ActionState = {
  recommendations: Recommendation[] | null;
  error: string | null;
};
