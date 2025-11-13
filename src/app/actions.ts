'use server';

import { generateFoodRecommendations } from '@/ai/flows/generate-food-recommendations';
import { z } from 'zod';
import type { ActionState } from '@/lib/types';

const recommendationSchema = z.object({
  mood: z.string().min(1, 'Mood is required.'),
  occasion: z.string().min(1, 'Occasion is required.'),
  cuisine: z.string().min(1, 'Cuisine is required.'),
  dietaryPreference: z.enum(['vegetarian', 'non-vegetarian', 'vegan', 'gluten-free']),
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
    const errorMessages = validatedFields.error.errors.map(e => e.message).join('. ');
    return {
      recommendations: null,
      error: `Invalid form data: ${errorMessages}`,
    };
  }

  try {
    const result = await generateFoodRecommendations(validatedFields.data);
    if (!result.recommendations || result.recommendations.length === 0) {
      return {
        recommendations: [],
        error: null,
      };
    }
    return {
      recommendations: result.recommendations,
      error: null,
    };
  } catch (error) {
    console.error('Error generating recommendations:', error);
    return {
      recommendations: null,
      error: 'Failed to generate recommendations. The AI model might be unavailable. Please try again later.',
    };
  }
}
