
# TimeTraveler

**TimeTraveler** is a Python tool for tracking work sessions across multiple time zones. It calculates total hours worked, including adjustments for daylight saving time (DST), and logs all data to a CSV file for easy record-keeping.

---

## Features
- Navigate through time zones like a true TimeTraveler!
- Automatically handles daylight saving time (DST) adjustments.
- Validates and logs work session data with start and end times.
- Outputs all results to a CSV file for future reference.

---

## Requirements
- Python 3.7 or higher
- Required package: `pytz`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bytesweep/timetraveler.git
   cd timetraveler
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script**:
   ```bash
   python timetraveler.py
   ```

---

## Usage Instructions

1. **Follow the Prompts**:
   - Enter the start date and time of your work session.
   - Select the time zone for your start time.
   - Enter the end date and time of your work session.
   - Select the time zone for your end time.

2. **Output**:
   - TimeTraveler calculates:
     - Total hours worked.
     - DST adjustments (if applicable).
   - Data is saved to `work_time.csv` with the following fields:
     - Date
     - Start Time
     - Start Timezone
     - End Time
     - End Timezone
     - Total Hours Worked
     - DST Adjustment

3. **CSV File**:
   - Open `work_time.csv` in any spreadsheet editor to view logged sessions.

---

## Example Output
A sample CSV entry:
```csv
Date,Start Time,Start Timezone,End Time,End Timezone,Total Hours Worked,DST Adjustment
2024-03-19,09:00,US/Eastern,17:00,US/Pacific,8.00,-3.00
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
