import math

import numpy as np
import heapq

import tkinter as tk
from tkinter import ttk
from tkinter import *

# Calls the file that makes the map
import map_maker as displayMap
import gui_file as GUI

# https://medium.com/@siddhanuka/demystifying-gps-2a034461644a
# Comment stuff and explain

"""Find a way to have a gui print locations based on coords and draw lines based on distance and connections
"""

# Make this for example
symbols = {"HBR_H": "Harbor Hall"}
degree_sign = u'\N{DEGREE SIGN}'
xyz = '"'
lb = '{'
rb = '}'


MAIN_LOCATIONS = ["Harbor Hall", "Chesapeake Hall", "Potomac Hall",
                  "Patapsco Hall", "Susquehanna Hall", "Library",
                  "The Commons", "Fine Arts", "Engineering",
                  "ITE", "Sherman Hall", "Sondheim Hall",
                  "RAC", "Math & Psych", "Meyerhoff Hall",
                  "Chemistry Lecture Hall", "Lecture Hall One", "Bioscience",
                  "Administration Building", "University Center", "Performing Arts & Humanities",
                  "Interdisciplinary Life Sciences Building", "Physics Building", "Public Policy Building",
                  "The Center of Well-Being", "True Grits", "Erikson Hall",
                  "Hillside Apartments", "West Hills Community Center", "Walker Apartments"]
# Only includes main buildings

# This class hold all the data for each location
class Location:
    # Default Constructor, initializes all variables required
    def __init__(self, name: str, lat: float, long: float, f_name: str):
        self.name = name
        self.lat = lat
        self.long = long
        self.full_name = f_name
        # Connections is a dictionary that contains all the neighboring locations
        self.connections = {}  # inputted data looks like: {location: dist}, {location2: dist2}...

    # Function to display all the locations data in a readable fashion
    def display(self):
        print(f"{self.lat}, {self.long} {lb}{self.name}:\t, ", end='')
        for i in range(len(self.connections)):
            keys = list(self.connections.keys())
            print(f"{keys[i]}, ", end='')
        print(f"{rb} <default-dot>")
        return

        print(f"Location Name: {self.name} \t Coords: {self.lat}{degree_sign}N  {self.long}{degree_sign}W")
        print(self.full_name)
        # Maybe wont be used, this only works if I can figure out a way to convert to cords
        print("\tX AND Y:", self.get_xy())
        for i in self.connections:
            dist = self.connections[i]
            print(f"\t {i}: {dist}m")
        print("\n\n")

    # Returns a list containing the latitude and longitude of the location
    def get_coordinates(self):
        return [self.lat, self.long]

    # Returns coordinates for the location to be used on a graph
    """THIS MAY OR MAY NOT BE USED"""
    def get_xy(self):
        radius_earth = 3371000
        x = radius_earth * np.cos(self.lat) * np.cos(self.long)
        y = radius_earth * np.cos(self.lat) * np.sin(self.long)
        return x, y

