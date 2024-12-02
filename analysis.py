import os
import json
from collections import defaultdict

### ANALYSIS ###

# Function to calculate the average review scores for each cuisine in each state.
def calculate_average_review_scores(folder_path):
    average_scores = {}

    # Iterate through each file in the review_scores folder.
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # Read the JSON data from the file.
            with open(file_path, 'r', encoding='utf-8') as infile:
                review_scores = json.load(infile)
                
                # Calculate the average of the values.
                if review_scores:
                    average_score = sum(review_scores.values()) / len(review_scores)
                else:
                    average_score = 0
                
                # Remove the '.json' from the end of the file name.
                filename = filename[:-5]

                # Store the filename and the average score in the dictionary
                average_scores[filename] = average_score

    return average_scores

# Define the path to the review_scores folder.
review_scores_folder = os.path.join(os.getcwd(), "review_scores")

# Calculate the average review scores.
average_review_scores = calculate_average_review_scores(review_scores_folder)

def get_top_5_states_by_cuisine(average_review_scores):
    cuisine_scores = defaultdict(list)

    # Populate the cuisine_scores dictionary
    for key, average_score in average_review_scores.items():
        state_abbreviation, cuisine = key.split('_')
        cuisine_scores[cuisine].append((state_abbreviation, average_score))

    top_5_states_by_cuisine = {}

    # Find the top 5 states for each cuisine.
    for cuisine, scores in cuisine_scores.items():
        # Sort the states by their average review scores in descending order.
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        # Get the top 5 states.
        top_5_states = sorted_scores[:5]
        top_5_states_by_cuisine[cuisine] = top_5_states

    return top_5_states_by_cuisine

# Calculate the top 5 states for each cuisine.
top_5_states_by_cuisine = get_top_5_states_by_cuisine(average_review_scores)

# Print the resulting dictionary.
for cuisine, top_5_states in top_5_states_by_cuisine.items():
    print(f"Top 5 states for {cuisine}: {top_5_states}\n")

### VISUALIZATION ###

import folium
from folium.plugins import MarkerCluster

# Dictionary mapping state abbreviations to their corresponding cities and coordinates.
state_city_coordinates = {
    "AZ": ["Phoenix", (33.4484, -112.0740)],
    "CA": ["Los Angeles", (34.0522, -118.2437)],
    "DE": ["Wilmington", (39.7391, -75.5398)],
    "FL": ["Miami", (25.7617, -80.1918)],
    "ID": ["Boise", (43.6150, -116.2023)],
    "IL": ["Urbana-Champaign", (40.1106, -88.2073)],
    "IN": ["Indianapolis", (39.7684, -86.1581)],
    "LA": ["New Orleans", (29.9511, -90.0715)],
    "MO": ["St. Louis", (38.6270, -90.1994)],
    "NV": ["Las Vegas", (36.1699, -115.1398)],
    "NJ": ["Jersey City", (40.7178, -74.0431)],
    "PA": ["Pittsburgh", (40.4406, -79.9959)],
    "TN": ["Nashville", (36.1627, -86.7816)],
    "AB": ["Calgary", (51.0447, -114.0719)]
}

def create_map(top_5_states_by_cuisine):
    # Create a map centered in North America.
    m = folium.Map(location=[54.5260, -105.2551], zoom_start=3)

    # Create a MarkerCluster instance.
    marker_cluster = MarkerCluster().add_to(m)

    # List to store the coordinates of the markers.
    marker_coordinates = []

    for cuisine, top_states in top_5_states_by_cuisine.items():
        # Get the coordinates for the top city for each cuisine.
        top_state = top_states[0][0]
        top_city = state_city_coordinates[top_state][0]
        coordinates = state_city_coordinates[top_state][1]

        # Add the coordinates to the list.
        marker_coordinates.append(coordinates)
        
        # Add a marker for the top city.
        folium.Marker(
            location=coordinates,
            popup=f"{cuisine}: {top_city}",
            tooltip=f"{cuisine} ({top_city})"
        ).add_to(marker_cluster)
    
    # Adjust the map to fit all the marker coordinates.
    m.fit_bounds(marker_coordinates)

    return m

# Generate the map.
map_visualization = create_map(top_5_states_by_cuisine)

# Save the map to an HTML file.
map_visualization.save("top_cities_by_cuisine.html")