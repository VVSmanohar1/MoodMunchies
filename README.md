# Mood Munchies

Welcome to Mood Munchies, a personalized food recommendation application powered by Machine Learning. Based on your mood, the occasion, and your food preferences, Mood Munchies suggests the perfect meal for you from real restaurants, complete with images and details.

## Core Features

- **ML-Powered Recommendations**: Utilizes a Python-based ML recommendation engine using content-based filtering and mood mapping algorithms.
- **Mood-Based Matching**: Advanced feature engineering that maps user moods to restaurant characteristics for personalized suggestions.
- **Intuitive UI**: A simple and clean interface makes it easy to input your preferences and receive recommendations.
- **Detailed Suggestions**: Each recommendation includes the restaurant's name, a food suggestion, a reason for the choice, address, and contact details.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or later recommended)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)
- [Python](https://www.python.org/downloads/) (v3.8 or later recommended)
- [pip](https://pip.pypa.io/en/stable/) (usually comes with Python)

### Installation

1.  Clone the repository to your local machine.
2.  Navigate to the project directory:
    ```bash
    cd <project-folder>
    ```
3.  Install the Node.js dependencies:
    ```bash
    npm install
    ```
4.  Set up the Python ML backend:
    ```bash
    cd python_ml
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    ```

### Running the Application

1. **Start the Python ML API server** (in a separate terminal):
    ```bash
    cd python_ml
    # Activate virtual environment if not already activated
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    python -m uvicorn api.main:app --reload --port 8000
    ```

2. **Start the Next.js frontend** (in another terminal):
    ```bash
    npm run dev
    ```

The application will be available at [http://localhost:9002](http://localhost:9002).

**Note**: Make sure the Python ML API is running on port 8000 before using the application. You can configure a different API URL by setting the `ML_API_URL` environment variable.

## Project Structure

- `src/app/`: Contains the main pages and components of the Next.js application.
  - `page.tsx`: The entry point and main page of the app.
  - `components/recommendation-wizard.tsx`: The main form component where users input their preferences.
  - `components/recommendation-card.tsx`: The component used to display each individual recommendation.
  - `actions.ts`: Server-side actions that call the Python ML API for recommendations.
- `python_ml/`: Python ML recommendation system.
  - `api/main.py`: FastAPI server that serves restaurant recommendations.
  - `ml_engine/recommendation_engine.py`: Core ML recommendation engine with content-based filtering.
  - `data/restaurants.json`: Restaurant dataset with mood, occasion, and feature mappings.
- `src/lib/`: Includes utility functions, type definitions, and placeholder data.
- `public/`: Static assets for the application.

## How It Works

Mood Munchies uses a Python-based Machine Learning recommendation system. When a user submits their preferences through the recommendation wizard, a server action is triggered. This action calls the Python ML API, which uses:

1. **Content-Based Filtering**: Matches restaurants based on mood, occasion, cuisine, dietary preferences, and time of day.
2. **Feature Engineering**: Each restaurant has mood scores, occasion scores, and time scores that are used for matching.
3. **TF-IDF Vectorization**: Text-based similarity matching using cuisine, ambiance, and dish information.
4. **Weighted Scoring**: Combines multiple factors (mood 30%, occasion 30%, time 10%, cuisine 10%, content similarity 10%, additional notes 10%) to rank recommendations.

The ML engine returns a list of personalized restaurant recommendations, which are then displayed to the user in a series of recommendation cards.

## ML Algorithm Details

The recommendation system uses a sophisticated scoring algorithm:

- **Mood Matching (30%)**: Each restaurant has compatibility scores for different moods (happy, sad, stressed, adventurous, relaxed, celebratory).
- **Occasion Matching (30%)**: Restaurants are scored for different occasions (casual meal, celebration, quick bite, date night, family dinner).
- **Time Matching (10%)**: Restaurants have time-of-day preferences (breakfast, brunch, lunch, dinner, snack).
- **Cuisine Matching (10%)**: Exact cuisine match gets full score, "any" cuisine accepts all, mismatches get partial score.
- **Content Similarity (10%)**: TF-IDF cosine similarity based on restaurant features.
- **Additional Notes (10%)**: Keyword-based preference extraction (spicy, quiet, romantic, etc.).

See `python_ml/README.md` for more detailed documentation about the ML system.
