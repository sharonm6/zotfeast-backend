import datetime
from icalendar import Calendar

def is_day_in_event(event, target_date: datetime):
    start_date = event.get("DTSTART").dt.date()
    if target_date < start_date:
        return False

    end_date = event.get("DTEND").dt.date()

    if event.get("RRULE") is not None:
        recurrence = event.get("RRULE").to_ical().decode()

        if "UNTIL" in recurrence:
            until = datetime.datetime.strptime(recurrence.split(";UNTIL=")[1], "%Y%m%dT%H%M%S")
            if target_date > until.date():
                return False

        elif "COUNT" in recurrence:
            count = int(recurrence.split(";COUNT=")[1].split(";")[0])
            if count <= 0:
                return False
            
            if ";FREQ=" in recurrence:
                freq = recurrence.split(";FREQ=")[1].split(";")[0]
            elif "FREQ" in recurrence:
                freq = recurrence.split("FREQ=")[1].split(";")[0]
            else:
                return False
            
            if freq == "DAILY":
                if target_date > end_date:
                    return False

            elif freq == "WEEKLY":
                if "BYDAY" in recurrence:
                    byday = recurrence.split(";BYDAY=")[1].split(",")
                    weekdays = {
                        "SU": 6,
                        "MO": 0,
                        "TU": 1,
                        "WE": 2,
                        "TH": 3,
                        "FR": 4,
                        "SA": 5
                    }
                    target_weekday = target_date.weekday()
                    if target_weekday not in [weekdays[day] for day in byday]:
                        return False
                else:
                    if target_date.weekday() != start_date.weekday():
                        return False

            elif freq == "MONTHLY":
                if target_date.day != start_date.day:
                    return False

            elif freq == "YEARLY":
                if target_date.month != start_date.month or target_date.day != start_date.day:
                    return False

            if freq == "DAILY":
                num_occurrences = (target_date - start_date).days + 1
            elif freq == "WEEKLY":
                num_occurrences = (target_date - start_date).days // 7 + 1
            elif freq == "MONTHLY":
                num_occurrences = (target_date.year - start_date.year) * 12 + (target_date.month - start_date.month) + 1
            elif freq == "YEARLY":
                num_occurrences = target_date.year - start_date.year + 1

            if num_occurrences > count:
                return False

    if event.get("EXDATE") is not None:
        excluded_dates = event.get("EXDATE")
        if isinstance(excluded_dates, list):
            excluded_dates = [excluded_date.dts[0].dt.date() for excluded_date in excluded_dates]
        else:
            excluded_dates = [excluded_dates.dts[0].dt.date()]
        if target_date in excluded_dates:
            return False

    return True

def get_day_interval_encoding(event, interval_encoding: list[int]):
    start_time = event.get("DTSTART").dt.time()
    end_time = event.get("DTEND").dt.time()

    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute

    for i in range(start_minutes // 30, end_minutes // 30 + 1):
        interval_encoding[i] = 1

    return interval_encoding

def generate_encoding(ics : str, day : datetime):
    cal = Calendar.from_ical(ics)

    interval_encoding = [0] * 48

    for event in cal.walk("VEVENT"):
        if is_day_in_event(event, day):
            interval_encoding = get_day_interval_encoding(event, interval_encoding)

    return interval_encoding

def parse_schedule(ics : str, day : datetime):
    '''
    Given an ics_file and datetime, returns a string of 0s and 1s representing the schedule for that day from 8AM to 12AM in time intervals of 30 minutes.

    1s represent that the user is busy during that time interval, and 0s represent that the user is free during that time interval.
    '''
    interval_encoding = generate_encoding(ics, day)
    return "".join([str(i) for i in interval_encoding[-32:]])
    
if __name__ == "__main__":
    print(parse_schedule("data/schedule_s.ics", datetime.date(2023, 10, 3)))