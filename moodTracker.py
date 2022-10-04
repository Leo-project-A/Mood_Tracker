from logging import exception
import string
import random
from dataclasses import dataclass, field
from datetime import datetime, date
import csv

HEADERS = ['logID', 'date', 'time', 'overall feeling', 'anxiety level', 'mood', 'exercise', 'reading', 'health', 'phone use/social media']
OVERALL_RATES = ["1", "2", "3", "4", "5"]
ANXIETY_RATES = ["None", "low", "moderate", "HIGH"]
MOOD_RATES = [":D", ":)", ":|", "):", "D;"]
EXERCISE_RATES = ["none", "workout", "15 min walk", "bouldering", "surf", "weights"]
READING_RATES = ["0", "1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100", "100+"]
HEALTH_RATES = ["Healthy", "mild symptoms", "sickness", "severe sickness"]
PHONE_RATES = ["EXTREME", "too much", "moderate", "safe use", "detox"]

def generate_id() -> str:
    return "".join(random.choices(string.hexdigits, k= 16))
def generate_date() -> str:
    return date.today().strftime("%d-%m-%Y")
def generate_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

@dataclass
class Log:
    """id=HEX bumber represented in str"""
    _id: str = field(default_factory=generate_id)
    _date: str = field(default_factory=generate_date)
    _time: str = field(default_factory=generate_time)

    overall: str = ""
    anxiety: str = ""
    mood: str = ""
    exercise: str = "" 
    reading: str = ""
    health: str = ""
    phone: str = ""

@dataclass
class Tracker():
    _id: str = field(default_factory=generate_id)
    _date: str = field(default_factory=generate_date)

    _first_name: str = "John"
    _last_name: str = "Doe"

    logs: list[Log] = field(default_factory=list)
    _personal_score: int = 0
    _moodAvg: int = 0

    def add_new_log(self, logObj: Log) -> None:
        self.logs.append(logObj)

def load_tracker(filepath: str) -> Tracker:
    try:
        with open(filepath, 'r') as file:
            id = file.readline().strip().replace(',','')

            string = file.readline().strip().replace(',','').split(' ')
            first_name = string[0]
            last_name = string[1]

            tracker_date = file.readline().strip().replace(',','')
            file.readline()
            csv_reader = csv.reader(file, delimiter=',', quotechar='"')
            logs = []
            for row in csv_reader:
                logs.append(Log(*row))

            trackerObj = Tracker(id, tracker_date, first_name, last_name, logs)
        return trackerObj
    except Exception as e:
        raise e

def dump_tracker(trackerObj: Tracker, filepath: str) -> None:
    try:
        with open(filepath, 'w') as file:
            file.write(trackerObj._id + '\n')
            file.write(trackerObj._first_name + ' ' + trackerObj._last_name + '\n')
            file.write(trackerObj._date + '\n')
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer = csv.DictWriter(file, fieldnames=HEADERS)   
            writer.writeheader()
        for log in trackerObj.logs:
            dump_log(log, filepath)
    except Exception as e:
        print("failed to dump data")
        raise e

def dump_log(logObj: Log, filepath: str) -> None:
    try:
        with open(filepath, 'a', newline='') as file:
            file.write(','.join([
                logObj._id,
                logObj._date,
                logObj._time,
                logObj.overall,
                logObj.anxiety,
                logObj.mood,
                '"' + logObj.exercise + '"',
                logObj.reading,
                logObj.health,
                logObj.phone]) + '\n')
        print(f"log {logObj._id} dumped!")
    except Exception as e:
        print(f"failed to load log {logObj._id}")
        raise e
