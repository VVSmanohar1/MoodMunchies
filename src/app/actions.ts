'use server';

import {z} from 'zod';
import type {ActionState, Recommendation} from '@/lib/types';
import fallbackRecs from '@/lib/fallback-recommendations.json';

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

/**
 * Calls an async function with a retry mechanism and exponential backoff.
 * @param fn The async function to call.
 * @param maxRetries The maximum number of retries.
 * @returns The result of the function call.
 */
async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      // Check for a specific error type if possible, e.g., a 503 status.
      // For this generic example, we'll retry on any error.
      if (i === maxRetries - 1) {
        throw error; // Last retry failed, throw the error
      }
      // Exponential backoff: 1s, 2s, 4s...
      const delay = Math.pow(2, i) * 1000 + Math.random() * 1000;
      console.warn(`AI call failed, retrying in ${Math.round(delay)}ms... (Attempt ${i + 1})`);
      await new Promise(res => setTimeout(res, delay));
    }
  }
  // This line should not be reachable if maxRetries > 0
  throw new Error('Exceeded max retries');
}

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
    // Attempt to get fresh recommendations from the Python ML API with retry logic
    const result = await callWithRetry(async () => {
      const apiUrl = process.env.ML_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mood: validatedFields.data.mood,
          occasion: validatedFields.data.occasion,
          cuisine: validatedFields.data.cuisine,
          dietaryPreference: validatedFields.data.dietaryPreference,
          time: validatedFields.data.time,
          location: validatedFields.data.location,
          additionalNotes: validatedFields.data.additionalNotes || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`ML API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    });

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
    console.error('Error generating recommendations from ML API after retries, serving from fallback:', error);
    
    // Fallback to a static, curated list of recommendations
    const staticFallback: Recommendation[] = fallbackRecs.recommendations;
    
    if (staticFallback.length > 0) {
      return {
        recommendations: staticFallback,
        error:
          'The AI is currently unavailable, but here are some popular suggestions!',
        isFallback: true,
      };
    }

    // If static fallback is also empty for some reason, return an error
    return {
      recommendations: [],
      error: 'The AI is currently unavailable and I could not find any fallback recommendations. Please try again later.',
      isFallback: false,
    };
  }
}
