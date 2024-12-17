import argparse
import logging
import uuid
from icalendar import Calendar, Event, vText
from astral.sun import sun
from astral import LocationInfo
from tqdm import tqdm
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(filename='full_redux_calendar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def is_leap_year(year: int) -> bool:
    """Determine if a year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_winter_solstice_date(year: int) -> datetime.date:
    """
    Use the astral library to get the exact date of the winter solstice.
    Assumes UTC and solstice happening at northern hemisphere.
    """
    city = LocationInfo("Greenwich", "UK", "UTC", latitude=51.5, longitude=0)
    solstice = sun(city.observer, date=datetime(year, 12, 21))["sunrise"].date()
    return solstice


def create_event(summary: str, description: str, date: datetime.date) -> Event:
    """Create an iCalendar event."""
    event = Event()
    event.add('summary', vText(summary))
    event.add('description', vText(description))
    event.add('dtstart', date)
    event.add('dtend', date + timedelta(days=1))  # Event lasts one day
    event.add('uid', f"{uuid.uuid4()}@reduxcalendar.com")
    return event


def generate_ics_for_year(year: int) -> Calendar:
    """Generate the Redux Calendar events for a given year."""
    calendar = Calendar()
    calendar.add('prodid', '-//Full Redux Calendar//EN')
    calendar.add('version', '2.0')

    # Add Zero Day
    solstice_date = get_winter_solstice_date(year)
    calendar.add_component(create_event(
        summary="Zero Day",
        description="Winter Solstice Zero Day",
        date=solstice_date
    ))

    # Add the days of the year: 1/1 to 13/28
    current_date = solstice_date + timedelta(days=1)
    for month in range(1, 14):  # 13 months
        for day in range(1, 29):  # 28 days per month
            calendar.add_component(create_event(
                summary=f"Day {month}/{day}",
                description=f"Redux Calendar - Month {month}, Day {day}",
                date=current_date
            ))
            current_date += timedelta(days=1)

    # Add Double Zero Day for leap years
    if is_leap_year(year):
        calendar.add_component(create_event(
            summary="Double Zero Day",
            description="Leap Year Double Zero Day",
            date=solstice_date
        ))

    return calendar


def write_to_file(base_name: str, counter: int, calendar: Calendar, start_year: int, end_year: int):
    """Write the calendar to a file with the corrected year range in the filename."""
    file_name = f"{base_name}_part{counter}_{start_year}-{end_year}.ics"
    try:
        with open(file_name, "wb") as file:
            file.write(calendar.to_ical())
        logging.info(f"Generated: {file_name}")
        print(f"Generated: {file_name}")
    except IOError as e:
        logging.error(f"Error writing file {file_name}: {e}")
        print(f"Error writing file {file_name}: {e}")


def write_split_ics_files(start_year: int, end_year: int, base_name: str, size_limit: int):
    """Generate and split ICS files into parts with size limits."""
    combined_calendar = Calendar()
    combined_calendar.add('prodid', '-//Full Redux Calendar//EN')
    combined_calendar.add('version', '2.0')

    current_size = 0
    counter = 1
    current_start_year = start_year

    for year in tqdm(range(start_year, end_year + 1), desc="Processing Years", unit="year"):
        year_calendar = generate_ics_for_year(year)
        year_size = len(year_calendar.to_ical())

        if current_size + year_size > size_limit:
            write_to_file(base_name, counter, combined_calendar, current_start_year, year - 1)
            combined_calendar = Calendar()
            combined_calendar.add('prodid', '-//Full Redux Calendar//EN')
            combined_calendar.add('version', '2.0')
            current_start_year = year
            counter += 1
            current_size = 0

        combined_calendar.add_component(year_calendar)
        current_size += year_size

    # Write the last file
    if len(combined_calendar.subcomponents) > 0:
        write_to_file(base_name, counter, combined_calendar, current_start_year, end_year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Full Redux Calendar ICS files.")
    parser.add_argument("--start_year", type=int, default=2024, help="Starting year for the calendar.")
    parser.add_argument("--end_year", type=int, default=2100, help="Ending year for the calendar.")
    parser.add_argument("--base_name", type=str, default="full_redux_calendar", help="Base name for the output files.")
    parser.add_argument("--size_limit", type=int, default=1000000, help="Maximum file size in bytes.")

    args = parser.parse_args()

    if args.start_year > args.end_year:
        raise ValueError("Start year must be less than or equal to end year.")

    write_split_ics_files(args.start_year, args.end_year, args.base_name, args.size_limit)
