from ctypes.wintypes import INT
from tokenize import String
import ub_sched_data, ub_sched_scraper
import plotly.express as px

# return matrix with values of number of people in classes at an hour of day
def schedPeopleMatrix(timeRange: int):
    matrix = initializeSchedMatrix(timeRange)
    schedDict = ub_sched_scraper.loadSchedDict()
    for dept in schedDict.keys():
        for course in dept:
            time = course["Time"]
            startEndMilTime = parseTime(time)
            

    return data

# [[ ... ], [ ... ]. [ ... ] ]
def initializeSchedMatrix(timeRange: int):
    retMatrix = []
    for hour in range(timeRange):
        row = []
        for day in range(5):
            row.append(0)
        retMatrix.append(row)
    return retMatrix

# convert time to military time
# return tuple start end time of class
def parseTime(time: String):
    retTuple = ()
    startEndTimes = time.split("-").strip()
    # parse start time
    retTuple[0] = militaryTime(startEndTimes[0][-2])
    # parse end time
    retTuple[1] = militaryTime(startEndTimes[1][-2])
    return retTuple

# convert string to military time in ints 
# 11:00PM -> 2300, 12:00PM -> 1200
# 11:00AM -> 1100, 12:00AM -> 0000
def militaryTime(time: String):
    if time[-2] == "P":
        timePM = int(startEndTimes[0].split("P")[0]) * 100 
        if timePM < 1200:
            timePM = timePM + 1200
        return timePM
    else:
        timeAM = int(startEndTimes[0].split("P")[0]) * 100
        if timeAM >= 1200:
            timeAM = timeAM - 1200
        return timeAM
        

def main():
    return 0

if __name__ == "__main__":
    main()