# This class contains all the functions and detials of the map the
class Map:
    # Default constuctor
    def __init__(self):
        # Adjacency list contains all the list of locations
        self.adjacency_list = {}  # {"location name": location.obj, ...}
        # Populates the map with the locations and connections using text files
        self.add_locations()
        self.add_connections()

    # This fucntion returns the distance between two locations using their coordinates
    def heuristic(self, loc1: Location, loc2: Location):
        # returns the distance calculated by comparing long and lat
        distance = self.distanceInBetweenPoints(loc1, loc2)

        print(f"{loc1.name} to {loc2.name}:")
        print(f"\t\t {loc1.get_coordinates()} to {loc2.get_coordinates()}")
        print(f"\t\t\t Distance is: {distance}\n")
        return distance

    # Converts degrees to radians
    def degreeToRad(self, degree: float):
        return degree * np.pi / 180

    def distanceInBetweenPoints(self, loc1: Location, loc2: Location):
        earthRad = 6371
        # makes the output dist in meters
        earthRad *= 1000

        # Turns the coordinates to radians for calculation
        dLat = self.degreeToRad(loc2.lat - loc1.lat)
        dLon = self.degreeToRad(loc2.long - loc1.long)
        lat1 = self.degreeToRad(loc1.lat)
        lat2 = self.degreeToRad(loc2.lat)

        # Calculates part of the distance formula needed
        a = np.sin(dLat/2) * np.sin(dLat/2) + np.sin(dLon/2) * np.sin(dLon/2) * np.cos(lat1) * np.cos(lat2)
        y_div_x = np.sqrt(a) / np.sqrt(1-a)
        c = 2 * np.arctan(y_div_x)

        # Returns the distance between the two coordinates
        return earthRad * c

    # This function adds locations to the graph using a text file
    def add_locations(self):
        # Tries to open the file
        try:
            file = open('campus.txt', 'r')
            cont = True
            while cont:
                # Grabs a line from the textfile
                lines = file.readline().split(',')

                # Strips all the lines of extra whitespace
                for i in range(len(lines)):
                    lines[i].strip()

                # Makes sure the location is validly assigned
                if len(lines) == 4:
                    # Checks to see if it already exits in the map
                    if lines[0] not in self.adjacency_list:
                        # Creates a new location object using the variables from the line
                        loco = Location(lines[0].strip(), float(lines[1]), float(lines[2]), lines[3].strip())

                        # Adds the locations name to the list and the value is the location variable for quick access
                        # Accessed by shortened name and value is location object
                        self.adjacency_list.update({f"{lines[0].strip()}": loco})
                # If there arent enough lines IE, one of the lines is improper or end of file
                elif len(lines) != 4:
                    cont = False
            file.close()

        # If the file cannot be found output the error message
        except FileNotFoundError:
            print("Error: couldn't find campus.txt")
            return

    def add_connections(self):
        # Tries to add connections to each location using textfile
        try:
            file = open('connections.txt', 'r')
            cont = True
            while cont:

                lines = file.readline().strip().split(',')
                for i in range(len(lines)):
                    # checks if the main location exists and that its not adding to itself
                    if lines[0].strip() in self.adjacency_list and i != 0:
                        # If the connected location is a valid location(in the list) and it isnt
                        # already in the connected locations connections
                        if lines[i].strip() in self.adjacency_list and lines[i].strip() not in self.adjacency_list[lines[0].strip()].connections:
                            # Grabs the locations from the dictionary using name as key
                            loc1 = self.adjacency_list[lines[0].strip()]
                            loc2 = self.adjacency_list[lines[i].strip()]

                            # Calculates the distance between the locations
                            distance = self.heuristic(loc1, loc2)

                            # Adds the opposite location to each of both locations connected list as well as the distance
                            loc1.connections.update({lines[i].strip(): distance})
                            loc2.connections.update({lines[0].strip(): distance})

                    # If the # of lines is 1 then end the loop (reached end of file)
                    elif len(lines) == 1:
                        cont = False
            file.close()

        # Outputs file not found error message if file isnt found
        except FileNotFoundError:
            print("Error: couldn't find connections.txt")
            return

    # This function shows the details of each location on the map
    def show_details(self):
        for i in self.adjacency_list:
            self.adjacency_list[i].display()

    # This function uses dijkstras greedy path algorithm to find the shortest distance from one umbc location to another
    def path_search(self, start: str, end: str, ):
        # This line makes a dictionary using each locations name and their distance
        # initializes all nodes distances to infinite to start
        distances = {node: float('inf') for node in self.adjacency_list}
        # Sets the start distance to 0 as that is the node we are currently on
        distances[start] = 0

        # Appends the start node and distance to a heap
        heap = [(0, start)]
        # Creates a dictionary to be used to keep track of the path
        previous_nodes = {}
        visited = set()

        # While the heap isnt empty t checks to see if the neighbors have a good path towards the end
        while heap:
            # Pops the node and weight we currently have
            (current_dist, current_node) = heapq.heappop(heap)
            # If the node has already been visited continue, otherwise add it to the visited list
            if current_node in visited:
                continue
            visited.add(current_node)

            # Helps show whats happening
            # print(self.adjacency_list[current_node].connections.items())
            # This line retrieves the connected nodes and their weights (distance) to be used to determine a good path
            for neighbor, weight in self.adjacency_list[current_node].connections.items():
                # Current distance is the total current distance so far
                tentative_dist = current_dist + weight

                # If the tentative distance isnt infinite or is less than the
                # distance to the neighbor update the distances
                if tentative_dist < distances[neighbor]:
                    # Updates the distance to the new shorter distance
                    distances[neighbor] = tentative_dist

                    # Set the previous nodes of the neighbor to the current node
                    previous_nodes[neighbor] = current_node

                    # Attempts to push the new heap with the new distance and the neighbors node to continue along path
                    heapq.heappush(heap, (tentative_dist, neighbor))
        # If the end isnt in the previous nodes path that means there is no path to it
        if end not in previous_nodes:
            return None, None

        #
        path = []
        current_node = end
        while current_node != start:
            # Adds the nodes from end to start to the path list
            path.insert(0, self.adjacency_list[current_node].full_name)
            # Traverses up the list by finding the previous nodes to the current node
            current_node = previous_nodes[current_node]
        # Inserts the start at the end for better display
        path.insert(0, self.adjacency_list[start].full_name)

        return distances[end], path







