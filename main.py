import pandas as pd
import json
import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import plotly.express as px
from collections import defaultdict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

### EXPLORATORY DATA ANALYSIS ###

# Dictionary of state abbreviations.
state_abbreviations = {
    "AL": 0, "AK": 0, "AZ": 0, "AR": 0, "CA": 0,
    "CO": 0, "CT": 0, "DE": 0, "FL": 0, "GA": 0,
    "HI": 0, "ID": 0, "IL": 0, "IN": 0, "IA": 0,
    "KS": 0, "KY": 0, "LA": 0, "ME": 0, "MD": 0,
    "MA": 0, "MI": 0, "MN": 0, "MS": 0, "MO": 0,
    "MT": 0, "NE": 0, "NV": 0, "NH": 0, "NJ": 0,
    "NM": 0, "NY": 0, "NC": 0, "ND": 0, "OH": 0,
    "OK": 0, "OR": 0, "PA": 0, "RI": 0, "SC": 0,
    "SD": 0, "TN": 0, "TX": 0, "UT": 0, "VT": 0,
    "VA": 0, "WA": 0, "WV": 0, "WI": 0, "WY": 0
}

# Dictionary of identifying the main states represented in the dataset.
main_states = {}

# List of cuisines based on which cuisines are highly represented* in the Yelp dataset.
# *>100 restaurants in the dataset.
cuisine_list = [
    "American (Traditional)", "American (New)", "Mexican", "Italian", "Chinese",
    "Japanese", "Mediterranean", "Thai", "Cajun/Creole", "Latin American", "Greek",
    "Indian", "Vietnamese", "Caribbean", "Middle Eastern", "French", "Korean",
    "Spanish", "Pakistani", "Irish", "Hawaiian", "German", "African", "Filipino"
]

# Initialize dictionaries for each state with cuisine types as keys and empty lists as values.
arizona_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                       "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                       "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                       "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                       "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

california_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                          "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                          "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                          "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                          "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

delaware_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                        "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                        "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                        "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                        "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

florida_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                       "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                       "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                       "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                       "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

idaho_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                     "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                     "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                     "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                     "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

illinois_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                        "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                        "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                        "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                        "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

indiana_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                       "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                       "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                       "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                       "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

louisiana_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                         "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                         "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                         "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                         "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

missouri_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                        "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                        "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                        "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                        "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

nevada_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                      "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                      "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                      "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                      "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

new_jersey_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                          "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                          "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                          "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                          "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

pennsylvania_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                            "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                            "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                            "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                            "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

tennessee_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                         "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                         "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                         "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                         "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

alberta_restaurants = {"American (Traditional)": [], "American (New)": [], "Mexican": [], "Italian": [],
                       "Chinese": [], "Japanese": [], "Mediterranean": [], "Thai": [], "Cajun/Creole": [],
                       "Latin American": [], "Greek": [], "Indian": [], "Vietnamese": [], "Caribbean": [],
                       "Middle Eastern": [], "French": [], "Korean": [], "Spanish": [], "Pakistani": [],
                       "Irish": [], "Hawaiian": [], "German": [], "African": [], "Filipino": []}

# Load and sort the restaurant records based on state and cuisine.
with open("yelp_academic_dataset_business.json", 'r', encoding = "utf-8") as f:
    for line in f:
        record = json.loads(line)

        # Check if the record is a restaurant.
        if 'categories' in record and record['categories'] is not None and 'Restaurants' in record['categories']:
            state = record['state']

            # Convert categories to a list by splitting the string (categories are comma-separated).
            categories = record['categories'].split(", ") if 'categories' in record else []

            # Categorize the restaurant by state and cuisine.
            if state == "AZ":  # Arizona
                for cuisine in categories:
                    if cuisine in arizona_restaurants:
                        arizona_restaurants[cuisine].append(record['business_id'])
            elif state == "CA":  # California.
                for cuisine in categories:
                    if cuisine in california_restaurants:
                        california_restaurants[cuisine].append(record['business_id'])
            elif state == "DE":  # Delaware.
                for cuisine in categories:
                    if cuisine in delaware_restaurants:
                        delaware_restaurants[cuisine].append(record['business_id'])
            elif state == "FL":  # Florida.
                for cuisine in categories:
                    if cuisine in florida_restaurants:
                        florida_restaurants[cuisine].append(record['business_id'])
            elif state == "ID":  # Idaho.
                for cuisine in categories:
                    if cuisine in idaho_restaurants:
                        idaho_restaurants[cuisine].append(record['business_id'])
            elif state == "IL":  # Illinois.
                for cuisine in categories:
                    if cuisine in illinois_restaurants:
                        illinois_restaurants[cuisine].append(record['business_id'])
            elif state == "IN":  # Indiana.
                for cuisine in categories:
                    if cuisine in indiana_restaurants:
                        indiana_restaurants[cuisine].append(record['business_id'])
            elif state == "LA":  # Louisiana.
                for cuisine in categories:
                    if cuisine in louisiana_restaurants:
                        louisiana_restaurants[cuisine].append(record['business_id'])
            elif state == "MO":  # Missouri.
                for cuisine in categories:
                    if cuisine in missouri_restaurants:
                        missouri_restaurants[cuisine].append(record['business_id'])
            elif state == "NV":  # Nevada.
                for cuisine in categories:
                    if cuisine in nevada_restaurants:
                        nevada_restaurants[cuisine].append(record['business_id'])
            elif state == "NJ":  # New Jersey.
                for cuisine in categories:
                    if cuisine in new_jersey_restaurants:
                        new_jersey_restaurants[cuisine].append(record['business_id'])
            elif state == "PA":  # Pennsylvania.
                for cuisine in categories:
                    if cuisine in pennsylvania_restaurants:
                        pennsylvania_restaurants[cuisine].append(record['business_id'])
            elif state == "TN":  # Tennessee.
                for cuisine in categories:
                    if cuisine in tennessee_restaurants:
                        tennessee_restaurants[cuisine].append(record['business_id'])
            elif state == "AB":  # Alberta.
                for cuisine in categories:
                    if cuisine in alberta_restaurants:
                        alberta_restaurants[cuisine].append(record['business_id'])

