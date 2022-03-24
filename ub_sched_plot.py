import string
import ub_sched_data, ub_sched_scraper
import plotly.express as px
import math
import numpy

# return matrix with values of number of course at an interval of hour of a day in week
# counts Courses by default, if countPeople is True, count people enrolled in class
def schedCoursesMatrix(timeInterval: int, dayRange:int, countPeople: bool = False):
    # initialize matrix of zeros
    timeRange = getTimeRange(timeInterval)
    matrix = initializeSchedMatrix(timeRange, dayRange)
    schedDict = ub_sched_data.loadSchedDict()
    print("Forming Data")
    for courses in schedDict.values():
        for course in courses:
            days = course["Days"]
            time = course["Time"]
            # get binary list of class days
            binDays = parseDays(days)
            # if empty continue
            if not binDays:
                continue
            # get tuple (start,end) in military time, returns (-1,-1) if not valid time
            startEndMilTime = parseTime(time)
            # if not number time, skip course
            if startEndMilTime[0] == -1:
                continue
            # for each day add 1 to time interval matrix cell when class in session
            for i in range(dayRange):
                if binDays[i] == 1:
                    print("Next day")
                    startIndex = getIndexOfTime(startEndMilTime[0], timeInterval)
                    endIndex = getIndexOfTime(startEndMilTime[1], timeInterval)
                    print(startIndex)
                    print(endIndex)
                    j = startIndex
                    while j <= endIndex:
                        print("Next time")
                        # add course to total courses in that time interval
                        matrix[j][i] += 1
                        j += 1
    return matrix

def plotSched(colorName, timeInterval = 30, dayRange = 6, ):
    data = schedCoursesMatrix(timeInterval, dayRange)
    print("Plotting")
    fig = px.imshow(data,
                    labels=dict(x="Day of Week", y="Time of Day", color=colorName),
                    x= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                    y= getListofTimeIntervals(timeInterval),
                    aspect="auto"
                )
    fig.layout.height = 750
    fig.layout.width = 750
    fig.update_xaxes(side="top")
    fig.show()            

# get index of time in a list given the timeInterval 
def getIndexOfTime(time: int, timeInterval: int):
    minutes = (int(str(time)[:-2]) * 60) + int(str(time)[-2:])
    return math.ceil(minutes / timeInterval) - 1

# timeInterval input 0-60 minutes
def getListofTimeIntervals(timeInterval):
    retList = []
    time = 0000
    minutes = 0
    while time < 2400:
        retList.append(timeIntToString(time))
        # if minutes == 60 add 40 to time to get next hour
        minutes += timeInterval
        if minutes == 60:
            minutes = 0
            time += 40
        time += timeInterval
    return retList

def timeIntToString(time: int):
    if time == 0:
        return "12:00AM"
    elif time < 10:
        return "12" + ":0" + str(time) + "AM"
    elif time < 100:
        return "12"+ ":" + str(time) + "AM"
    elif time < 1000:
        return str(time)[:1] + ":" + str(time)[-2:] + "AM"
    elif time < 1200:
        return str(time)[:2] + ":" + str(time)[-2:] + "AM"
    elif time < 1300:
        return str(time)[:2] + ":" + str(time)[-2:] + "PM"
    elif time < 2200:
        return str(time - 1200)[:1] + ":" + str(time)[-2:] + "PM"
    elif time < 2400:
        return str(time - 1200)[:2] + ":" + str(time)[-2:] + "PM"

def getTimeRange(timeInterval):
    # 60 / timeInterval - 1
    # Number of minute intervals minus the 60 min interval
    # * 24 
    # Each hour of minute intervals for each hour in day
    # + 24
    # Each hour in day
    return (((math.ceil(60 / timeInterval) - 1)) * 24) + 24

# [[ 0 ], [ 1 ]. [ 2 ], ... [ timeRange ] ]
def initializeSchedMatrix(timeRange: int, dayRange: int):
    retMatrix = []
    for hour in range(timeRange):
        row = []
        retMatrix.append(listOfZeros(dayRange))
    return retMatrix

# returns binary list. 1 if class else 0 
def parseDays(days: string):
    if days == "TBA" or len(days) > 6:
        return []
    retList = listOfZeros(6)
    days = ub_sched_scraper.removeAllWhiteSpace(days)
    for day in days:
        if day == "M":
            retList[0] = 1
        elif day == "T":
            retList[1] = 1
        elif day == "W":
            retList[2] = 1
        elif day == "R":
            retList[3] = 1
        elif day == "F":
            retList[4] = 1
        elif day == "S":
            retList[5] = 1
    return retList

# convert time to military time
# return tuple start end time of class
def parseTime(time: string):
    if not time[0].isdigit():
        return (-1,-1)
    startEndTimes = time.split("-")
    # start , end
    return (militaryTime(startEndTimes[0]), militaryTime(startEndTimes[1]))

# convert string to military time in ints 
# 11:00PM -> 2300, 12:00PM -> 1200
# 11:00AM -> 1100, 12:00AM -> 0000
def militaryTime(time: string):
    if time[-2] == "P":
        timeSplit = time[:-2].split(":")
        timePM = int(timeSplit[0] + timeSplit[1])
        if timePM < 1200:
            timePM = timePM + 1200
        return timePM
    else:
        timeSplit = time[:-2].split(":")
        timeAM = int(timeSplit[0] + timeSplit[1])
        if timeAM >= 1200:
            timeAM = timeAM - 1200
        return timeAM

def listOfZeros(n: int):
    return [0] * n

def main():
    print("Getting Data")
    #ub_sched_data.saveSchedDict()
    plotSched('Courses', 10)

if __name__ == "__main__":
    main()