def main():
    print("Welcome to UMBC Map Search:")
    # Generates and populates map
    mapX = Map()
    # Shows all the locations and connections on the map
    mapX.show_details()


    print("\nhttps://www.mapcustomizer.com/# \n\n")

    # This for loop tests some of the directions based off the maps locations
    for i in range(7):
        if i == 0:
            start = "TG_MB"
            end = "SHERM_MB"
            # start = "CWB_MB"
            # end = "TG_MB"
        elif i == 1:
            start = "HH_MB"
            end = "PTAP_MB"
        elif i == 2:
            start = "PH_MB"
            end = "SH_MB"
        elif i == 3:
            start = "CH_MB"
            end = "SH_MB"
        elif i == 4:
            start = "CH_MB"
            end = "HH_EAST-SOUTH_ENTRANCE"
        elif i == 5:
            start = "AROW_CIRCLE_ENTRANCE"
            end = "HH_MB"
            # end = "MATH_PSYCH_MB"
        elif i == 6:
            start = "ITE_MB"
            end = "MATH_PSYCH_MB"

        shortest_distance, path = mapX.path_search(start, end)
        print(mapX.adjacency_list[start].full_name, "to", mapX.adjacency_list[end].full_name)
        print("Path:", path)
        print(f"Shortest Distance: {shortest_distance}")
        print(shortest_distance / 82, f" minutes to walk from {start} to {end}\n")
    #     Average walking speed is 82m/s

    return 0
    # Attempts to make GUI
    # https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/

    root2 = Tk()
    root2.title("Welcome to UMBC Tracker")
    root2.geometry('350x350')
    lbl = Label(root2, text = "Would you like to see the map?")
    lbl.grid()

    # frame = Frame(root)
    # frame.pack()
    #
    # bottomframe = Frame(root)
    # bottomframe.pack(side=LEFT)
    #
    # redbutton = Button(frame, text="Red", fg="red")
    # redbutton.pack(side=LEFT)
    #
    # greenbutton = Button(frame, text="Brown", fg="brown")
    # greenbutton.pack(side=LEFT)
    #
    # bluebutton = Button(frame, text="Blue", fg="blue")
    # bluebutton.pack(side=LEFT)
    #
    # blackbutton = Button(bottomframe, text="Black", fg="black")
    # blackbutton.pack(side=BOTTOM)




    start_txt = Entry(root2, width=10)
    start_txt.grid(column=0,  row=1)


    def clicked():
            displayMap.showMap()
            lbl.configure(text = "Displaying Map...")

    btn = Button(root2, text = "Click me", fg = "red", command = clicked)


    btn.grid(column=1, row=0)

    root2.mainloop()




    def sel():
        selection = "You selected the option " + str(var.get())
        label.config(text=selection)


    # Function to be called when a radio button in the first set is selected
    def on_select_1():
        selected_option = var1.get()
        print("Selected option from List 1:", selected_option)

    # Function to be called when a radio button in the second set is selected
    def on_select_2():
        selected_option = var2.get()
        print("Selected option from List 2:", selected_option)

    # Create the main window
    root = tk.Tk()
    root.title("Two Sets of Radio Buttons with Scrollbars")

    # Frame for the first set of radio buttons
    frame1 = tk.Frame(root)
    frame1.pack(pady=10, padx=10, side=tk.LEFT)

    label1 = tk.Label(frame1, text="Select from List 1")
    label1.pack()

    # Scrollbar for the first list
    scrollbar1 = tk.Scrollbar(frame1, orient="vertical")
    scrollbar1.pack(side="right", fill="y")

    # Create a canvas to contain the radio buttons and attach scrollbar
    canvas1 = tk.Canvas(frame1, yscrollcommand=scrollbar1.set)
    canvas1.pack(side="left", fill="both", expand=True)

    scrollbar1.config(command=canvas1.yview)

    # Frame inside the canvas to hold the radio buttons
    radio_frame1 = tk.Frame(canvas1)
    canvas1.create_window((0, 0), window=radio_frame1, anchor="nw")

    # Add radio buttons to the first frame
    var1 = tk.StringVar()
    options = [f"Option {i}" for i in range(1, 51)]  # Example options
    for option in options:
        rb = ttk.Radiobutton(radio_frame1, text=option, variable=var1, value=option, command=on_select_1)
        rb.pack(anchor='w')

    # Function to update scroll region of the canvas
    def update_scroll_region_1(event):
        canvas1.configure(scrollregion=canvas1.bbox("all"))

    radio_frame1.bind("<Configure>", update_scroll_region_1)

    # Frame for the second set of radio buttons
    frame2 = tk.Frame(root)
    frame2.pack(pady=10, padx=10, side=tk.RIGHT)

    label2 = tk.Label(frame2, text="Select from List 2")
    label2.pack()

    # Scrollbar for the second list
    scrollbar2 = tk.Scrollbar(frame2, orient="vertical")
    scrollbar2.pack(side="right", fill="y")

    # Create a canvas to contain the radio buttons and attach scrollbar
    canvas2 = tk.Canvas(frame2, yscrollcommand=scrollbar2.set)
    canvas2.pack(side="left", fill="both", expand=True)

    """DO THIS IS A WAY WHERE ITS ALL IN ONE FRAME AND CANVAS"""

    scrollbar2.config(command=canvas2.yview)

    # Frame inside the canvas to hold the radio buttons
    radio_frame2 = tk.Frame(canvas2)
    canvas2.create_window((0, 0), window=radio_frame2, anchor="nw")

    # Add radio buttons to the second frame
    var2 = tk.StringVar()
    for option in options:
        rb = ttk.Radiobutton(radio_frame2, text=option, variable=var2, value=option, command=on_select_2)
        rb.pack(anchor='w')

    # Function to update scroll region of the canvas
    def update_scroll_region_2(event):
        canvas2.configure(scrollregion=canvas2.bbox("all"))

    radio_frame2.bind("<Configure>", update_scroll_region_2)
    checkArea = Button()



    # Run the main loop
    root.mainloop()

if __name__ == '__main__':
    main()
