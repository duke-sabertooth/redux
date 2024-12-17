# Full Redux Calendar Generator - README

Welcome to the **Full Redux Calendar** generator! This tool creates `.ics` files for a unique calendar system based on the winter solstice as **Zero Day** and includes 13 months of 28 days each, plus **Double Zero Days** in leap years.

This README provides detailed instructions on how to set up, install dependencies, and run the generator.

---

## Table of Contents
1. [Requirements](#requirements)
2. [Installation Instructions](#installation-instructions)
3. [How to Run the Script](#how-to-run-the-script)
4. [Command-Line Options](#command-line-options)
5. [Generated Files](#generated-files)
6. [Troubleshooting](#troubleshooting)

---

## Requirements

Ensure you have the following before running the script:

- **Python**: Version 3.8 or higher  
  Verify your Python version by running:
  ```bash
  python --version
  ```
- **pip**: Python package manager  
  Verify `pip` installation:
  ```bash
  pip --version
  ```

---

## Installation Instructions

Follow these steps to install all necessary dependencies:

1. **Clone or Download the Script**  
   Clone this repository or download the script file `full_redux_calendar.py`:
   ```bash
   git clone https://github.com/yourusername/full_redux_calendar.git
   cd full_redux_calendar
   ```

2. **Install Dependencies**  
   Run the following command to install required Python libraries:
   ```bash
   pip install icalendar astral tqdm
   ```
   - **icalendar**: For generating ICS calendar files.
   - **astral**: For calculating accurate winter solstice dates.
   - **tqdm**: Provides a progress bar for better user experience.

   If you encounter errors, use `pip3` instead:
   ```bash
   pip3 install icalendar astral tqdm
   ```

---

## How to Run the Script

Run the script from the command line using the following format:

```bash
python full_redux_calendar.py --start_year 2024 --end_year 2100 --size_limit 1000000
```

### Explanation:
- `--start_year`: The first year to generate the Full Redux Calendar (default: 2024).  
- `--end_year`: The last year to generate the calendar (default: 2100).  
- `--size_limit`: Maximum file size in bytes for each `.ics` file. Default is 1,000,000 bytes (~1MB).  

### Example:
To generate calendars from **2024 to 2100** with a 1MB file size limit:
```bash
python full_redux_calendar.py --start_year 2024 --end_year 2100 --size_limit 1000000
```

---

## Command-Line Options

Here are all the available options:

| Option             | Description                                 | Default Value |
|--------------------|---------------------------------------------|---------------|
| `--start_year`     | Starting year for calendar generation.      | 2024          |
| `--end_year`       | Ending year for calendar generation.        | 2100          |
| `--base_name`      | Base name for output files.                 | full_redux_calendar |
| `--size_limit`     | Max size of each `.ics` file (in bytes).    | 1000000 (1MB) |

---

## Generated Files

- The script creates `.ics` files named as follows:
  ```
  full_redux_calendar_part1_2024-2100.ics
  full_redux_calendar_part2_2024-2100.ics
  ...
  ```

- **Log File**: A log file is saved as `full_redux_calendar.log` in the current directory.  
  - It contains details about processed years, generated files, and any errors encountered.

---

## Troubleshooting

1. **Module Not Found Errors**:
   - If you get `ModuleNotFoundError` for `icalendar`, `astral`, or `tqdm`, ensure all dependencies are installed:
     ```bash
     pip install icalendar astral tqdm
     ```

2. **Python Version Issues**:
   - Use `python3` or `pip3` if your system defaults to Python 2:
     ```bash
     python3 full_redux_calendar.py --start_year 2024 --end_year 2100
     ```

3. **Permission Denied**:
   - Ensure you have write permissions for the directory where the script is run.

4. **File Size Limits**:
   - If your ICS files are not splitting correctly, adjust the `--size_limit` parameter to a smaller value (e.g., `500000` for 500KB files).

5. **Missing Dependencies**:
   - Re-run the installation step:
     ```bash
     pip install --upgrade icalendar astral tqdm
     ```

---

## Example Output

Here is an example of the structure within a generated `.ics` file:

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Full Redux Calendar//EN
BEGIN:VEVENT
SUMMARY:Zero Day
DTSTART;VALUE=DATE:20241221
DTEND;VALUE=DATE:20241222
UID:86ecfa10-2000-4725-a2b6-672e5c2b1901@fullreduxcalendar.com
DESCRIPTION:Winter Solstice Zero Day
END:VEVENT
BEGIN:VEVENT
SUMMARY:Day 1/1
DTSTART;VALUE=DATE:20241222
DTEND;VALUE=DATE:20241223
UID:507dcb42-b2ec-4bc5-b732-2c775e6961ae@fullreduxcalendar.com
DESCRIPTION:Full Redux Calendar Day 1 of Month 1, Year 2025
END:VEVENT
...
END:VCALENDAR
```

---

## Feedback and Support

If you encounter any issues or have suggestions for improvement, feel free to open an issue in the repository or contact the developer:
 
- **GitHub**: https://github.com/duke-sabertooth/redux  

---

Enjoy using the **Full Redux Calendar Generator**! 🎉
