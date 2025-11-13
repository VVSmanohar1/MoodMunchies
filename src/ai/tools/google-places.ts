'use server';

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const NearbySearchInputSchema = z.object({
  query: z
    .string()
    .describe(
      'The text query to search for (e.g., "restaurants in San Francisco").'
    ),
});

const PlaceSchema = z.object({
  name: z.string().describe('The name of the place.'),
  photoReference: z
    .string()
    .optional()
    .describe('A reference for a photo of the place.'),
});

const NearbySearchOutputSchema = z.object({
  places: z
    .array(PlaceSchema)
    .describe('A list of places that match the search query.'),
});

export const searchNearbyPlaces = ai.defineTool(
  {
    name: 'searchNearbyPlaces',
    description: 'Search for nearby places using the Google Places API.',
    inputSchema: NearbySearchInputSchema,
    outputSchema: NearbySearchOutputSchema,
  },
  async input => {
    // This tool is not actively used but kept for potential future use.
    // It currently returns an empty array to avoid errors.
    console.warn("searchNearbyPlaces tool was called but is configured to return no results.");
    return {places: []};
  }
);
