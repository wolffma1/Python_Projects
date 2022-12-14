##############################################################################
#
#    PYTHON MAPS APPLICATION - Marcus Wolff
#
#    Algorithm
#        
#    Initialize variables
#    Call open_file() function to open a file for reading
#    Call read_file() function to read the file; obtain list of tuples
#    Call adjacency_matrix() function; obtain places list and adjacency matrix
#    Call make_objects() function; obtain dictionaries of places by name and id
#    Prompt user to input starting location
#    Enter main mapping loop
#        Print banner
#        Error check starting location
#        Enter destination loop
#            Prompt user to enter destinations, error checking in the process
#        Loop through destinations; update total path and distance
#        Print total path and distance if path exists
#        Prepare for next repetition; reinitialize variables and print banner
#        Prompt user for new starting location; quit if user enters "q"
#    Print closing message
#    Close file
#    END
#
##############################################################################

import csv, place

def apsp(g):
    '''All-Pairs Shortest Paths using the Floyd-Warshall algorithm.'''

    INFINITE = 2**63-1  # a really big number (the biggest int for a 64-bit machine)

    # Initialize paths with paths for adjacent nodes
    paths = [[0 for j in range(len(g))] for i in range(len(g))]
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] != 0: 
                paths[i][j] = [i,j] # if two places are already adjacent then assign an initial path to them
            elif i != j:  # i == j means this is the same place so distance is zero
                g[i][j] = INFINITE # replacing zero by an "infinite" value
                # zero earlier meant that two places are not connected, now it will mean that they are not connected
                # initially, meaning that are "very-very" far ("virtually", for the sake of initialization)


    #apsp computation - floyd-warshall algorithm
    for k in range(len(g)):  # (for each) vertex k, to compare if i--k + k--j is shorter than i--j computed so far
        for i in range(len(g)): # (for each) vertex i of our interest
            for j in range(len(g)): # (for each) vertex j, to get the computed distance so far (between i and j)
                if g[i][j] > g[i][k] + g[k][j]: # determining if there is a shorter path (as per the above comment)
                    g[i][j] = g[i][k] + g[k][j] # updating the path-length value if there is a shorter path

                    # updating the path itself if there is a shorter path
                    paths[i][j] = paths[i][k][:]
                    paths[i][j].extend(paths[k][j][1:])

    # if a pair of places are still at infinite distance,
    # then assign them 0, to declare that they are not connected 
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] == INFINITE: 
                g[i][j] = 0

    return g,paths

def open_file():
    '''This function takes no parameters, and simply opens a file for reading,
    returning a file pointer.'''
    
    # Use try-except to ensure a valid file name is entered
    while True:
        
        try:
            file_name_str = input("Enter the file name: ")
            fp = open(file_name_str, "r")
            break
        
        except FileNotFoundError:
            print("\nFile not found.! Try again.")
    
    return fp
            
def read_file(fp):
    '''This function takes the file pointer as a parameter and reads through
    the file, returning a list of tuples whose members are a place, another
    place, and the distance between them.'''
    
    reader = csv.reader(fp)
    next(reader, None)
    master_list = []
    
    # Read through the file, changing the distances to integers
    for line in reader:
        
        # Append one tuple to master list per line of the file
        master_list.append((line[0], line[1], int(line[2])))
    
    return master_list

def adjacency_matrix(L):
    '''This function takes one parameter, the list of tuples of places and 
    distances between them, and returns a list of places in this list of 
    tuples, as well an adjacency matrix for distances between places, denoted
    as g.'''
    
    places_set = set()
    g = []
    zeros_list = []
    
    # Create list of places using a set for uniqueness requirement
    for tup in L:
        
        for index,element in enumerate(tup):
            
            # Add the tuple element only if it is at index 0 or 1 (the places)
            if (index == 0) or (index == 1):
                places_set.add(element)
    
    # Now create list of that set and sort it
    places_lst = sorted(list(places_set))
    
    # Create adjacency matrix g
    # First create list of zeros of proper length
    for i in range(len(places_lst)):
        
        zeros_list.append(0)
        
    # Next create the list of lists, g
    for i in range(len(places_lst)):
        
        # Each sublist must be DEEP copy of the zeros list, so that a change
        # to a sublist does not affect the other sublists in filling g
        g.append(zeros_list[:])
        
    # Add distances to g
    for tup in L:
        
        # Find indices of places in tuple
        first_index_int = places_lst.index(tup[0])
        second_index_int = places_lst.index(tup[1])
        distance_int = tup[2]
        
        # Fill matrix g with distance at the proper two locations
        g[first_index_int][second_index_int] = distance_int
        g[second_index_int][first_index_int] = distance_int
    
    return places_lst, g
    
    
