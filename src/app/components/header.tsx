import { UtensilsCrossed } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-start space-x-4 px-4">
        <div className="flex items-center gap-3">
          <UtensilsCrossed className="h-7 w-7 text-primary" />
          <span className="font-headline text-2xl font-bold">
            Mood Munchies
          </span>
        </div>
      </div>
    </header>
  );
}
