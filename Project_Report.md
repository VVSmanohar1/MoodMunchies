
# **A Project Report on**
## **Mood Munchies: A Mood-Based Restaurant Recommendation System**

---

### **ABSTRACT**

Choosing a restaurant can be a complex decision influenced by more than just cuisine or location. Factors like mood, the social occasion, and specific cravings play a significant role, yet are often overlooked by traditional recommendation platforms. This project, "Mood Munchies," introduces a personalized restaurant recommendation system that leverages machine learning to address this gap. The application provides users with tailored restaurant and meal suggestions by analyzing their current mood, the occasion, cuisine preferences, and other contextual factors. 

The core of the system is a Python-based recommendation engine that employs a hybrid content-based filtering model. It calculates a weighted score for restaurants based on their compatibility with user inputs, including mood matching, occasion appropriateness, time of day, and cuisine type. The frontend is a modern, intuitive web application built with Next.js, designed for a seamless user experience. This report details the complete lifecycle of the project, from the initial concept and design to implementation, testing, and potential future enhancements. The project successfully demonstrates the integration of sentiment analysis into recommendation algorithms to create a more intelligent, personalized, and human-centric user experience.

---

### **TABLE OF CONTENTS**

*   CHAPTER 1: INTRODUCTION
*   CHAPTER 2: LITERATURE SURVEY
*   CHAPTER 3: PROPOSED SYSTEM
*   CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION
*   CHAPTER 5: DESIGN
*   CHAPTER 6: IMPLEMENTATION
*   CHAPTER 7: CODING
*   CHAPTER 8: TESTING
*   CHAPTER 9: RESULT
*   CHAPTER 10: TIMELINE OF THE PROJECT
*   CHAPTER 11: CONCLUSION
*   CHAPTER 12: FUTURE ENHANCEMENTS
*   CHAPTER 13: PROJECT OUTCOME-POS/PSOS MAPPING
*   CHAPTER 14: REFERENCES

---

### **CHAPTER 1: INTRODUCTION**

#### **1.1 Project Idea**
The core idea of "Mood Munchies" is to create a smart, personalized food recommendation application. Unlike conventional platforms that rely on generic filters like cuisine or price, this application suggests restaurants and meals by primarily considering the user's emotional state (mood) and the context of the meal (occasion).

#### **1.2 Motivation of the Project**
The motivation stems from the common dilemma of "what to eat?". This decision is often influenced by how we feel. A person feeling celebratory might desire a different dining experience than someone feeling stressed or relaxed. Existing recommendation systems fail to capture this nuanced, human element of decision-making. This project aims to make the process of choosing a restaurant more intuitive, personal, and satisfying.

#### **1.3 Problem Statement**
To design and develop a web-based restaurant recommendation system that utilizes a machine learning model to provide personalized suggestions based on a user's mood, occasion, cuisine preference, time of day, and other dietary notes. The system should offer a user-friendly interface for input and display detailed, actionable recommendations.

#### **1.4 Statement of Scope**
The project encompasses the development of two main components:
1.  A frontend web application with an intuitive UI for users to input their preferences.
2.  A backend machine learning service that processes user inputs, applies a custom recommendation algorithm, and returns a ranked list of restaurant suggestions.
The scope is limited to providing recommendations from a pre-defined dataset of restaurants and does not include features like live reservations or order placements.

#### **1.5 Goals and Objectives**
*   **Goal:** To build a functional and effective mood-based restaurant recommendation system.
*   **Objectives:**
    *   To develop a sophisticated ML recommendation engine using content-based filtering and a custom mood-matching algorithm.
    *   To build a clean, responsive, and intuitive user interface using Next.js and Tailwind CSS.
    *   To integrate the frontend with the backend ML service via a REST API.
    *   To curate a dataset of restaurants with attributes suitable for mood and occasion-based filtering.
    *   To test the system thoroughly to ensure functionality and quality of recommendations.

---

### **CHAPTER 2: LITERATURE SURVEY**

#### **2.1 Literature Survey**
Recommendation systems are a well-researched area of data science. The two most prominent techniques are:
*   **Collaborative Filtering:** This method builds a model from a user's past behaviors (items previously purchased or rated) as well as decisions made by similar users.
*   **Content-Based Filtering:** This method uses the attributes of an item to recommend other items with similar properties.
This project employs a hybrid approach, primarily using content-based filtering where the "content" includes not just standard restaurant attributes (like cuisine) but also specially engineered features for "mood" and "occasion."

