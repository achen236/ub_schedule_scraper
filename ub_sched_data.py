import string
import pandas as pd
import pickle
from os.path import exists
import json

import ub_sched_scraper


# Get department schedule to csv
def getCSVDeptSched(schedDict, dept, overwrite = False):
    # Create dataframe
    df = pd.DataFrame.from_records(schedDict[dept])
    if not exists("./csv/" + dept + ".csv"):
        df.to_csv("./csv/" + dept + ".csv", index = False)
    elif overwrite:
        print("Overwriting CSVs")
        df.to_csv("./csv/" + dept + ".csv", index = False)
    else:
        print("Already have CSVs")

# Get all department schedules to csv
def getCSVAllDeptSched(schedDict, overwrite = False):
    for dept in schedDict.keys():
        getCSVDeptSched(schedDict, dept, overwrite)

# Save schedDict to pickle
# Multiprocessing if processors > 1
def saveSchedDictPkl(semester: string, processors: int = 1):
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict(semester, processors)

    with open("schedDict.pkl", "wb") as tf:
        pickle.dump(schedDict, tf)
    print("Saved schedDict to schedDict.pkl")

# Load schedDict from pickle
def loadSchedDictPkl():
    if not exists("./schedDict.pkl"):
        print("./schedDict.pkl does not exist")
    with open("schedDict.pkl", "rb") as tf:
        schedDict = pickle.load(tf)
    return schedDict

# Save schedDict to JSON
def saveSchedDictJSON(semester: string, processors: int = 1):
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict(semester, processors)

    with open("schedDict.json", "w") as tf:
        json.dump(schedDict, tf, indent=6)
    print("Saved schedDict to schedDict.json")

# Load schedDict from JSON
def loadSchedDictJSON():
    if not exists("./schedDict.json"):
        print("./schedDict.json does not exist")
    with open("schedDict.json", "r") as tf:
        schedDict = json.load(tf)
    return schedDict


def main():
    #saveSchedDictPkl("spring", 1)
    saveSchedDictJSON("spring", 4)
    #getCSVAllDeptSched(loadSchedDict(), True)
    
if __name__ == "__main__":
    main()