def make_objects(places_lst,g):
    '''This function takes the list of places and the adjacency matrix as
    parameters, and returns two dictionaries of Place objects from the places
    list. One dictionary is indexed by name, and the other by id.'''
    
    # Call apsp() function to get shortest distances and paths between places
    g, paths = apsp(g)
    
    # Initialize dictionaries
    dict_by_name = {}
    dict_by_id = {}
    
    # Create dictionaries of Place objects
    for i, place_name in enumerate(places_lst):
        
        # Initialize Place object with its name (place_name) and index/id (i)
        a_place = place.Place(place_name, i)
        
        # Set Place's distance
        a_place.set_distances(g)
        
        # Set Place's path
        a_place.set_paths(paths)
        
        # Properly add Place objects to each dictionary
        dict_by_name[place_name] = a_place
        dict_by_id[i] = a_place
        
    return dict_by_name, dict_by_id

def main():
    '''The main() function is the user's interface with the program.'''
    
    # Initialize variables
    BANNER = '\nBegin the search!'
    start_str = ""
    next_str = ""
    last_str = ""
    route_lst = []
    path_lst = []
    distance_int = 0
    is_path_bool = True
    
    # Open and read the file to obtain place information list of tuples
    fp = open_file()
    L = read_file(fp)
    
    # Obtain places list adjacency matrix
    places_lst, g = adjacency_matrix(L)
    
    # Obtain dictionaries of places
    name_dict_of_places, id_dict_of_places = make_objects(places_lst, g)
    
    print(BANNER)
    
    # Initialize starting location
    start_str = input("Enter starting place, enter 'q' to quit: ")
    
    # Enter loop to find a route
    while start_str != "q":
        
        # Error checking the starting point entered
        while start_str not in places_lst:
            print("This place is not in the list!")
            start_str = input("Enter starting place, enter 'q' to quit: ")
        
        # Add start location to path list
        path_lst.append(start_str)
        
        # Loop to input destinations
        while next_str != "end":
            
            next_str = input('Enter next destination, enter "end" to exit: ')
            
            # Error checking the destination entered
            while (next_str != "end") and ((next_str not in places_lst) or \
                (next_str == last_str)):
                print("This destination is not valid or is the same as the previous destination!")
                next_str = input('Enter next destination, enter "end" to exit: ')
            
            # Add destination to the route
            if next_str != "end":
                route_lst.append(next_str)
                
                # Prepare current location as last location for next iteration
                last_str = next_str
            
            else:
                pass
        
        # Initialize last location as the start for iterating through route
        last_place_obj = name_dict_of_places[start_str]
        
        # Loop through route list to obtain total path and distance of route
        for location in route_lst:
            
            next_place_obj = name_dict_of_places[location]
            
            # Obtain name and id of next location, and name of last location
            last_name = last_place_obj.get_name()
            next_name = next_place_obj.get_name()
            next_id = next_place_obj.get_index()
            
            # Add to path if the sub path exists; if not, break loop
            sub_path = last_place_obj.get_path(next_id)
            if sub_path == 0:
                
                print("places {} and {} are not connected.".format(last_name, \
                    next_name))
                is_path_bool = False
            
            # Otherwise, add to the total path
            else:
                
                # Ensure end of last sub path is not double counted
                if path_lst:
                    del path_lst[-1]
                
                # Must extract destinations from sub path sublists
                # Sub path contains ids; index the id dictionary to get names
                for node in sub_path:
                    path_lst.append(id_dict_of_places[node].get_name())
                    
                # Add to distance only if sub path exists
                distance_int += last_place_obj.get_distance(next_id)
            
            # Prepare the starting destination for next iteration
            last_place_obj = next_place_obj
        
        # If path exists, print it
        if is_path_bool:
            
            print("Your route is:")
            
            for node in path_lst:
                print("     {}".format(node))
            
            # Print distance
            print("Total distance =", distance_int)
        
        # Prepate for next repetition
        print(BANNER)
        start_str = input("Enter starting place, enter 'q' to quit: ")
        next_str = ""
        route_lst = []
        path_lst = []
        distance_int = 0
        is_path_bool = True
        
    # Print closing message and close the file
    print('Thanks for using the software')
    fp.close()
    
if __name__=='__main__':
    main()