#### **2.2 Existing System**
Existing systems for restaurant discovery include platforms like Yelp, Zomato, and Google Maps. These platforms offer robust search and filtering capabilities based on:
*   Cuisine (Italian, Mexican, etc.)
*   Location (City, Neighborhood)
*   Price Range
*   User Ratings and Reviews

#### **2.3 Disadvantages of Existing System**
*   **Lack of Personalization:** They do not account for the user's current mood or the specific context of the dining occasion.
*   **Information Overload:** A search can often return hundreds of options, leading to decision fatigue.
*   **Generic Reviews:** User reviews are subjective and may not align with the specific needs of a user at a given moment. For example, a restaurant perfect for a lively party might be poorly rated by someone who was seeking a quiet dinner.

#### **2.4 Feasibility Study**
*   **Technical Feasibility:** The project is highly feasible. The required technologies (Next.js for the frontend, Python for the backend) are open-source, well-documented, and widely used. The ML algorithms are based on established principles.
*   **Economic Feasibility:** As a software-based project using open-source tools, the primary cost is development time. Deployment costs can be minimized or eliminated by using free-tier services offered by cloud providers.
*   **Operational Feasibility:** The system is designed to be straightforward and easy to operate. Users with basic web literacy can easily navigate the interface to get recommendations, requiring no special training.

---

### **CHAPTER 3: PROPOSED SYSTEM**

#### **3.1 Proposed System**
The proposed system, "Mood Munchies," is a smart recommendation engine that acts as a personal dining assistant. It moves beyond generic filters by creating a direct link between a user's feelings and the dining experience. By inputting their mood (e.g., Happy, Stressed, Adventurous), occasion (e.g., Date Night, Family Dinner), and other standard preferences, users receive a small, curated list of highly relevant restaurant suggestions.

#### **3.2 Methodology**
The methodology is centered around a hybrid recommendation model:
1.  **User Input:** The user provides their mood, occasion, preferred time, cuisine, and any other specific notes through the web interface.
2.  **API Request:** The frontend sends this data to the backend Python API.
3.  **Scoring Algorithm:** The backend ML engine iterates through the restaurant dataset and calculates a "match score" for each restaurant based on a weighted algorithm.
4.  **Ranking:** Restaurants are ranked based on their final score.
5.  **Response:** The top-ranked recommendations are sent back to the frontend.
6.  **Display:** The UI presents the recommendations, including details like the restaurant's name, address, and the reason for the suggestion.

#### **3.3 Advantages**
*   **Highly Personalized:** Recommendations are tailored to the user's emotional and situational context.
*   **Reduces Decision Fatigue:** By providing a few high-quality suggestions instead of a long list, the system simplifies the choice.
*   **Novelty and Engagement:** The unique mood-based approach offers a more engaging and enjoyable user experience.
*   **Improved Satisfaction:** Users are more likely to be satisfied with a choice that aligns with their mood and occasion.

#### **3.4 Approaches**
The development approach is modular, separating the frontend (user interface) from the backend (recommendation logic). This follows modern software architecture principles, allowing for independent development, testing, and scaling of each component.

---

### **CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION**

#### **4.1 Software Requirements**
*   **Operating System:** Windows, macOS, or Linux
*   **Web Browser:** Google Chrome, Mozilla Firefox, Safari, or Microsoft Edge
*   **Frontend Framework:** Next.js / React.js
*   **Backend Language/Framework:** Python / FastAPI
*   **Key Python Libraries:** Pandas, Scikit-learn
*   **Node.js Environment:** For running the frontend development server and build process.
*   **Code Editor:** Visual Studio Code or similar.

#### **4.2 Technologies Used**
*   **TypeScript:** For type-safe frontend code.
*   **Tailwind CSS:** For styling the user interface.
*   **Python:** For the machine learning model and backend API.
*   **FastAPI:** A modern, high-performance web framework for building the Python API.
*   **Genkit:** An open-source framework used for building AI-powered features.
*   **JSON:** As a lightweight format for the restaurant dataset.

