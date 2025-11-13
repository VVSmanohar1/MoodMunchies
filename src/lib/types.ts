export type Recommendation = {
  restaurantName: string;
  foodSuggestion: string;
  description: string;
};

export type ActionState = {
  recommendations: Recommendation[] | null;
  error: string | null;
};
