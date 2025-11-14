'use client';

import {useActionState, useEffect, useState, useTransition} from 'react';
import {useFormStatus} from 'react-dom';
import {getRecommendationsAction} from '@/app/actions';
import {useToast} from '@/hooks/use-toast';
import type {ActionState} from '@/lib/types';
import {VoiceInput, type ExtractedPreferences} from '@/components/voice-input';

import {Card, CardContent, CardHeader, CardTitle} from '@/components/ui/card';
import {Label} from '@/components/ui/label';
import {Input} from '@/components/ui/input';
import {Textarea} from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {RadioGroup, RadioGroupItem} from '@/components/ui/radio-group';
import {Button} from '@/components/ui/button';
import {Loader2, Mic, Sparkles, Lightbulb, History} from 'lucide-react';
import {Skeleton} from '@/components/ui/skeleton';
import {RecommendationCard} from './recommendation-card';
import {Alert, AlertDescription, AlertTitle} from '@/components/ui/alert';
import {Info} from 'lucide-react';

const initialState: ActionState = {
  recommendations: null,
  error: null,
  isFallback: false,
};

const moods = [
  'Happy',
  'Sad',
  'Stressed',
  'Adventurous',
  'Relaxed',
  'Celebratory',
];
const occasions = [
  'Casual Meal',
  'Celebration',
  'Quick Bite',
  'Date Night',
  'Family Dinner',
];
const cuisines = [
  'Any',
  'Italian',
  'Mexican',
  'Indian',
  'Japanese',
  'Chinese',
  'American',
];
const times = ['Breakfast', 'Brunch', 'Lunch', 'Dinner', 'Snack'];
const dietaryPreferences = [
  {value: 'non-vegetarian', label: 'Non-Vegetarian'},
  {value: 'vegetarian', label: 'Vegetarian'},
  {value: 'vegan', label: 'Vegan'},
  {value: 'gluten-free', label: 'Gluten-Free'},
];

