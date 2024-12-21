import argparse
import logging
import json
import uuid
from icalendar import Calendar, Event, vText
from tqdm import tqdm
from datetime import datetime, timedelta


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(filename='redux.log', level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def is_leap_year(year: int) -> bool:
    """Determine if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def load_solstice_data(file_path: str) -> dict:
    """Load solstice data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            solstice_data = json.load(f)
        logging.info("Solstice data successfully loaded.")
        return solstice_data
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading solstice data: {e}")
        return {}


def create_event(summary: str, description: str, date: datetime.date) -> Event:
    """Create a calendar event."""
    event = Event()
    event.add('summary', vText(summary))
    event.add('description', vText(description))
    event.add('dtstart', date)
    event.add('dtend', date + timedelta(days=1))
    event.add('uid', f"{uuid.uuid4()}@reduxcalendar.com")
    return event


def generate_ics_for_year(year: int, solstice_data: dict) -> Calendar:
    """Generate Redux calendar events for a specific year."""
    calendar = Calendar()
    calendar.add('prodid', '-//Redux//EN')
    calendar.add('version', '2.0')
    calendar.add('calscale', 'GREGORIAN')

    # Get solstice date from JSON data
    solstice_info = solstice_data.get(str(year))
    if not solstice_info:
        logging.error(f"Solstice data for year {year} not found. Skipping year.")
        return calendar

    solstice_date = datetime.strptime(solstice_info["date"], "%Y-%m-%d").date()
    redux_year = year + 1  # Redux year starts the day after solstice
    calendar.add_component(create_event(
        summary="Zero Day",
        description=f"Winter Solstice Zero Day ({solstice_info['time_gmt']} GMT)",
        date=solstice_date
    ))

    # Add Redux calendar days starting from the day after the solstice
    current_date = solstice_date + timedelta(days=1)
    redux_day = 1
    redux_month = 1

    for _ in range(364):  # 13 months of 28 days each
        calendar.add_component(create_event(
            summary=f"{redux_month}/{redux_day}/{redux_year} Redux",
            description=f"Redux Calendar - Month {redux_month}, Day {redux_day}",
            date=current_date
        ))
        current_date += timedelta(days=1)
        redux_day += 1
        if redux_day > 28:  # Reset day and increment month
            redux_day = 1
            redux_month += 1

    # Add Double Zero Day for leap years
    if is_leap_year(year):
        calendar.add_component(create_event(
            summary="Double Zero Day",
            description="Leap Year Double Zero Day",
            date=current_date
        ))

    return calendar


def write_to_file(base_name: str, counter: int, calendar: Calendar, start_year: int, end_year: int):
    """Write a calendar to a file."""
    file_name = f"{base_name}_part{counter}_{start_year}-{end_year}.ics"
    with open(file_name, "wb") as file:
        file.write(calendar.to_ical())
    print(f"Generated: {file_name}")


def write_split_ics_files(start_year: int, end_year: int, base_name: str, size_limit: int, solstice_file: str):
    """Write multiple ICS files split by size limit."""
    solstice_data = load_solstice_data(solstice_file)

    combined_calendar = Calendar()
    combined_calendar.add('prodid', '-//Redux//EN')
    combined_calendar.add('version', '2.0')
    combined_calendar.add('calscale', 'GREGORIAN')

    current_size = 0
    counter = 1
    current_start_year = start_year

    for year in tqdm(range(start_year, end_year + 1), desc="Processing Years", unit="year"):
        year_calendar = generate_ics_for_year(year, solstice_data)
        year_size = len(year_calendar.to_ical())

        if current_size + year_size > size_limit:
            write_to_file(base_name, counter, combined_calendar, current_start_year, year - 1)
            combined_calendar = Calendar()
            combined_calendar.add('prodid', '-//Redux//EN')
            combined_calendar.add('version', '2.0')
            combined_calendar.add('calscale', 'GREGORIAN')
            current_start_year = year
            counter += 1
            current_size = 0

        for component in year_calendar.subcomponents:
            combined_calendar.add_component(component)
        current_size += year_size

    if len(combined_calendar.subcomponents) > 0:
        write_to_file(base_name, counter, combined_calendar, current_start_year, end_year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Redux ICS files.")
    parser.add_argument("--start_year", type=int, default=2024)
    parser.add_argument("--end_year", type=int, default=2100)
    parser.add_argument("--base_name", type=str, default="redux")
    parser.add_argument("--size_limit", type=int, default=1000000)
    parser.add_argument("--solstice_file", type=str, default="solstices_precise.json")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    configure_logging(args.verbose)

    write_split_ics_files(args.start_year, args.end_year, args.base_name, args.size_limit, args.solstice_file)
