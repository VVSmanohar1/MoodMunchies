# Mood Munchies

Welcome to Mood Munchies, a personalized food recommendation application powered by AI. Based on your mood, the occasion, and your food preferences, Mood Munchies suggests the perfect meal for you from real restaurants, complete with images and details.

## Core Features

- **AI-Powered Recommendations**: Utilizes a powerful AI model to generate personalized restaurant and food suggestions.
- **Dynamic Image Generation**: The AI creates a unique image for each restaurant recommendation, providing a visual taste of what to expect.
- **Intuitive UI**: A simple and clean interface makes it easy to input your preferences and receive recommendations.
- **Detailed Suggestions**: Each recommendation includes the restaurant's name, a food suggestion, a reason for the choice, address, and contact details.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or later recommended)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)

### Installation

1.  Clone the repository to your local machine.
2.  Navigate to the project directory:
    ```bash
    cd <project-folder>
    ```
3.  Install the necessary dependencies:
    ```bash
    npm install
    ```

### Running the Application

To start the development server, run the following command:

```bash
npm run dev
```

The application will be available at [http://localhost:9002](http://localhost:9002).

## Project Structure

- `src/app/`: Contains the main pages and components of the Next.js application.
  - `page.tsx`: The entry point and main page of the app.
  - `components/recommendation-wizard.tsx`: The main form component where users input their preferences.
  - `components/recommendation-card.tsx`: The component used to display each individual recommendation.
  - `actions.ts`: Server-side actions for handling form submissions.
- `src/ai/`: Home to the AI-related logic and Genkit flows.
  - `flows/generate-food-recommendations.ts`: The core Genkit flow that communicates with the AI model to get recommendations and generate images.
- `src/lib/`: Includes utility functions, type definitions, and placeholder data.
- `public/`: Static assets for the application.

## How It Works

Mood Munchies uses the Genkit framework to interact with a generative AI model. When a user submits their preferences through the recommendation wizard, a server action is triggered. This action calls the `generateFoodRecommendations` flow, which constructs a detailed prompt for the AI. The AI then returns a list of personalized restaurant recommendations, including generating a unique image for each one. The results are then displayed to the user in a series of recommendation cards.
