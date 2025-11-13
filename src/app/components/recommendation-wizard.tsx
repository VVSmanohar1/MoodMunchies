'use client';

import {useActionState, useEffect} from 'react';
import {useFormStatus} from 'react-dom';
import {getRecommendationsAction} from '@/app/actions';
import {useToast} from '@/hooks/use-toast';
import type {ActionState} from '@/lib/types';

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
import {Loader2, Mic, Sparkles, Lightbulb} from 'lucide-react';
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

  useEffect(() => {
    // Only show toast for actual errors, not for fallback success
    if (state.error && !state.isFallback) {
      toast({
        variant: 'destructive',
        title: 'Oh no! Something went wrong.',
        description: state.error,
      });
    }
  }, [state, toast]);

  return (
    <form action={formAction} className="w-full max-w-6xl space-y-12">
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
              <Select name="mood" required>
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
              <Select name="occasion" required>
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
              <Select name="cuisine" defaultValue="any" required>
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
              <Select name="time" required>
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
              />
            </div>
          </div>
          <div>
            <Label>Any dietary preferences?</Label>
            <RadioGroup
              name="dietaryPreference"
              defaultValue="non-vegetarian"
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
            />
          </div>
        </CardContent>
      </Card>
      <ResultsAndSubmit state={state} />
    </form>
  );
}

function ResultsAndSubmit({state}: {state: ActionState}) {
  const {pending} = useFormStatus();
  const {toast} = useToast();

  return (
    <>
      <div className="flex items-center justify-between">
        <Button
          type="button"
          variant="outline"
          size="lg"
          onClick={() =>
            toast({
              title: 'Coming Soon!',
              description: 'Voice input feature is under development.',
            })
          }
        >
          <Mic /> Use Voice
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
                <Alert className="border-primary/50 text-primary-foreground bg-primary/10">
                  <Info className="h-4 w-4 !text-primary" />
                  <AlertTitle className="font-bold">
                    Using Fallback Suggestions
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
