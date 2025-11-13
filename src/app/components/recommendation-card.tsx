import Image from "next/image";
import type { Recommendation } from "@/lib/types";
import { PlaceHolderImages } from "@/lib/placeholder-images";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Utensils, MapPin, Phone } from "lucide-react";

interface RecommendationCardProps {
  recommendation: Recommendation;
  index: number;
}

export function RecommendationCard({ recommendation, index }: RecommendationCardProps) {
  const placeholder = PlaceHolderImages[index % PlaceHolderImages.length];
  
  // We'll use placeholder images since we are not using Google Maps API for photos.
  const imageUrl = placeholder.imageUrl;

  return (
    <Card className="overflow-hidden transition-all hover:shadow-xl hover:-translate-y-1 duration-300 flex flex-col">
      <CardHeader className="p-0">
        <div className="relative h-48 w-full">
            <Image
              src={imageUrl}
              alt={recommendation.restaurantName}
              fill
              className="object-cover"
              data-ai-hint={placeholder.imageHint}
            />
        </div>
      </CardHeader>
      <CardContent className="p-6 flex-grow flex flex-col">
        <CardTitle className="font-headline text-2xl">{recommendation.restaurantName}</CardTitle>
        <CardDescription className="flex items-center gap-2 pt-2 text-primary font-semibold">
          <Utensils className="h-4 w-4" />
          {recommendation.foodSuggestion}
        </CardDescription>
        
        <p className="mt-4 text-foreground/80 text-sm italic">
          "{recommendation.reasonForRecommendation}"
        </p>

        <div className="mt-4 flex-grow space-y-3 text-sm text-foreground/90">
            <div className="flex items-start gap-3">
                <MapPin className="h-4 w-4 mt-0.5 shrink-0" />
                <span>{recommendation.address}</span>
            </div>
            {recommendation.contactDetails && (
                 <div className="flex items-center gap-3">
                    <Phone className="h-4 w-4" />
                    <span>{recommendation.contactDetails}</span>
                </div>
            )}
        </div>
      </CardContent>
    </Card>
  );
}
