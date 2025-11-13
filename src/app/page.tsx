import { Header } from "@/app/components/header";
import { RecommendationWizard } from "@/app/components/recommendation-wizard";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto flex flex-col items-center justify-center gap-12 px-4 py-16">
          <div className="flex flex-col items-center gap-4 text-center">
            <h1 className="font-headline text-5xl font-bold tracking-tight md:text-6xl">
              How are you feeling today?
            </h1>
            <p className="max-w-2xl text-lg text-foreground/80 md:text-xl">
              Tell us your mood, and we'll find the perfect munchies for you.
              From comforting classics to adventurous new flavors, let your mood guide your meal.
            </p>
          </div>
          <RecommendationWizard />
        </div>
      </main>
    </div>
  );
}
