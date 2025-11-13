'use server';

import {generateFoodRecommendations} from '@/ai/flows/generate-food-recommendations';
import {z} from 'zod';
import type {ActionState, Recommendation} from '@/lib/types';
import * as fs from 'fs/promises';
import * as path from 'path';

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

const cacheFilePath = path.resolve(
  process.cwd(),
  'src',
  'lib',
  'cached-recommendations.json'
);

async function readCache(): Promise<Recommendation[]> {
  try {
    const data = await fs.readFile(cacheFilePath, 'utf-8');
    const parsed = JSON.parse(data);
    return parsed.recommendations || [];
  } catch (error) {
    console.warn('Cache read failed, starting with empty cache:', error);
    return [];
  }
}

async function writeCache(recommendations: Recommendation[]): Promise<void> {
  try {
    await fs.writeFile(
      cacheFilePath,
      JSON.stringify({recommendations}, null, 2)
    );
  } catch (error) {
    console.error('Failed to write to cache:', error);
  }
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
    // Attempt to get fresh recommendations from the AI
    const result = await generateFoodRecommendations(validatedFields.data);
    if (!result.recommendations || result.recommendations.length === 0) {
      // If AI returns no results, still treat it as a non-error state
      return {
        recommendations: [],
        error: null,
        isFallback: false,
      };
    }

    // AI call was successful, update the cache
    const existingRecs = await readCache();
    const newRecs = result.recommendations;

    // Create a Set of existing restaurant names for quick lookup
    const existingRestaurantNames = new Set(
      existingRecs.map(rec => rec.restaurantName.toLowerCase())
    );
    
    // Filter out duplicates from the new recommendations
    const uniqueNewRecs = newRecs.filter(
      rec => !existingRestaurantNames.has(rec.restaurantName.toLowerCase())
    );

    // Combine and write back to cache if there are any unique new ones
    if (uniqueNewRecs.length > 0) {
      const updatedCache = [...existingRecs, ...uniqueNewRecs];
      await writeCache(updatedCache);
    }
    
    // Return the fresh recommendations from the AI
    return {
      recommendations: newRecs,
      error: null,
      isFallback: false,
    };
  } catch (error) {
    console.error('Error generating recommendations, serving from cache:', error);
    
    // AI call failed, fallback to local cache
    const cachedRecs = await readCache();
    
    if (cachedRecs.length > 0) {
      return {
        recommendations: cachedRecs.slice(0, 9), // Show up to 9 from cache
        error:
          'The AI is currently unavailable, but here are some suggestions from my memory!',
        isFallback: true,
      };
    }

    // If cache is also empty, return an error
    return {
      recommendations: [],
      error: 'The AI is currently unavailable and I could not find any cached recommendations. Please try again later.',
      isFallback: false,
    };
  }
}
