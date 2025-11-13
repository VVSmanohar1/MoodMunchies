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
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('Google Maps API key is not set.');
    }

    const response = await fetch(
      `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${encodeURIComponent(
        input.query
      )}&key=${apiKey}`
    );

    if (!response.ok) {
      throw new Error(
        `Failed to fetch places: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    const places = data.results.map((result: any) => ({
      name: result.name,
      photoReference: result.photos?.[0]?.photo_reference,
    }));

    return {places};
  }
);
