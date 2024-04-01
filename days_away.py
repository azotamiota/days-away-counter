import csv
from datetime import datetime, date, timedelta

# Calculate the date 6 years ago from today
today = date.today()
six_years_ago = date(today.year - 6, today.month, today.day)
print(f"Six years ago from today ({today}) was: {six_years_ago}")

# Define a function to validate date input
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    except ValueError:
        return None

# Define a function to validate date range
def validate_date_range(date_range_str):
    dates = date_range_str.split("-")
    if len(dates) != 2:
        return None
    start_date = validate_date(dates[0])
    end_date = validate_date(dates[1])
    if start_date is None or end_date is None or end_date <= start_date:
        return None
    return start_date, end_date

# Define a function to calculate days within date ranges
def calculate_days_in_ranges(date_ranges, target_date):
    days = 0
    for start_date, end_date in date_ranges:
        range_start = max(start_date, target_date - timedelta(days=365*6))
        range_end = min(end_date, target_date)
        days += (range_end - range_start).days + 1
    return days

# Main loop
data = []
while True:
    mode = input("Enter 'i' to provide a date range and destination, 'r' to view the summary, or 'q' to exit program: ").lower()
    if mode == "i":
        date_range_str = input("Enter a date range in the format YYYY/MM/DD-YYYY/MM/DD: ")
        date_range = validate_date_range(date_range_str)
        if date_range is None:
            print("Invalid date range. Please try again.")
            continue
        destination = input("Enter a destination: ")
        data.append({"date_range": date_range_str, "destination": destination})
        print("Data saved successfully.")
        with open("data.csv", "a", newline="") as csvfile:
            fieldnames = ["date_range", "destination"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    elif mode == "r":
        date_ranges = []
        destinations = []
        with open("data.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_range = validate_date_range(row["date_range"])
                if date_range:
                    date_ranges.append(date_range)
                    destinations.append(row["destination"])

        total_days = calculate_days_in_ranges(date_ranges, today)
        print(f"Summary for the last 6 years (from {six_years_ago} to {today}):")
        print("Date Range\tDestination\tDays")
        for date_range, destination in zip(date_ranges, destinations):
            days = calculate_days_in_ranges([date_range], today)
            print(f"{'-'.join([d.strftime('%Y/%m/%d') for d in date_range])}\t{destination}\t{days}")
        print(f"Total days: {total_days}")
    elif mode == "q":
        print("Exiting...")
        break
    else:
        print("Invalid mode. Please try again.")