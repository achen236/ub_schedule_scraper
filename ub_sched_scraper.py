import string
import unicodedata
import requests
from bs4 import BeautifulSoup
import re
import html5lib
from multiprocessing import Pool
from multiprocessing import cpu_count
from functools import partial
import time


# Request website and download HTML
def getDeptURLs(semester: str, division: str = "UGRD"):
    # Get soup
    url = 'https://www.buffalo.edu/class-schedule?semester=' + semester
    request = requests.get(url)
    content = request.text 
    soup = BeautifulSoup(content, "html.parser")

    # Get all links to each department course schedule pages
    deptURLs = []
    baseShowCourseLink = "http://www.buffalo.edu/class-schedule?switch=showcourses&semester=" + semester + "&division=" + division + "&dept="
    for link in soup.find_all("a"):
        url = link.get("href")
        if url.startswith(baseShowCourseLink):
            deptURLs.append(url)
    return deptURLs

# In each department course schedule page extract data into list of dictionaries
# {"Dept": [Course1 = {"CourseAttr": Value}, Course2 = {"CourseAttr": Value}, . . .]}
def getSchedDict(semester:string = "spring", processors: int = 1, division: str = "UGRD"):
    retDict = {}
    # timer
    start=time.time()
    # get list of Dept URLS
    deptURLs = getDeptURLs(semester, division)
    # Uniprocessing
    if processors < 2:
        for url in deptURLs:
            soup = getSoup(url)
            # Get dept abbreviation from url
            # Add (dept key : {}) to retDict
            dept = url.split("=")[-1].strip()
            print(dept)
            retDict[dept] = getDeptList(soup)
            print("Multiprocessing Scraping Time Taken: ",str(time.time()-start))
            return retDict
    # Multiprocessing
    else:
        pool = Pool(min(processors, cpu_count()))  # Creates a Pool with number of processors (max processors = cpu_count)
        results = pool.map(partial(getSchedDictProcessorHelper, semester=semester, division=division ),deptURLs)

        print("Multiprocessing " + str(processors) + " Scraping Time Taken: ",str(time.time()-start))
        for result in results:
            retDict[result[0]] = result[1]
        return retDict


#return tuple (dept name, list of courseDicts in dept)
def getSchedDictProcessorHelper(url, semester: str, division: str = "UGRD"):
    # wait 5-10 seconds so we dont get blocked
    # time.sleep(random.randint(5, 10))
    soup = getSoup(url)
    # Get dept abbreviation from url
    # Add (dept key : {}) to retDict
    dept = url.split("=")[-1].strip()
    print(dept)
    return (dept, getDeptList(soup))




# Fill deptDict at department schedule url page
# Returns list of Department's courses
def getDeptList(soup):
    deptList = []
    #print("Getting deptDict\n")

    # Get list of labels
    labels = getLabels(soup)
    # Get course rows
    tableRows = soup.find_all(lambda tag: tag.name=="tr" and tag.has_attr("onmouseover") and tag.has_attr("onmouseout") and tag.has_attr("onclick"))
    # For each course row get class num as key for classDict{labels:text}
    for row in tableRows:  
        classNumRows = row.find_all("td")
        deptList.append(getCourseDict(classNumRows, labels))

    return deptList


# Get classDict
def getCourseDict(classNumRows, labels):
    courseDict = {}
    #print("Getting classDict\n")

    # Fill dictionary with label:text
    i = 0
    for col in classNumRows:
        text = stringNormalize(col.string)
        # Get course name from hyperlink
        course = col.find("a")
        if course != None:
            courseDict[labels[i]] = stringNormalize(course.string)
            detailsURL = course["href"]
            # returns int of enrolled students in class
            enrolled = getEnrolled(detailsURL)
            courseDict["Enrolled"] = enrolled
            i += 1
        elif text:
            if labels[i] == "Time":
                text = removeAllWhiteSpace(text)
            courseDict[labels[i]] = text
            i += 1

    return courseDict

def getEnrolled(url):
    soup = getSoup(url)
    td = soup.find("td", text = re.compile("Enrollment Total"))
    enrolled = td.find_next_sibling("td").text
    return int(enrolled)

# Get soup
def getSoup(url):
    request = requests.get(url)
    content = request.text
    soup = BeautifulSoup(content, "html5lib")
    return soup

# Turn soup's NavigableString into str and unicode normalize it
def stringNormalize(navigableString):
    string = str(navigableString)
    normalString = unicodedata.normalize("NFKD", string)
    return normalString.strip()

# Get list of column labels
def getLabels(soup):
    retList = []
    labels = soup.find_all("td", class_ = "gridlabel", limit = 11)
    #print(labels)
    for label in labels:
        text = stringNormalize(label.string)
        retList.append(text)
    return retList

def removeAllWhiteSpace(string: string):
    return "".join(string.split())

def main():
    #print(getSchedDict("spring"))
    #soup = getSoup("https://www.buffalo.edu/class-schedule?switch=showcourses&semester=spring&division=UGRD&dept=AAS")
    #getDeptDict(soup)
    return
    
if __name__ == "__main__":
    main()