import moodTracker
import os
from datetime import date

TRACKER_DIR = 'trackers/'

def run():
    trackers = [item.split('.')[0] for item in os.listdir(TRACKER_DIR)]
    show_trackers(trackers)

    user_input = input("please select your name. or type 'new' to create new tracker \n>")
    user_input = convert_name(user_input)
    if user_input == 'New':
        trackerObj = create_new_tracker()
        filepath = TRACKER_DIR + convert_name(trackerObj._first_name + ' ' + trackerObj._last_name) + '.csv'
    elif user_input not in trackers:
        print(f"{user_input} doesn't exist in the system. :(")
        return
    else:
        filepath = TRACKER_DIR + user_input + '.csv'
        trackerObj = moodTracker.load_tracker(filepath)
        print("<---------------------------------------->")
        print(f"\tWelcome Back {trackerObj._first_name} {trackerObj._last_name}")
    if trackerObj.logs != []:
        lastDate = trackerObj.logs[-1]._date
        if str(date.today().strftime("%d-%m-%Y")) == lastDate:
            print("You already logged today, come back tomorrow :)")
            return
    trackerObj.add_new_log(newRecord())
    moodTracker.dump_tracker(trackerObj, filepath)
    print("<---------------------------------------->")
    print(f"\tGood Job {trackerObj._first_name} {trackerObj._last_name}, See you tomorrow! :)")
    return 

def convert_name(string_name: str):
    return string_name.strip().lower().capitalize().replace(' ','_')

def default_format(string: str) -> str:
    return string.strip().lower()
    
def show_trackers(tracker_list: list[moodTracker.Tracker]):
    print("<---------------------------------------->")
    print("Avaliable Users:")
    for item in tracker_list:
        print(f"\t {item}")
    print("<---------------------------------------->")

def create_new_tracker():
    print("<---------------------------------------->")
    print("\tWelcome to the Mood Track System!")
    first_name = input("what is your First name? \n>")
    last_name = input("what is your Last name? \n>")
    trackerObj = moodTracker.Tracker(_first_name=first_name, _last_name=last_name)
    print(f"\t {first_name} {last_name}, welcome to your new tracker!")
    print("Lets enter your first log :")
    print("<---------------------------------------->")
    filepath = TRACKER_DIR + convert_name(trackerObj._first_name + ' ' + trackerObj._last_name) + '.csv'
    moodTracker.dump_tracker(trackerObj, filepath)
    return trackerObj

def newRecord():
    while True:
        input_overall = default_format(input(f'''How would you rete your Overall feeling today?
        horrible -> {moodTracker.OVERALL_RATES} -> Excellent
        >'''))
        if input_overall in moodTracker.OVERALL_RATES:
            break
    while True:
        input_anxiety = default_format(input(f'''How were your Anxiety levels today?
        {moodTracker.ANXIETY_RATES}
        >'''))
        if input_anxiety in moodTracker.ANXIETY_RATES:
            break
    while True:
        input_mood = default_format(input(f'''How was your Mood today?
        {moodTracker.MOOD_RATES}
        >'''))
        if input_mood in moodTracker.MOOD_RATES:
            break
    input_exercise = set()
    while True:
        entry = default_format(input(f'''Did you have any exercise today? name it all. type 'Done' when finished.
        {moodTracker.EXERCISE_RATES}
        >'''))
        if entry in moodTracker.EXERCISE_RATES:
            input_exercise.add(entry)
        if entry == 'done':
            break
    if not input_exercise:
        input_exercise.add('none')
    input_exercise = ','.join(list(input_exercise))
    while True:
        input_reading = default_format(input(f'''How Much did you Read today?
        >'''))
        try:
            input_reading = int(int(input_reading)/10) + 1
            if input_reading > 11:
                input_reading = 11
            input_reading = moodTracker.READING_RATES[input_reading]
            break
        except:
            continue
    while True:
        input_health = default_format(input(f'''How was your Health today?
        {moodTracker.HEALTH_RATES}
        >'''))
        if input_health in moodTracker.HEALTH_RATES:
            break
    while True:
        input_phoneUse = default_format(input(f'''How was your phone/social media Use today?
        {moodTracker.PHONE_RATES}
        >'''))
        if input_phoneUse in moodTracker.PHONE_RATES:
            break
    logObj = moodTracker.Log(
        overall=input_overall,
        anxiety=input_anxiety, 
        mood=input_mood, 
        exercise=input_exercise, 
        reading=input_reading, 
        health=input_health, 
        phone=input_phoneUse)
    return logObj

if __name__ == '__main__':
    run()