# import torch
# import cv2
import heapq
import heapq as heap
import os
# img = cv2.imread('UMBC_CAMPUS_MAP.jpg')
# cv2.imshow('UMBC_CAMPUS_MAP.jpg', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(cv2.__version__)
# print(torch.__version__)

# https://stackoverflow.com/questions/61942985/animate-a-plot-over-an-image-in-python

NAME = "UMBC TRACKER 0.1v"
CAMPUS_LIVING = ["Harbor", "Erikson", "Chesapeake", "Potomec", "Potapsco", "Susquehena", "Walker", "Hillside", "West Hill"]

TEXT_PROGRESSION = ["Name:", "Major", "CampusID", "On-Campus Living", "Classes", "Food", "Club", "Free Time"]


classDict = {"section": 1, "name": 2, "teacher": 3, "day": [1,2,3], "time": {"start": 1, "end": 2}, "location": 123}


studentList = []



# https://www.w3schools.com/python/python_classes.asp
class Student:
    def __init__(self, name):
        self.name = name
        self.major = ""
        self.campusID = []
        self.onCampus = "no"
        self.classes = []
        self.food = []
        self.club = []
        self.freeTime = []


class Map:
    def __init__(self):
        self.locations = set()
        self.paths = {}
        self.distance = {}

    def addLocation(self, location):
        self.locations.add(location)
        self.paths[location] = []

    def addPath(self, start, end, length):
        self.paths[start].append(end)
        self.paths[end].append(start)
        self.distance[start, end] = length
        self.distance[end, start] = length



def populate_map():
    try:
        file = open('locations.txt', 'r')
        line = file.readline()

        UMBC_MAP = Map()

        loop = 0
        while loop != 10:
            if loop >= 5:
                line = file.readline()
                UMBC_MAP.addLocation(line)

            elif loop >= 6:
                line = file.readline()
                print(line)
                info = line.split(":")
                UMBC_MAP.addPath(info[0], info[1], int(info[2]))
            loop += 1

        file.close()
        return UMBC_MAP



    except FileNotFoundError:
        print("Error: couldn't find locations.txt")
        return




def heuristic(map, a, b):
    return map.distance[a, b]
    # map.paths[a][b] = map.distance[a, b]
    # return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {location: float("inf") for location in map.locations}
    g_score[start] = 0
    f_score = {location: float('inf') for location in map.locations}
    f_score[start] = heuristic(map, start, goal)

    while open_list:
        current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in map.paths[current]:
            tentative_g_score = g_score[current] + map.distance[(current, neighbor)]

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(map,neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return None


def manualInput():
    name = input("What is the students name: ")
    major = input("What is the students major: ")
    id = input("What is the students ID: ")


    if input("Do you want a text file of your scredule? y/n: ") == "y":
        newFile = open(f"{id}.txt","w+")
        newFile.write(f"Name:\n\t{name}\n")
        newFile.close()


def textInput(textFile):
    # Try in stages name, on campus, classes, food times, clubs,
    try:
        file = open(textFile, 'r')
        line = file.readline()


        while line != EOFError:
            if TEXT_PROGRESSION[0] == line.strip():
                name = file.readline().strip()
                student = Student(name)
                studentList.append(student)

            elif TEXT_PROGRESSION[1] == line.strip():
                student.major = file.readline().strip()



        # Add stuff here to read it

        file.close()

    except FileNotFoundError:

        print("Invalid File: Please try a different file or import manually!")
        return


def getStudentSchedule():
    print("Would you like to import from a text file or import manually?\n\t1. Import\n\t2. Manual\n")
    typeInput = input().lower()

    if(typeInput == '1' or typeInput == 'import'):
        textFile = input("Please enter the name of the text file: ")
        textInput(textFile)


    elif (typeInput == '2' or typeInput == 'manual'):
        manualInput()


def checkInstruction():
    file = open("commands.txt", 'r')
    print(file.read())
    file.close()

    # Takes in a command
    cmd = input().lower()


    if(cmd == "1" or cmd == "imput" or cmd == "input student schedule"):
        getStudentSchedule()
        return True

    elif(cmd == "2" or cmd == "choose" or cmd == "choose trackee"):
        for i in range(0, len(studentList)):
            print(studentList[i].name)
        print("implement soon with objects")
        return True

    elif(cmd == "3" or cmd == "open" or cmd == "open map"):
        print("implement soon with map and animation")
        return True

    elif(cmd == "4" or cmd == "run" or cmd == "run time simulation"):
        print("add this to the thing soon")
        return True

    elif(cmd == "5" or cmd == "ask ai" or cmd == "ask ai questions"):
        print("figure out how to get AI to read the full map as well as text file for object or about umbc and food options or clubs etc")
        return True

    elif(cmd == "6" or cmd == "quit" or cmd == "q"):
        print(f"Thank you for using {NAME}")
        return False
    # Maybe make this more easy with using del __filename__ instead by splitting?
    elif(cmd == "7" or cmd == "del" or cmd == "delete file"):
        # maybe use glob to find easier
        # https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/
        os.listdir()
        fileName = input("Please enter the name of the file you want to delete: ")
        file_path = f'{fileName}.txt'
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")

        return True

    elif cmd == "8" or cmd == "search":
        start = input("What is the start location: ")
        goal = input("What is the end location: ")
        umbc_map = populate_map()
        path = a_star_search(umbc_map, start, goal)
        print("Path found:", path)


    else:
        print("Invalid Command! Please try again!")
        return True

def main():
    print("Welcome to UMBC Tracker 0.1")

    # Maybe fix later with better code
    instruction = checkInstruction()
    while instruction == True:
        instruction = checkInstruction()


if __name__ == "__main__":
    main()


