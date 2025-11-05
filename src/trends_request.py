from pytrends.request import TrendReq
from pytrends import dailydata
import pandas as pd
from datetime import date, timedelta
import time

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Keyword and date range
keyword = "Golden State Warriors"
start_date = date(2020, 10, 25)
end_date = date.today()

# Function to split date range into 3-month intervals
def generate_intervals(start, end, delta_days=90):
    intervals = []
    current_start = start
    while current_start < end:
        current_end = current_start + timedelta(days=delta_days)
        if current_end > end:
            current_end = end
        intervals.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)  # avoid overlapping last day
    return intervals

# Generate intervals
intervals = generate_intervals(start_date, end_date)

# Storage
all_trends = pd.DataFrame()

# Loop through intervals and fetch data
for start, stop in intervals:
    timeframe = f"{start} {stop}"
    print(f"Fetching: {timeframe}")
    pytrends.build_payload([keyword], timeframe=timeframe, geo='US')
    df = pytrends.interest_over_time()
    if not df.empty:
        df = df.reset_index()[['date', keyword]]  # drop isPartial column
        all_trends = pd.concat([all_trends, df], ignore_index=True)
    time.sleep(1)  # polite delay to avoid rate limiting

# Remove duplicates (overlaps) and sort
all_trends = all_trends.drop_duplicates(subset='date').sort_values('date')

# Save to CSV
all_trends.to_csv("warriors_trends_2020-2025.csv", index=False)
print(f"✅ Collected {len(all_trends)} daily data points.")
