'use server';

/**
 * @fileOverview Generates personalized food and restaurant recommendations based on user preferences.
 *
 * - generateFoodRecommendations - A function that generates food recommendations.
 * - GenerateFoodRecommendationsInput - The input type for the generateFoodRecommendations function.
 * - GenerateFoodRecommendationsOutput - The return type for the generateFoodRecommendations function.
 */

import {ai} from '@/ai/genkit';
import {searchNearbyPlaces} from '@/ai/tools/google-places';
import {z} from 'genkit';

const GenerateFoodRecommendationsInputSchema = z.object({
  mood: z.string().describe("The user's current mood."),
  occasion: z
    .string()
    .describe('The occasion for the meal (e.g., dinner, lunch, celebration).'),
  cuisine: z
    .string()
    .describe('The preferred cuisine (e.g., Italian, Mexican, Indian).'),
  dietaryPreference: z
    .string()
    .describe(
      'The dietary preference (e.g., vegetarian, non-vegetarian, vegan, gluten-free).'
    ),
  time: z.string().describe('The preferred time for the meal.'),
  location: z.string().describe("The user's current location."),
  additionalNotes: z
    .string()
    .optional()
    .describe('Any additional notes or preferences from the user.'),
});

export type GenerateFoodRecommendationsInput = z.infer<
  typeof GenerateFoodRecommendationsInputSchema
>;

const GenerateFoodRecommendationsOutputSchema = z.object({
  recommendations: z
    .array(
      z.object({
        restaurantName: z.string().describe('The name of the restaurant.'),
        foodSuggestion: z
          .string()
          .describe('A specific food suggestion from the restaurant.'),
        description: z
          .string()
          .describe('A description of the restaurant and food.'),
      })
    )
    .describe(
      'A list of 9 personalized food and restaurant recommendations.'
    ),
});

export type GenerateFoodRecommendationsOutput = z.infer<
  typeof GenerateFoodRecommendationsOutputSchema
>;

export async function generateFoodRecommendations(
  input: GenerateFoodRecommendationsInput
): Promise<GenerateFoodRecommendationsOutput> {
  return generateFoodRecommendationsFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generateFoodRecommendationsPrompt',
  input: {schema: GenerateFoodRecommendationsInputSchema},
  output: {schema: GenerateFoodRecommendationsOutputSchema},
  tools: [searchNearbyPlaces],
  prompt: `You are a personal food and restaurant recommendation assistant. Based on the user's mood, occasion, cuisine preferences, dietary requirements, preferred time, and location, provide a list of 9 personalized food and restaurant recommendations.

Use the searchNearbyPlaces tool to find relevant restaurants.

Mood: {{{mood}}}
Occasion: {{{occasion}}}
Cuisine: {{{cuisine}}}
Dietary Preference: {{{dietaryPreference}}}
Time: {{{time}}}
Location: {{{location}}}
Additional Notes: {{{additionalNotes}}}

Please provide restaurant recommendations that closely align with the details provided.
`,
  config: {
    safetySettings: [
      {
        category: 'HARM_CATEGORY_HATE_SPEECH',
        threshold: 'BLOCK_ONLY_HIGH',
      },
      {
        category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold: 'BLOCK_NONE',
      },
      {
        category: 'HARM_CATEGORY_HARASSMENT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE',
      },
      {
        category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        threshold: 'BLOCK_LOW_AND_ABOVE',
      },
    ],
  },
});

const generateFoodRecommendationsFlow = ai.defineFlow(
  {
    name: 'generateFoodRecommendationsFlow',
    inputSchema: GenerateFoodRecommendationsInputSchema,
    outputSchema: GenerateFoodRecommendationsOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
