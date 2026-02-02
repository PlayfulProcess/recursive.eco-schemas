#!/usr/bin/env python3
"""
Fetch Google Trends data for anti-oppressive tarot deck figures.
Uses pytrends to get real visibility metrics.
"""

import json
import time
from pytrends.request import TrendReq

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Our figures to search
figures = [
    "Jane Addams",
    "Mary Richmond social worker",
    "W.E.B. Du Bois",
    "Ida B. Wells",
    "Martin Luther King Jr",
    "Malcolm X",
    "Rosa Parks",
    "Frederick Douglass",
    "Booker T. Washington",
    "Emma Goldman",
    "Richard Henry Pratt",
    "Theodore Roosevelt",
    "Maggie Lena Walker",
    "Claudette Colvin",
    "Viola Desmond",
    "Bayard Rustin",
    "James Baldwin writer",
    "Huey Newton",
    "Henry Bibb",
    "Mary Ann Shadd Cary",
]

# Reference term for normalization (high visibility baseline)
REFERENCE = "Martin Luther King Jr"

results = {}

print("Fetching Google Trends data...")
print("=" * 50)

# Query in batches of 4 (plus reference term = 5 max)
batch_size = 4

for i in range(0, len(figures), batch_size):
    batch = figures[i:i+batch_size]

    # Skip if reference is in batch
    batch_clean = [f for f in batch if f != REFERENCE]
    if len(batch_clean) < len(batch):
        batch = batch_clean

    # Always include reference for normalization
    search_terms = batch + [REFERENCE] if REFERENCE not in batch else batch

    try:
        print(f"\nBatch {i//batch_size + 1}: {batch}")
        pytrends.build_payload(search_terms, timeframe='today 12-m', geo='US')
        data = pytrends.interest_over_time()

        if not data.empty:
            # Get average interest over the period
            for term in batch:
                if term in data.columns:
                    avg_interest = data[term].mean()
                    results[term] = {
                        "average_interest": round(avg_interest, 2),
                        "max_interest": int(data[term].max()),
                        "query": term
                    }
                    print(f"  {term}: avg={avg_interest:.1f}, max={data[term].max()}")

        # Rate limiting - be nice to Google
        time.sleep(2)

    except Exception as e:
        print(f"  Error: {e}")
        time.sleep(5)

# Add reference term result
if REFERENCE in results:
    pass
else:
    try:
        pytrends.build_payload([REFERENCE], timeframe='today 12-m', geo='US')
        data = pytrends.interest_over_time()
        if not data.empty:
            results[REFERENCE] = {
                "average_interest": round(data[REFERENCE].mean(), 2),
                "max_interest": int(data[REFERENCE].max()),
                "query": REFERENCE
            }
    except:
        pass

# Save results
output = {
    "metadata": {
        "source": "Google Trends via pytrends",
        "timeframe": "12 months",
        "geo": "US",
        "reference_term": REFERENCE,
        "collection_date": "2026-01-30"
    },
    "trends_data": results
}

output_path = "/home/user/recursive.eco-schemas/schemas/tarot/anti-opressive-major-arcana/data/google-trends-data.json"
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 50)
print(f"Results saved to: {output_path}")
print(f"Total figures with data: {len(results)}")
