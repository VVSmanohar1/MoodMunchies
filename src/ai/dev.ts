import { config } from 'dotenv';
config();

import '@/ai/flows/process-additional-notes.ts';
import '@/ai/flows/generate-food-recommendations.ts';
import '@/ai/tools/google-places.ts';
