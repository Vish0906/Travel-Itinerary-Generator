# Travel Assistant Chatbot

## Travel Itinerary Generator with Mistral 7b in tandem with Geonames Library

This app generates a detailed travel itinerary based on user preferences using a Python FastAPI backend and the `mistralai/Mistral-7B-Instruct-v0.3` model from Groq.

### Inputs from User:
- **Destination** (e.g., Paris, Tokyo)
- **Start Date** (e.g., 2025-06-01)
- **End Date** (e.g., 2025-06-07)
- **Budget** (optional, e.g., 1000 USD)
- **Preferences** (e.g., adventure, relaxation, food, culture)
- **Number of Travelers** (optional, e.g., 2 adults)
- **Additional Notes** (e.g., want to try local cuisine, prefer public transport)

### Output:
- Day-by-day itinerary including:
  - Morning, afternoon, and evening plans
  - Local attractions and suggested activities
  - Dining recommendations
  - Transport details
- Estimated budget breakdown
- Travel tips or local facts

### Usage of `geonames()`:
The `geonames()` library is used to fetch location-specific data such as:
- Nearby places of interest
- Geographic details (latitude, longitude, timezone)
- Local administrative details (country, state, city)
This helps generate accurate and realistic plans personalized to the user's destination.