export function RecommendationWizard() {
  const [state, formAction] = useActionState(
    getRecommendationsAction,
    initialState
  );
  const {toast} = useToast();
  
  // Form state for controlled components
  const [formData, setFormData] = useState({
    mood: '',
    occasion: '',
    cuisine: 'any',
    dietaryPreference: 'non-vegetarian',
    time: '',
    location: '',
    additionalNotes: '',
  });
  
  const [showVoiceInput, setShowVoiceInput] = useState(false);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    // Only show toast for actual errors, not for fallback success message
    if (state.error && !state.isFallback) {
      toast({
        variant: 'destructive',
        title: 'Oh no! Something went wrong.',
        description: state.error,
      });
    }
  }, [state, toast]);

  const handleVoicePreferences = (preferences: ExtractedPreferences) => {
    const updates: Partial<typeof formData> = {};
    
    if (preferences.mood) {
      updates.mood = preferences.mood.toLowerCase();
    }
    if (preferences.occasion) {
      updates.occasion = preferences.occasion.toLowerCase();
    }
    if (preferences.cuisine) {
      updates.cuisine = preferences.cuisine.toLowerCase();
    }
    if (preferences.dietaryPreference) {
      updates.dietaryPreference = preferences.dietaryPreference.toLowerCase();
    }
    if (preferences.time) {
      updates.time = preferences.time.toLowerCase();
    }
    if (preferences.location) {
      updates.location = preferences.location;
    }
    if (preferences.additionalNotes) {
      updates.additionalNotes = preferences.additionalNotes;
    }
    
    setFormData(prev => ({...prev, ...updates}));
    
    toast({
      title: 'Preferences extracted!',
      description: 'Your voice preferences have been filled in. Review and submit when ready.',
    });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formDataObj = new FormData(form);
    
    // Use form state values if available, otherwise use form data
    if (formData.mood) formDataObj.set('mood', formData.mood);
    if (formData.occasion) formDataObj.set('occasion', formData.occasion);
    if (formData.cuisine) formDataObj.set('cuisine', formData.cuisine);
    if (formData.dietaryPreference) formDataObj.set('dietaryPreference', formData.dietaryPreference);
    if (formData.time) formDataObj.set('time', formData.time);
    if (formData.location) formDataObj.set('location', formData.location);
    if (formData.additionalNotes) formDataObj.set('additionalNotes', formData.additionalNotes);
    
    // Wrap formAction call in startTransition
    startTransition(() => {
      formAction(formDataObj);
    });
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-6xl space-y-12">
      {showVoiceInput && (
        <VoiceInput
          onPreferencesExtracted={handleVoicePreferences}
          autoExtract={true}
        />
      )}
      
      <Card className="shadow-lg border-2 border-primary/20">
        <CardHeader>
          <CardTitle className="font-headline text-3xl">
            Find Your Flavor
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <Label htmlFor="mood">What's your mood?</Label>
              <Select
                name="mood"
                required
                value={formData.mood}
                onValueChange={(value) => setFormData(prev => ({...prev, mood: value}))}
              >
                <SelectTrigger id="mood">
                  <SelectValue placeholder="Select a mood" />
                </SelectTrigger>
                <SelectContent>
                  {moods.map(mood => (
                    <SelectItem key={mood} value={mood.toLowerCase()}>
                      {mood}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="occasion">What's the occasion?</Label>
              <Select
                name="occasion"
                required
                value={formData.occasion}
                onValueChange={(value) => setFormData(prev => ({...prev, occasion: value}))}
              >
                <SelectTrigger id="occasion">
                  <SelectValue placeholder="Select an occasion" />
                </SelectTrigger>
                <SelectContent>
                  {occasions.map(occasion => (
                    <SelectItem key={occasion} value={occasion.toLowerCase()}>
                      {occasion}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div>
              <Label htmlFor="cuisine">Craving a cuisine?</Label>
              <Select
                name="cuisine"
                required
                value={formData.cuisine}
                onValueChange={(value) => setFormData(prev => ({...prev, cuisine: value}))}
              >
                <SelectTrigger id="cuisine">
                  <SelectValue placeholder="Select a cuisine" />
                </SelectTrigger>
                <SelectContent>
                  {cuisines.map(cuisine => (
                    <SelectItem key={cuisine} value={cuisine.toLowerCase()}>
                      {cuisine}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="time">Time of day?</Label>
              <Select
                name="time"
                required
                value={formData.time}
                onValueChange={(value) => setFormData(prev => ({...prev, time: value}))}
              >
                <SelectTrigger id="time">
                  <SelectValue placeholder="Select a time" />
                </SelectTrigger>
                <SelectContent>
                  {times.map(time => (
                    <SelectItem key={time} value={time.toLowerCase()}>
                      {time}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="location">Your location?</Label>
              <Input
                id="location"
                name="location"
                placeholder="e.g., Downtown, San Francisco"
                required
                value={formData.location}
                onChange={(e) => setFormData(prev => ({...prev, location: e.target.value}))}
              />
            </div>
          </div>
          <div>
            <Label>Any dietary preferences?</Label>
            <RadioGroup
              name="dietaryPreference"
              value={formData.dietaryPreference}
              onValueChange={(value) => setFormData(prev => ({...prev, dietaryPreference: value}))}
              className="mt-2 flex flex-wrap gap-4"
            >
              {dietaryPreferences.map(pref => (
                <div key={pref.value} className="flex items-center space-x-2">
                  <RadioGroupItem value={pref.value} id={pref.value} />
                  <Label htmlFor={pref.value} className="font-normal">
                    {pref.label}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </div>
          <div>
            <Label htmlFor="additionalNotes">Any other notes?</Label>
            <Textarea
              id="additionalNotes"
              name="additionalNotes"
              placeholder="e.g., 'Looking for a quiet place', 'Something spicy!'"
              value={formData.additionalNotes}
              onChange={(e) => setFormData(prev => ({...prev, additionalNotes: e.target.value}))}
            />
          </div>
        </CardContent>
      </Card>
      <ResultsAndSubmit state={state} showVoiceInput={showVoiceInput} onToggleVoice={() => setShowVoiceInput(!showVoiceInput)} />
    </form>
  );
}

function ResultsAndSubmit({
  state,
  showVoiceInput,
  onToggleVoice,
}: {
  state: ActionState;
  showVoiceInput: boolean;
  onToggleVoice: () => void;
}) {
  const {pending} = useFormStatus();
  const {toast} = useToast();

  return (
    <>
      <div className="flex items-center justify-between">
        <Button
          type="button"
          variant={showVoiceInput ? 'default' : 'outline'}
          size="lg"
          onClick={onToggleVoice}
        >
          <Mic /> {showVoiceInput ? 'Hide Voice Input' : 'Use Voice'}
        </Button>
        <Button type="submit" size="lg" disabled={pending} className="font-bold">
          {pending ? <Loader2 className="animate-spin" /> : <Sparkles />}
          Get Recommendations
        </Button>
      </div>

      <div className="pt-8">
        {pending && <LoadingSkeletons />}
        {!pending &&
          state.recommendations &&
          state.recommendations.length > 0 && (
            <div className="space-y-8">
              {state.isFallback && (
                <Alert className="border-amber-500/50 text-amber-900 bg-amber-500/10 dark:text-amber-200 dark:border-amber-500/50 dark:bg-amber-900/20">
                  <History className="h-4 w-4 !text-amber-600 dark:!text-amber-400" />
                  <AlertTitle className="font-bold">
                    Using Cached Suggestions
                  </AlertTitle>
                  <AlertDescription>{state.error}</AlertDescription>
                </Alert>
              )}
              <h2 className="font-headline text-4xl font-bold text-center">
                Your Culinary Matches
              </h2>
              <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 animate-in fade-in-50 duration-500">
                {state.recommendations.map((rec, index) => (
                  <RecommendationCard
                    key={index}
                    recommendation={rec}
                    index={index}
                  />
                ))}
              </div>
            </div>
          )}
        {!pending && state.recommendations?.length === 0 && <EmptyState />}
      </div>
    </>
  );
}

function LoadingSkeletons() {
  return (
    <div className="space-y-8">
      <Skeleton className="h-10 w-1/2 mx-auto" />
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(9)].map((_, i) => (
          <div key={i} className="flex flex-col space-y-3">
            <Skeleton className="h-[200px] w-full rounded-xl" />
            <div className="space-y-2">
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-5/6" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-muted bg-card/50 p-12 text-center animate-in fade-in-50">
      <Lightbulb className="h-12 w-12 text-muted-foreground" />
      <h3 className="mt-4 text-xl font-semibold font-headline">
        No Matches Found
      </h3>
      <p className="mt-2 text-muted-foreground">
        We couldn't find any recommendations for your criteria. Try being a bit
        more general!
      </p>
    </div>
  );
}
