from datetime import datetime
import pytz
import csv
from pathlib import Path

def get_us_timezones():
    us_timezones = [
        "US/Eastern", "US/Central", "US/Mountain", "US/Pacific", 
        "US/Alaska", "US/Hawaii", 
        "America/New_York", "America/Chicago", "America/Denver", 
        "America/Los_Angeles", "America/Anchorage", "America/Honolulu"
    ]
    return us_timezones + sorted(tz for tz in pytz.all_timezones if tz not in us_timezones)

def validate_date(date_str):
    """Validate date string format and return True if valid."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """Validate time string format and return True if valid."""
    try:
        # First check basic format
        if not time_str.count(':') == 1:
            return False
        
        hours, minutes = time_str.split(':')
        
        # Check if hours and minutes are numbers
        if not (hours.isdigit() and minutes.isdigit()):
            return False
            
        # Convert to integers
        hours = int(hours)
        minutes = int(minutes)
        
        # Check ranges
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            return False
            
        return True
    except Exception:
        return False

def get_date_input(default_date=None):
    """Get and validate date input from user."""
    while True:
        if default_date:
            print(f"Current date is {default_date.strftime('%Y-%m-%d')}")
            change = input("Would you like to change the date? (y/n): ").lower()
            if change == 'n':
                return default_date.strftime('%Y-%m-%d')
        
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        
        if not date_str:
            print("Date cannot be empty. Please try again.")
            continue
            
        if not validate_date(date_str):
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2024-03-19)")
            print("Make sure:")
            print("- Year is between 1900 and 2100")
            print("- Month is between 01 and 12")
            print("- Day is valid for the given month")
            continue
            
        return date_str

def get_time_input():
    """Get and validate time input from user."""
    while True:
        print("\nPlease enter time in 24-hour format (e.g., 13:30 for 1:30 PM, 09:15 for 9:15 AM)")
        time_str = input("Enter time (HH:MM): ").strip()
        
        if not time_str:
            print("Time cannot be empty. Please try again.")
            continue
            
        if not validate_time(time_str):
            print("Invalid time format. Please use HH:MM in 24-hour format")
            print("Make sure:")
            print("- Hours are between 00 and 23")
            print("- Minutes are between 00 and 59")
            print("- Use leading zeros (e.g., 09:05 instead of 9:5)")
            continue
            
        return time_str

def get_datetime_input(prompt, default_date=None):
    """Get and validate both date and time input."""
    while True:
        try:
            date_str = get_date_input(default_date)
            time_str = get_time_input()
            
            # Combine date and time and validate the combination
            datetime_str = f"{date_str} {time_str}"
            parsed_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # Additional validation for reasonable date range
            current_year = datetime.now().year
            if not (current_year - 2 <= parsed_datetime.year <= current_year + 2):
                print(f"Warning: Year {parsed_datetime.year} seems unusual.")
                confirm = input("Are you sure this is correct? (y/n): ").lower()
                if confirm != 'y':
                    continue
            
            return parsed_datetime
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Please try again with valid date and time.")
            continue

def display_timezone_page(timezones, page, per_page=10):
    start_idx = page * per_page
    end_idx = start_idx + per_page
    displayed_zones = timezones[start_idx:end_idx]
    
    print(f"\nTimezones (Page {page + 1}/{(len(timezones) + per_page - 1) // per_page}):")
    for i, tz in enumerate(displayed_zones, start_idx + 1):
        tz_obj = pytz.timezone(tz)
        current_time = datetime.now(tz_obj)
        dst_status = " (DST)" if current_time.tzinfo.dst(current_time) else ""
        print(f"{i}. {tz}{dst_status}")
    
    print("\nNavigation:")
    print("n - Next page")
    print("p - Previous page")
    print("s - Search")
    print("Enter number to select timezone")

def get_timezone_input(prompt):
    all_timezones = get_us_timezones()
    page = 0
    per_page = 10
    
    while True:
        display_timezone_page(all_timezones, page, per_page)
        user_input = input(f"\n{prompt}").strip().lower()
        
        if user_input == 'n':
            if (page + 1) * per_page < len(all_timezones):
                page += 1
            continue
        
        elif user_input == 'p':
            if page > 0:
                page -= 1
            continue
        
        elif user_input == 's':
            search_term = input("Enter search term: ").strip().lower()
            matching_zones = [tz for tz in all_timezones if search_term in tz.lower()]
            
            if not matching_zones:
                print("No matching timezones found.")
                continue
            
            print("\nMatching timezones:")
            for i, tz in enumerate(matching_zones, 1):
                tz_obj = pytz.timezone(tz)
                current_time = datetime.now(tz_obj)
                dst_status = " (DST)" if current_time.tzinfo.dst(current_time) else ""
                print(f"{i}. {tz}{dst_status}")
            
            choice = input("Select a number (or press Enter to return to browsing): ")
            if choice.isdigit() and 1 <= int(choice) <= len(matching_zones):
                return matching_zones[int(choice) - 1]
            continue
        
        elif user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(all_timezones):
                selected_tz = all_timezones[index]
                
                tz_obj = pytz.timezone(selected_tz)
                current_time = datetime.now(tz_obj)
                dst_status = " (Currently observing Daylight Savings Time)" if current_time.tzinfo.dst(current_time) else ""
                
                confirm = input(f"Confirm selection of {selected_tz}{dst_status}? (y/n): ")
                if confirm.lower() == 'y':
                    return selected_tz
        
        print("Invalid input. Please try again.")

def get_current_time_in_timezone(timezone_str):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz)

def main():
    print("=== Work Time Tracker ===")
    print("Automatically handles Daylight Savings Time")
    print("US Timezones shown first")
    print("Time entries use 24-hour format")
    print("=====================================")
    
    csv_file = Path("work_time.csv")
    headers = ["Date", "Start Time", "Start Timezone", "End Time", "End Timezone", "Total Hours Worked", "DST Adjustment"]
    
    if not csv_file.exists():
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    print("\n=== Work Start Information ===")
    start_dt = get_datetime_input("Enter start date and time: ")
    print("\nSelect start timezone:")
    start_tz = get_timezone_input("Enter selection: ")
    start_tz_obj = pytz.timezone(start_tz)
    start_dt = start_tz_obj.localize(start_dt)
    
    print("\n=== Work End Information ===")
    end_dt = get_datetime_input("Enter end date and time: ", default_date=start_dt)
    print("\nSelect end timezone:")
    end_tz = get_timezone_input("Enter selection: ")
    end_tz_obj = pytz.timezone(end_tz)
    end_dt = end_tz_obj.localize(end_dt)
    
    # Calculate DST adjustment
    start_dst = start_dt.tzinfo.dst(start_dt)
    end_dst = end_dt.tzinfo.dst(end_dt)
    dst_adjustment = end_dst - start_dst
    
    # Convert end time to start timezone for accurate duration calculation
    end_dt_converted = end_dt.astimezone(start_tz_obj)
    
    # Calculate duration
    duration = end_dt_converted - start_dt
    hours_worked = duration.total_seconds() / 3600
    
    # Validate that end time is after start time
    if hours_worked < 0:
        print("Error: End time cannot be before start time!")
        return
    
    # Save to CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            start_dt.strftime('%Y-%m-%d'),
            start_dt.strftime('%H:%M'),
            start_tz,
            end_dt.strftime('%H:%M'),
            end_tz,
            f"{hours_worked:.2f}",
            f"{dst_adjustment.total_seconds() / 3600:.2f}"
        ])
    
    # Show summary with timezone information
    print("\n=== Work Session Summary ===")
    print(f"Start: {start_dt.strftime('%Y-%m-%d %H:%M')} {start_tz}")
    print(f"End: {end_dt.strftime('%Y-%m-%d %H:%M')} {end_tz}")
    print(f"Total hours worked: {hours_worked:.2f}")
    print(f"DST Adjustment: {dst_adjustment.total_seconds() / 3600:.2f} hours")
    print(f"Data saved to {csv_file}")

if __name__ == "__main__":
    main()
