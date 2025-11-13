'use server';

/**
 * @fileOverview Processes additional user notes to refine food recommendations.
 *
 * - processAdditionalNotes - Processes the additional notes provided by the user.
 * - ProcessAdditionalNotesInput - The input type for the processAdditionalNotes function.
 * - ProcessAdditionalNotesOutput - The return type for the processAdditionalNotes function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const ProcessAdditionalNotesInputSchema = z.object({
  notes: z.string().describe('Additional notes from the user to refine recommendations.'),
  currentRecommendations: z.string().describe('Current food and restaurant recommendations.'),
});
export type ProcessAdditionalNotesInput = z.infer<typeof ProcessAdditionalNotesInputSchema>;

const ProcessAdditionalNotesOutputSchema = z.object({
  refinedRecommendations: z.string().describe('Refined food and restaurant recommendations based on the notes.'),
});
export type ProcessAdditionalNotesOutput = z.infer<typeof ProcessAdditionalNotesOutputSchema>;

export async function processAdditionalNotes(input: ProcessAdditionalNotesInput): Promise<ProcessAdditionalNotesOutput> {
  return processAdditionalNotesFlow(input);
}

const prompt = ai.definePrompt({
  name: 'processAdditionalNotesPrompt',
  input: {schema: ProcessAdditionalNotesInputSchema},
  output: {schema: ProcessAdditionalNotesOutputSchema},
  prompt: `Refine the following food and restaurant recommendations based on the user's additional notes.

Current Recommendations: {{{currentRecommendations}}}

Additional Notes: {{{notes}}}

Provide refined recommendations that take into account the user's notes. Be concise and clear.
`,
});

const processAdditionalNotesFlow = ai.defineFlow(
  {
    name: 'processAdditionalNotesFlow',
    inputSchema: ProcessAdditionalNotesInputSchema,
    outputSchema: ProcessAdditionalNotesOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
