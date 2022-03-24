import string
import pandas as pd
import pickle
from os.path import exists

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
def saveSchedDict(semester: string, processors: int = 1):
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict(semester, processors)

    with open("schedDict.pkl", "wb") as tf:
        pickle.dump(schedDict, tf)
    print("Saved schedDict to schedDict.pkl")

# Load schedDict from pickle
def loadSchedDict():
    if not exists("./schedDict.pkl"):
        saveSchedDict
    with open("schedDict.pkl", "rb") as tf:
        schedDict = pickle.load(tf)
    return schedDict

def main():
    saveSchedDict("spring", 4)
    getCSVAllDeptSched(loadSchedDict(), True)
    
if __name__ == "__main__":
    main()