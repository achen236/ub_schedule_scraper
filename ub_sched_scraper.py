import re
import unicodedata
import requests
from os.path import exists
from bs4 import BeautifulSoup
import pandas as pd

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

# In each department course schedule page extract data into dictionary
# {"Dept": {"Class Number": {"ClassAttr": Value}}}
def getCourseDict(semester: str, division: str = "UGRD"):
    retDict = {}

    deptURLs = getDeptURLs("spring")
    for url in deptURLs:
        soup = getSoup(url)
        # Get dept abbreviation from url
        # Add (dept key : {}) to retDict
        dept = url.split("=")[-1].strip()
        retDict[dept] = getDeptDict(soup)
    
    return retDict



# Fill deptDict at department schedule url page
def getDeptDict(soup):
    deptDict = {}
    print("Getting deptDict\n")

    # Get list of labels
    labels = getLabels(soup)
    # Get course rows
    tableRows = soup.find_all(lambda tag: tag.name=="tr" and tag.has_attr("onmouseover") and tag.has_attr("onmouseout") and tag.has_attr("onclick"))
    # For each course row get class num as key for classDict{labels:text}
    for row in tableRows:  
        deptDict
        classNumRow = row.find("td")
        classNum = classNumRow.string
        deptDict[classNum] = getClassDict(soup, labels)

    return deptDict


# Get classDict
def getClassDict(classNumRow, labels):
    classDict = {}
    print("Getting classDict\n")

    # Fill dictionary with label:text
    i = 1
    for col in classNumRow.next_siblings:
        text = stringNormalize(col.string)
        if not re.search("^" + stringNormalize(col.string), "\n"):
            classDict[labels[i]] = text
            i += 1

    return classDict

# Get soup
def getSoup(url):
    request = requests.get(url)
    content = request.text
    soup = BeautifulSoup(content, "html.parser")
    return soup

# Turn soup's NavigableString into str and unicode normalize it
def stringNormalize(navigableString):
    string = str(navigableString)
    normalString = unicodedata.normalize("NFKD", string)
    return normalString.strip()

# Get list of labels
def getLabels(soup):
    retList = []
    labels = soup.find_all("td", class_ = "gridlabel", limit = 11)
    #print(labels)
    for label in labels:
        text = stringNormalize(label.string)
        retList.append(text)
    return retList
    




def main():
    print(getCourseDict("spring"))
    #soup = getSoup("https://www.buffalo.edu/class-schedule?switch=showcourses&semester=spring&division=UGRD&dept=AAS")
    #getDeptDict(soup)
    
if __name__ == "__main__":
    main()