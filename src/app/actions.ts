'use server';

import {generateFoodRecommendations} from '@/ai/flows/generate-food-recommendations';
import {z} from 'zod';
import type {ActionState} from '@/lib/types';
import fallbackData from '@/lib/fallback-recommendations.json';

const recommendationSchema = z.object({
  mood: z.string().min(1, 'Mood is required.'),
  occasion: z.string().min(1, 'Occasion is required.'),
  cuisine: z.string().min(1, 'Cuisine is required.'),
  dietaryPreference: z.enum([
    'vegetarian',
    'non-vegetarian',
    'vegan',
    'gluten-free',
  ]),
  time: z.string().min(1, 'Time is required.'),
  location: z.string().min(3, 'Location must be at least 3 characters.'),
  additionalNotes: z.string().optional(),
});

export async function getRecommendationsAction(
  prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  const validatedFields = recommendationSchema.safeParse({
    mood: formData.get('mood'),
    occasion: formData.get('occasion'),
    cuisine: formData.get('cuisine'),
    dietaryPreference: formData.get('dietaryPreference'),
    time: formData.get('time'),
    location: formData.get('location'),
    additionalNotes: formData.get('additionalNotes'),
  });

  if (!validatedFields.success) {
    const errorMessages = validatedFields.error.errors
      .map(e => e.message)
      .join('. ');
    return {
      recommendations: null,
      error: `Invalid form data: ${errorMessages}`,
      isFallback: false,
    };
  }

  try {
    const result = await generateFoodRecommendations(validatedFields.data);
    if (!result.recommendations || result.recommendations.length === 0) {
      return {
        recommendations: [],
        error: null,
        isFallback: false,
      };
    }
    return {
      recommendations: result.recommendations,
      error: null,
      isFallback: false,
    };
  } catch (error) {
    console.error('Error generating recommendations, serving fallback:', error);
    // Fallback to local data if AI fails
    return {
      recommendations: fallbackData.recommendations,
      error:
        'The AI is currently unavailable, but here are some popular suggestions!',
      isFallback: true,
    };
  }
}
