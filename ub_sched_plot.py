from ctypes.wintypes import INT
from tokenize import String
import ub_sched_data, ub_sched_scraper
import plotly.express as px

# return matrix with values of number of people in classes at an hour of day
def schedPeopleMatrix(timeRange: int, dayRange:int):
    # initialize matrix of zeros
    matrix = initializeSchedMatrix(timeRange, dayRange)
    schedDict = ub_sched_scraper.loadSchedDict()
    for dept in schedDict.keys():
        for course in dept:
            days = course["Days"]
            time = course["Time"]
            # get binary list of class days
            binDays = parseDays(days)
            # get tuple (start,end) in military time
            startEndMilTime = parseTime(time)
        for i in range(dayRange):
            if binDays[i] == 1:
                for 

    return data

def getListofHours(timeInterval):
    


# [[ 0 ], [ 1 ]. [ 2 ], ... [ timeRange ] ]
def initializeSchedMatrix(timeRange: int, dayRange: int):
    retMatrix = []
    for hour in range(timeRange):
        row = []
        retMatrix.append(listOfZeros(dayRange))
    return retMatrix

# returns binary list. 1 if class else 0 
def parseDays(days: String):
    retList = listOfZeros(6)
    days = ub_sched_scraper.removeAllWhiteSpace(days)
    for day in days:
        if day == "M":
            retList[0] == 1
        elif day == "T":
            retList[1] == 1
        elif day == "W":
            retList[2] == 1
        elif day == "R":
            retList[3] == 1
        elif day == "F":
            retList[4] == 1
        elif day == "S":
            retList[5] == 1
    return retList

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

def listOfZeros(n: int):
    return [0] * n

def main():
    return 0

if __name__ == "__main__":
    main()