### SEMANTIC ANALYSIS ###

# Download stopwords and WordNet for lemmatization.
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize stopwords and lemmatizer.
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Initialize the VADER SentimentIntensityAnalyzer.
analyzer = SentimentIntensityAnalyzer()

# Function to preprocess the review.
def preprocess_review(review):
    # Convert to lowercase.
    review = review.lower()
    
    # Remove URLs.
    review = re.sub(r'http\S+|www\S+|https\S+', '', review, flags=re.MULTILINE)
    
    # Remove punctuation and special characters.
    review = review.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text.
    tokens = review.split()
    
    # Remove stopwords and lemmatize.
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    # Join tokens back into a single string.
    processed_review = ' '.join(tokens)
    
    return processed_review

# Function to convert VADER compound score to a scale of 1-10.
def sentiment_to_score(compound_score):
    return round((compound_score + 1) * 5)  # Convert range (-1, 1) to (1, 10).

# Function to combine sentiment score and reviewer rating.
def combine_scores(sentiment_score, rating):
    if rating is not None:
        rating_scaled = rating * 2  # Scale rating (1-5) to match sentiment score (1-10).
        # Weighted average: giving 50% weight to each.
        final_score = round((0.5 * sentiment_score) + (0.5 * rating_scaled))
    else:
        final_score = sentiment_score  # If no rating is provided, use sentiment score only.
    return final_score

def generate_review_scores(cuisine, state_abbreviation, state_restaurants):
    if cuisine == "Cajun/Creole":
        cuisine = "Cajun"

    # Get the restaurant IDs for the specified cuisine.
    if cuisine == "Cajun":
        restaurant_ids = state_restaurants["Cajun/Creole"]
    else:
        restaurant_ids = state_restaurants[cuisine]

    # Dictionary to store review scores.
    review_scores = {}

    # Open the review dataset and filter reviews for the specified cuisine.
    with open("yelp_academic_dataset_review.json", 'r', encoding = "utf-8") as review_file:
        for line in review_file:
            review_record = json.loads(line)
            
            # Check if the review belongs to a restaurant of the specified cuisine:
            if review_record['business_id'] in restaurant_ids:
                # Load the review details.
                review = review_record['text']
                
                # Preprocess the review.
                processed_review = preprocess_review(review)

                # Perform sentiment analysis using VADER.
                sentiment_scores = analyzer.polarity_scores(processed_review)
                compound_score = sentiment_scores['compound']
                
                # Convert the compound score to a 1-10 scale.
                sentiment_score = sentiment_to_score(compound_score)
                
                # Get the reviewer's rating if available.
                rating = review_record['stars']

                # Combine the sentiment score and rating.
                final_score = combine_scores(sentiment_score, rating)
                
                # Store the review score in the dictionary.
                review_id = review_record['review_id']
                review_scores[review_id] = final_score

    # Save the review scores dictionary to a JSON file for future use
    json_path = os.path.join(os.getcwd(), "review_scores", f'{state_abbreviation}_{cuisine}.json')
    with open(json_path, 'w', encoding='utf-8') as outfile:
        json.dump(review_scores, outfile, ensure_ascii=False, indent=4)

    print(f"Review scores for {cuisine} restaurants in {state_abbreviation} have been successfully saved.")

# Generate review scores for each cuisine in each state.
for cuisine in cuisine_list:
    generate_review_scores(cuisine, "AZ", arizona_restaurants)
    generate_review_scores(cuisine, "CA", california_restaurants)
    generate_review_scores(cuisine, "DE", delaware_restaurants)
    generate_review_scores(cuisine, "FL", florida_restaurants)
    generate_review_scores(cuisine, "ID", idaho_restaurants)
    generate_review_scores(cuisine, "IL", illinois_restaurants)
    generate_review_scores(cuisine, "IN", indiana_restaurants)
    generate_review_scores(cuisine, "LA", louisiana_restaurants)
    generate_review_scores(cuisine, "MO", missouri_restaurants)
    generate_review_scores(cuisine, "NV", nevada_restaurants)
    generate_review_scores(cuisine, "NJ", new_jersey_restaurants)
    generate_review_scores(cuisine, "PA", pennsylvania_restaurants)
    generate_review_scores(cuisine, "TN", tennessee_restaurants)
    generate_review_scores(cuisine, "AB", alberta_restaurants)