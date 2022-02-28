import pandas as pd
import ub_sched_scraper
from os.path import exists

def showDeptSchedule(dept):
    soup = ub_sched_scraper.getSoup("https://www.buffalo.edu/class-schedule?switch=showcourses&semester=spring&division=UGRD&dept=AAS")
    labels = ub_sched_scraper.getLabels(soup)

    # Scrape and collect data
    # {"Dept": [{"ClassAttr": Value}]}
    schedDict = ub_sched_scraper.getSchedDict("spring")

    # Create dataframe
    df = pd.DataFrame.from_records(schedDict[dept])
    print(df)
    
    if not exists(dept + ".csv"):
        df.to_csv(dept + ".csv")

    

def main():
    showDeptSchedule("CSE")
    
if __name__ == "__main__":
    main()