#### **4.3 Hardware Requirements**
*   **Development Machine:**
    *   Processor: Intel Core i5 or equivalent
    *   RAM: 8 GB or more
    *   Storage: 500 MB of free disk space
*   **Server (for deployment):**
    *   A standard cloud virtual machine or serverless platform with at least 1 vCPU and 1 GB RAM.

---

### **CHAPTER 5: DESIGN**

#### **5.1 System Architecture**
The application follows a client-server architecture.
*   **Client (Frontend):** A Next.js single-page application that runs in the user's browser. It is responsible for rendering the UI, capturing user input, and displaying the final recommendations.
*   **Server (Backend):** A Python service built with FastAPI. It exposes a single API endpoint that accepts user preferences. It houses the core recommendation engine, processes the request, and returns the recommendation data.

![System Architecture Diagram](https://i.imgur.com/8aL4oH6.png)
*Figure 5.1: A diagram representing the client-server architecture, showing the flow of data from the User Interface to the Backend API and the ML Model.*

#### **5.2 Module Description**
*   **Module 1: User Interface Module:** This is the Next.js application. It includes all the UI components, such as the recommendation wizard, input forms (for mood, occasion, etc.), and the cards used to display results.
*   **Module 2: Data Collection & Pre-processing:** This involves the creation and maintenance of the `restaurants.json` file. Each entry in this file represents a restaurant and contains not only basic data (name, address) but also pre-assigned scores for different moods and occasions.
*   **Module 3: Recommendation Engine Module:** This is the core logic within the Python backend. It contains the scoring algorithm that calculates the suitability of each restaurant based on user input. It uses TF-IDF for text similarity on restaurant features.
*   **Module 4: API Module:** The FastAPI layer that acts as the bridge between the frontend and the recommendation engine. It defines the request and response models and handles the HTTP communication.

#### **5.3 UML DIAGRAMS (Textual Description)**

##### **5.3.1 Use Case Diagram for Mood Munchies**
*   **Actor:** User
*   **Use Cases:**
    *   `Input Preferences`: The user selects their mood, occasion, cuisine, etc.
    *   `Submit Request`: The user clicks a button to get recommendations.
    *   `View Recommendations`: The system displays a list of recommended restaurants.
    *   `View Restaurant Details`: The user can see more information about a specific recommendation.

##### **5.3.2 Sequence Diagram for Recommendation Generation**
1.  **User** interacts with the **Browser (UI)** to input preferences and clicks "Get Recommendations".
2.  **Browser** sends an HTTP POST request with the user's preferences to the **FastAPI Backend**.
3.  **FastAPI Backend** receives the request and calls the `get_recommendations` function in the **Recommendation Engine**.
4.  The **Recommendation Engine** reads the restaurant data from the **JSON Database**.
5.  The **Engine** iterates through each restaurant, calculating a score using its internal algorithms (mood match, occasion match, etc.).
6.  The **Engine** returns a sorted list of the top recommendations to the **FastAPI Backend**.
7.  The **FastAPI Backend** formats the list as a JSON response and sends it back to the **Browser**.
8.  The **Browser** receives the data and dynamically renders the recommendation cards for the **User**.

##### **5.3.3 Activity Diagram of Recommendation Process**
1.  Starts at **Open Application**.
2.  User is presented with the **Input Form**.
3.  User **Selects Mood, Occasion, and Cuisine**.
4.  User **Submits Form**.
5.  System **Processes Input** and **Calculates Scores** for all restaurants.
6.  A **Decision** node checks if any restaurants match.
    *   If **Yes**, the system **Ranks Restaurants** and **Displays Top 3**.
    *   If **No**, the system **Displays a "No Results" Message**.
7.  The flow ends.

---

### **CHAPTER 6: IMPLEMENTATION**

#### **6.1 Algorithms**
The recommendation system is powered by a custom weighted scoring algorithm. Each restaurant is rated on a scale, and the final score is a sum of the following components:

*   **Mood Matching (30% weight):** Each restaurant has pre-defined compatibility scores for various moods (e.g., happy, sad, stressed). The user's selected mood is matched against these scores.
*   **Occasion Matching (30% weight):** Similarly, restaurants are scored for their suitability for different occasions (e.g., casual meal, date night, celebration).
*   **Time Matching (10% weight):** Restaurants are checked for their appropriateness for the selected time of day (e.g., breakfast, lunch, dinner).
*   **Cuisine Matching (10% weight):** A high score is given for an exact cuisine match. A partial score is given if the user selects "any".
*   **Content Similarity (10% weight):** TF-IDF (Term Frequency-Inverse Document Frequency) cosine similarity is used to compare the descriptive features of a restaurant with the user's preferences.
*   **Additional Notes (10% weight):** User-provided keywords (e.g., "spicy", "quiet") are matched against restaurant tags to refine the score.

#### **6.1.5 Implementation Procedure**
The project was implemented in the following phases:
1.  **Project Setup:** Initialized a Next.js project for the frontend and a Python environment for the backend.
2.  **Dataset Curation:** Created the `restaurants.json` file, defining the structure and manually assigning scores for mood and occasion to each restaurant entry.
3.  **Backend Development:**
    *   Implemented the recommendation engine in Python, focusing on the scoring algorithm.
    *   Developed the FastAPI server to expose the engine through a `/recommend` endpoint.
4.  **Frontend Development:**
    *   Built the UI components using React and TypeScript.
    *   Designed the recommendation wizard to capture all necessary user inputs.
    *   Styled the entire application using Tailwind CSS for a modern and responsive look.
5.  **Integration:**
    *   Connected the frontend to the backend API.
    *   Implemented the logic to fetch recommendations and display them dynamically on the page.

---

### **CHAPTER 7: CODING**

#### **7.1 Coding and Explanation**
The codebase is logically divided into two main parts: `src` for the frontend and `python_ml` for the backend.

*   **`src/app/page.tsx`**: This is the main entry point of the web application. It contains the primary UI component, `RecommendationWizard`, which manages the state for user inputs and triggers the API call.
*   **`src/app/components/recommendation-card.tsx`**: A React component responsible for displaying a single restaurant recommendation, neatly formatting its details.
*   **`python_ml/api/main.py`**: This file sets up the FastAPI server and defines the `/recommend` endpoint which accepts user preferences and returns a list of recommendations.
*   **`python_ml/ml_engine/recommendation_engine.py`**: This is the heart of the backend. It contains the core `get_recommendations` function, which implements the entire scoring and ranking algorithm described in Chapter 6.

#### **7.2 Dataset Details**
The dataset is stored in `python_ml/data/restaurants.json`. It is a JSON array where each object represents a restaurant with the following key fields:
*   `name`: The restaurant's name.
*   `cuisine`: The primary cuisine type.
*   `features`: A text description of the restaurant.
*   `address`, `contact`: Location and contact details.
*   `mood_scores`: An object with scores for moods like `happy`, `sad`, etc.
*   `occasion_scores`: An object with scores for occasions like `date_night`, `family_dinner`, etc.

---

### **CHAPTER 8: TESTING**

#### **8.1 Testing Introduction**
Testing was a crucial phase to ensure the application is robust, reliable, and provides a good user experience. The testing strategy included unit tests for core logic, integration tests for component communication, and UI tests for the user interface.

##### **8.1.1 Unit Testing**
Unit tests were focused on isolating and verifying the smallest parts of the application. For the backend, this meant writing tests for the `recommendation_engine.py` functions to ensure the scoring logic was correct for a given input.

##### **8.1.2 Integration Testing**
Integration tests were performed to verify the communication between the frontend and backend. A key test involved making a call from the Next.js app to the FastAPI backend and asserting that the response was correctly formatted and contained the expected data structure.

##### **8.1.3 User Interface (UI) Testing**
UI testing involved manually interacting with the web application to check for visual consistency and usability. This included testing on different browsers and screen sizes to ensure responsiveness and checking that all interactive elements like buttons and dropdowns behaved as expected.

#### **8.2 Test Cases**

| Test ID | Type        | Description                                                                                             | Expected Result                                                                |
|---------|-------------|---------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| UT-01   | Unit        | Test the recommendation engine with "Happy" mood and "Celebration" occasion.                              | The top-ranked restaurant should have high scores for both `happy` and `celebration`. |
| UT-02   | Unit        | Test the engine with an unknown cuisine type.                                                           | The engine should gracefully handle the input and rely on other factors.       |
| IT-01   | Integration | Make a POST request from the frontend to the `/recommend` endpoint.                                     | A `200 OK` status code is returned with a valid JSON body of recommendations.  |
| UI-01   | UI          | Select options from all dropdowns and click "Get Recommendations".                                      | Recommendation cards appear on the screen without any layout issues.           |
| UI-02   | UI          | View the application on a mobile device screen size.                                                    | The layout should adapt to the smaller screen, and all text should be readable. |

---

### **CHAPTER 9: RESULT**

The project successfully resulted in a fully functional prototype of the "Mood Munchies" application. The final product is a web application that effectively generates personalized restaurant recommendations based on the user's specified mood, occasion, and other preferences. The user interface is clean, intuitive, and responsive, providing a seamless experience from input to result. The backend recommendation engine accurately processes user requests and returns relevant and diverse suggestions, fulfilling the core objective of the project. The final result demonstrates a successful proof-of-concept for the viability of incorporating emotional and contextual data into recommendation systems.

---

### **CHAPTER 10: TIMELINE OF THE PROJECT**

| Phase                      | Week 1-2 | Week 3-4 | Week 5-6 | Week 7-8 | Week 9-10 | Week 11-12 |
|----------------------------|:--------:|:--------:|:--------:|:--------:|:---------:|:----------:|
| **Requirement Analysis**   |   ████   |          |          |          |           |            |
| **System Design**          |          |   ████   |          |          |           |            |
| **Dataset Curation**       |          |   ████   |          |          |           |            |
| **Backend Development**    |          |          |   ████   |   ████   |           |            |
| **Frontend Development**   |          |          |          |   ████   |   ████    |            |
| **Integration & Testing**  |          |          |          |          |           |    ████    |
| **Final Report**           |          |          |          |          |           |    ████    |

---

### **CHAPTER 11: CONCLUSION**

This project successfully achieved its goal of creating a personalized, mood-based restaurant recommendation system. "Mood Munchies" stands as a testament to the potential of integrating machine learning with a user-centric design to solve everyday problems in a more nuanced way. By moving beyond traditional filtering methods, the application provides a more engaging and emotionally intelligent way for users to discover dining experiences that truly match their needs. The project demonstrates a strong understanding of full-stack development, machine learning principles, and user interface design.

---

### **CHAPTER 12: FUTURE ENHANCEMENTS**

1.  **Real-Time Context and Location:** Integrate with device GPS to automatically filter by nearby restaurants and provide real-time suggestions.
2.  **User Accounts and Feedback:** Allow users to create accounts, save their favorite restaurants, and provide feedback on recommendations, which can be used to further personalize the model.
3.  **Collaborative Filtering:** As a user base grows, implement collaborative filtering to recommend places that users with similar tastes have enjoyed.
4.  **Expanded and Dynamic Dataset:** Integrate with a third-party API (like Google Places) to access a vast and constantly updated database of restaurants.
5.  **Multimodal Emotion Recognition:** Implement voice analysis to automatically detect the user's mood, as originally envisioned in the project's conceptual phase.
6.  **Cloud Deployment and Scalability:** Deploy the application on a scalable cloud infrastructure to ensure high availability and performance for a larger audience.

---

### **CHAPTER 13: PROJECT OUTCOME-POS/PSOS MAPPING**

This project successfully demonstrates the achievement of several Program Outcomes (POs) and Program Specific Outcomes (PSOs) for a computer science and engineering curriculum.
*   **Engineering Knowledge:** Applied knowledge of mathematics, science, and engineering fundamentals to the problem of recommendation systems.
*   **Problem Analysis:** Identified, formulated, and analyzed a complex engineering problem to arrive at a substantiated conclusion.
*   **Design/Development of Solutions:** Designed and developed a software solution that meets specified needs with respect to user experience and functionality.
*   **Modern Tool Usage:** Utilized modern IT tools including Next.js, Python, FastAPI, and Git for the development and management of the project.
*   **The Engineer and Society:** Created a solution that addresses a societal need by improving user well-being and decision-making.

---

### **CHAPTER 14: REFERENCES**

This section would include a bibliography of all research papers, articles, and official documentation consulted during the project.
*   Official documentation for Next.js.
*   Official documentation for Python, Pandas, and Scikit-learn.
*   Official documentation for FastAPI.
*   Academic papers on content-based and collaborative filtering recommendation systems.
*   Articles on UI/UX design principles for web applications.
