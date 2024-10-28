import pandas as pd
import json
from collections import Counter
import plotly.express as px
from collections import defaultdict
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

# Sum all values in the dictionary
total_sum = sum(state_abbreviations.values())

with open("yelp_academic_dataset_business.json", 'r') as f:
    for line in f:
        record = json.loads(line)
        if record.get("state") in state_abbreviations.keys():
            state_abbreviations[record.get("state")] += 1
        else:
            state_abbreviations[record.get("state")] = 1

main_states = {}
for key, value in state_abbreviations.items():
    if int(value) > 10:
        main_states[key] = value
print(main_states)
print(len(main_states))
# List of cuisines to filter
cuisine_list = [
    "American (Traditional)", "American (New)", "Mexican", "Italian", "Chinese", "Japanese",
    "Mediterranean", "Thai", "Cajun/Creole", "Latin American", "Greek", "Indian", "Vietnamese",
    "Caribbean", "Middle Eastern", "French", "Korean", "Spanish", "Pakistani", "Irish", "Hawaiian",
    "German", "African", "Filipino"
]

# Step 2: Load and filter the restaurant data based on categories and states
restaurant_data = []  # Initialize an empty list to store filtered restaurant records

with open("yelp_academic_dataset_business.json", 'r') as f:
    for line in f:
        record = json.loads(line)
        # Filter for restaurant entries, ensuring categories is not None
        if 'categories' in record and record['categories'] is not None and 'Restaurants' in record['categories']:
            state = record['state']
            if state in main_states:  # Only keep restaurants in the main states
                restaurant_data.append(record)

# Step 3: Count occurrences for each (state, cuisine) combination
state_cuisine_counts = defaultdict(int)

for record in restaurant_data:
    state = record['state']
    categories = record['categories'].split(', ') if 'categories' in record else []
    for cuisine in categories:
        if cuisine in cuisine_list:
            state_cuisine_counts[(state, cuisine)] += 1

# Step 4: Print the counts in "State, Cuisine, Count" format
print("State, Cuisine, Count")
for (state, cuisine), count in state_cuisine_counts.items():
    print(f"{state}, {cuisine}, {count}")

top_states_dict = {}
for (state, cuisine), count in state_cuisine_counts.items():
    if cuisine not in top_states_dict:
        top_states_dict[cuisine] = []
    top_states_dict[cuisine].append((state, count))

top_cuisine_counts = {}
for cuisine, top_counts in top_states_dict.items():
    # Sort the counts by the second element (count) in descending order
    sorted_counts = sorted(top_counts, key = lambda x:x[1], reverse=True)
    # Keep only the top 5
    top_cuisine_counts[cuisine] = sorted_counts[:5]

# Display the results
for cuisine, top_counts in top_cuisine_counts.items():
    print(f"Cuisine: {cuisine}")
    for state, count in top_counts:
        print(f"  State: {state}, Count: {count}")

german_counts = {key: count for key, count in state_cuisine_counts.items() if key[1] == "German"}

plot_data = [{"State": state, "Cuisine": cuisine, "Count": count}
             for (state, cuisine), count in german_counts.items()]


df_plot = pd.DataFrame(plot_data)
top_states = df_plot.nlargest(5, 'Count')


fig = px.bar(top_states, x='State', y='Count',
             title='Top 5 States for Italian Cuisine',
             labels={'Count': 'Number of Restaurants', 'State': 'State'},
             color='Count',  
             color_continuous_scale='Viridis')  


fig.show()
