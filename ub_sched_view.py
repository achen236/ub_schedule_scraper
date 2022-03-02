import sched
import pandas as pd
import ub_sched_scraper
from os.path import exists

def showDeptSchedule(schedDict, dept):
    # Create dataframe
    print(schedDict)
    df = pd.DataFrame.from_records(schedDict[dept])
    print(df)

    if not exists("/csv/" + dept + ".csv"):
        df.to_csv("/csv/" + dept + ".csv")

def showSchoolSched():
    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict("spring")

    for dept, courseDict in schedDict.items():
        print(dept)
        showDeptSchedule(dept, schedDict)


def main():
    #showDeptSchedule("CSE")
    showSchoolSched()
    
if __name__ == "__main__":
    main()