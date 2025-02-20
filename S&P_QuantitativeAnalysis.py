import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pandas_market_calendars as mcal
import time

# Define the first market days in September for the past 20 years
september_dates = [
    "2023-09-01", "2022-09-01", "2021-09-01", "2020-09-01",
    "2019-09-03", "2018-09-04", "2017-09-01", "2016-09-01",
    "2015-09-01", "2014-09-02", "2013-09-03", "2012-09-04",
    "2011-09-01", "2010-09-01", "2009-09-01", "2008-09-02",
    "2007-09-04", "2006-09-01", "2005-09-01"
]

# Add the last 10 Mondays
today = datetime.today()
mondays = []
delta = timedelta(days=1)

while len(mondays) < 10:
    if today.weekday() == 0:  # Monday is weekday 0
        mondays.append(today.strftime("%Y-%m-%d"))
    today -= delta

# Set up the market calendar for NYSE
nyse = mcal.get_calendar('NYSE')

# Fetch the market open and close times for September dates
september_market_dates = []
for date in september_dates:
    dt = datetime.strptime(date, "%Y-%m-%d")
    if len(nyse.valid_days(start_date=dt, end_date=dt)) > 0:  # Properly checking for valid market day
        september_market_dates.append(dt.strftime("%Y-%m-%d"))

# Fetch historical S&P 500 data, with retries in case of failures
start_date = (datetime.today() - timedelta(days=365 * 20)).strftime("%Y-%m-%d")  # Ensuring 20 years of data

attempts = 3
for attempt in range(attempts):
    try:
        sp500 = yf.download("^GSPC", start=start_date, end=datetime.today().strftime("%Y-%m-%d"), auto_adjust=False)
        if not sp500.empty:
            break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(2)

# Check if data was retrieved successfully
if sp500.empty:
    print("Failed to retrieve S&P 500 data. Please check your internet connection or try again later.")
    exit()

# Print the available data dates to check the dataset
print("Available S&P 500 dates:")
print(sp500.index)

# Ensure the correct column is used for daily returns
if 'Adj Close' in sp500.columns:
    sp500['Daily Return'] = sp500['Adj Close'].pct_change()
else:
    sp500['Daily Return'] = sp500['Close'].pct_change()

# Calculate returns for September dates
september_returns = []
september_missing_dates = []

for date in september_market_dates:
    if date in sp500.index:
        daily_return = sp500.loc[date, 'Daily Return']
        if isinstance(daily_return, pd.Series):
            daily_return = daily_return.iloc[0]  # Ensure it's a single value
        september_returns.append((date, daily_return))
    else:
        september_missing_dates.append(date)

# Display results for September dates
if september_returns:
    print("\nS&P 500 movement on September dates:")
    for date, movement in september_returns:
        print(f"{date}: {movement:.4%}")
else:
    print("\nNo valid September dates found.")

if september_missing_dates:
    print("\nNo data available for September dates:")
    for date in september_missing_dates:
        print(f"{date}")

# Calculate returns for Monday dates
monday_returns = []
monday_missing_dates = []

for date in mondays:
    if date in sp500.index:
        daily_return = sp500.loc[date, 'Daily Return']
        if isinstance(daily_return, pd.Series):
            daily_return = daily_return.iloc[0]
        monday_returns.append((date, daily_return))
    else:
        monday_missing_dates.append(date)

# Display results for Monday dates
if monday_returns:
    print("\nS&P 500 movement on Monday dates:")
    for date, movement in monday_returns:
        print(f"{date}: {movement:.4%}")
else:
    print("\nNo valid Monday dates found.")

if monday_missing_dates:
    print("\nNo data available for Monday dates:")
    for date in monday_missing_dates:
        print(f"{date}")

# Calculate average return for September dates
if september_returns:
    september_avg_return = sum([movement for _, movement in september_returns]) / len(september_returns)
    print(f"\nAverage S&P 500 movement on September dates: {september_avg_return:.4%}")
else:
    print("\nNo valid September data for average calculation.")

# Calculate average return for Monday dates
if monday_returns:
    monday_avg_return = sum([movement for _, movement in monday_returns]) / len(monday_returns)
    print(f"\nAverage S&P 500 movement on Monday dates: {monday_avg_return:.4%}")
else:
    print("\nNo valid Monday data for average calculation.")

# Calculate total average return for both September and Monday dates
total_returns = september_returns + monday_returns
if total_returns:
    total_avg_return = sum([movement for _, movement in total_returns]) / len(total_returns)
    print(f"\nTotal average S&P 500 movement across both September and Monday dates: {total_avg_return:.4%}")
else:
    print("\nNo valid data for total average calculation.")
