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
        df.to_csv("./csv/" + dept + ".csv", index = False)

# Get all department schedules to csv
def getCSVAllDeptSched(schedDict, overwrite = False):
    for dept in schedDict.keys():
        getCSVDeptSched(schedDict, dept, overwrite)

# Save schedDict to pickle
def saveSchedDict():
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict("spring")

    with open("schedDict.pkl", "wb") as tf:
        pickle.dump(schedDict, tf)

# Load schedDict from pickle
def loadSchedDict():
    if not exists("./schedDict.pkl"):
        saveSchedDict
    with open("schedDict.pkl", "rb") as tf:
        schedDict = pickle.load(tf)
    return schedDict

def main():
    getCSVAllDeptSched(ub_sched_scraper.getSchedDict("spring"), True )
    saveSchedDict()
    print(loadSchedDict())
    
if __name__ == "__main__":
    main()