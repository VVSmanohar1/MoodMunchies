import Image from "next/image";
import type { Recommendation } from "@/lib/types";
import { PlaceHolderImages } from "@/lib/placeholder-images";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Utensils } from "lucide-react";

interface RecommendationCardProps {
  recommendation: Recommendation;
  index: number;
}

export function RecommendationCard({ recommendation, index }: RecommendationCardProps) {
  const placeholder = PlaceHolderImages[index % PlaceHolderImages.length];

  return (
    <Card className="overflow-hidden transition-all hover:shadow-xl hover:-translate-y-1 duration-300">
      <CardHeader className="p-0">
        <div className="relative h-48 w-full">
          {placeholder && (
            <Image
              src={placeholder.imageUrl}
              alt={placeholder.description}
              fill
              className="object-cover"
              data-ai-hint={placeholder.imageHint}
            />
          )}
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <CardTitle className="font-headline text-2xl">{recommendation.restaurantName}</CardTitle>
        <CardDescription className="flex items-center gap-2 pt-2 text-primary font-semibold">
          <Utensils className="h-4 w-4" />
          {recommendation.foodSuggestion}
        </CardDescription>
        <p className="mt-4 text-foreground/80">
          {recommendation.description}
        </p>
      </CardContent>
    </Card>
  );
}
