import pandas as pd
import pickle
from os.path import exists

import ub_sched_scraper


# Get department schedule to csv
def showDeptSchedule(schedDict, dept):
    # Create dataframe
    df = pd.DataFrame.from_records(schedDict[dept])

    if not exists("./csv/" + dept + ".csv"):
        df.to_csv("./csv/" + dept + ".csv", index = False)

# Get all department schedules to csv
def showSchoolSched(schedDict):
    for dept, courseDict in schedDict.items():
        showDeptSchedule(schedDict, dept)

# Save schedDict to pickle
def saveSchedDict():
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict("spring")

    with open("schedDict.pkl", "wb") as tf:
        pickle.dump(schedDict, tf)

# Load schedDict from pickle
def loadSchedDict():
    with open("schedDict.pkl", "rb") as tf:
        schedDict = pickle.load(tf)
    return schedDict

def main():
    #showDeptSchedule("CSE")
    #showSchoolSched()
    #saveSchedDict()
    print(loadSchedDict())
    
if __name__ == "__main__":
    main()