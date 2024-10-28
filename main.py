import pandas as pd
import json

us_states = set(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
                 "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                 "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])


data = []
with open('yelp_academic_dataset_business.json', 'r') as f:  # Replace with your file path
    for line in f:
        record = json.loads(line)
        if record.get("state") in us_states:
            data.append(record)


df_us_restaurants = pd.DataFrame(data)


print(df_us_restaurants)



