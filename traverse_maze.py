class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):

        # create a new entry only if it doesn't exist yet
        if vertex_id not in self.vertices:

            self.vertices[vertex_id] = dict()
            self.vertices[vertex_id]["n"] = None
            self.vertices[vertex_id]["s"] = None
            self.vertices[vertex_id]["e"] = None
            self.vertices[vertex_id]["w"] = None

    def add_edge(self, vertex1_id, vertex2_id, direction):

        # add v2 if it doesn't exist yet
        if vertex2_id not in self.vertices:
            self.add_vertex(vertex2_id)

        # create an edge going from vertex1_id to vertex2_id
        self.vertices[vertex1_id][direction] = vertex2_id

        # store the edge going from vertex2_id to vertex1_id using the opposite direction
        reverse_direction = opposite_directions[direction]
        self.vertices[vertex2_id][reverse_direction] = vertex1_id
        
    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    # use breadth-first search to return a list of nodes to traverse to travel between two vertices
    # starting_vertex and destination_vertex are purposely left out of the list
    def find_shortest_sequence_of_nodes_between(self, starting_vertex, destination_vertex):

        # create a queue to hold vertices to traverse
        vertices_to_visit = Queue()

        # initialize queue with starting vertex
        vertices_to_visit.enqueue(starting_vertex)

        # use a dictionary to keep track of visited vertices and their path from the starting node
        paths_to_vertices = dict()
        paths_to_vertices[starting_vertex] = []

        # use a set to keep track of visited vertices
        vertices_already_visited = set()

        while vertices_to_visit.size() > 0:

            # get next vertex in line
            current_vertex = vertices_to_visit.dequeue()

            # process current vertex if it hasn't been visited yet
            if current_vertex not in vertices_already_visited:

                # mark current vertex as visited and store its path at the same time
                vertices_already_visited.add(current_vertex)

                # inspect all the neighbors of the current vertex
                # neighbor_data = [neighbor for neighbor in self.get_neighbors(current_vertex) if neighbor is not None]
                neighbor_data = self.get_neighbors(current_vertex)

                for direction in neighbor_data:

                    neighbor = neighbor_data[direction]

                    # there are entries for all four directions, even if the neighbor doesn't exist
                    # skip those neighbors if they don't exist
                    if neighbor is not None:

                        # if the target vertex is one of the neighbors, the search is done
                        # right now paths_to_vertices[current_vertex] only contains all the vertices up to and including the parent vertex
                        # to return the full path, add both the current vertex and the target vertex first.
                        if neighbor == destination_vertex:
                            final_path = paths_to_vertices[current_vertex][:]
                            final_path.append(current_vertex)
                            final_path.append(neighbor)
                            return final_path[1:-1]

                        # add all the other neighbors to the queue
                        vertices_to_visit.enqueue(neighbor)

                        # store a copy of the current path for each of the neighbors
                        # take the path leading to current_vertex and add current_vertex to it
                        # make a copy in order to not modify the original
                        copy_of_path_to_parent = paths_to_vertices[current_vertex][:]
                        copy_of_path_to_parent.append(current_vertex)

                        # store path in dictionary
                        paths_to_vertices[neighbor] = copy_of_path_to_parent
        
        # target not found
        print("Vertex", destination_vertex, "was not found.")
        return

# use a dictionary to look up opposite directions (used for backtracking)
opposite_directions = dict()
opposite_directions["n"] = "s"
opposite_directions["s"] = "n"
opposite_directions["e"] = "w"
opposite_directions["w"] = "e"

def traverse_maze(player):
    
    # use a graph to store visited rooms and their neighbors
    maze = Graph()

    # keep track of room numbers at each step
    # this will later be converted to a sequence of movements
    traversal_path = []

    # keep track of rooms already visited
    # each entry in rooms_to_visit will be a Room object
    visited_rooms = dict()
    rooms_to_visit = Stack()

    # add current room to rooms to visit
    new_room = player.current_room
    rooms_to_visit.push(new_room)

    # keep track of previous room in order to know when to backtrack
    previous_room = None

    while rooms_to_visit.size() > 0:

        # visit next room in stack
        new_room = rooms_to_visit.pop()

        # visit room only if this room has not been visited before
        if new_room.id not in visited_rooms:

            # check to see if the new room is directly accessible from the previous room
            # only do so if this is not the starting room
            if previous_room is not None:

                is_valid_direct_connection = False
                exit_to_use = None

                # examine all exits from the previous room for one that will lead to the new room
                for exit_direction in previous_room.get_exits():

                    adjoining_room = previous_room.get_room_in_direction(exit_direction)

                    if adjoining_room.id == new_room.id:
                        is_valid_direct_connection = True
                        exit_to_use = exit_direction
                
                # the new room is not directly reachable; need to search for a path to the target room
                if not is_valid_direct_connection:

                    # use breadth-first search to find a route (which may involve backtracking if at a dead end, or moving forward at the end of a loop)
                    path_between_rooms = maze.find_shortest_sequence_of_nodes_between(previous_room.id, new_room.id)
                    
                    # add that route to traversal_path
                    traversal_path = traversal_path + path_between_rooms                      

            # add room to dictionary
            visited_rooms[new_room.id] = new_room

            # add room to graph
            maze.add_vertex(new_room.id)

            # add room to traversal path
            traversal_path.append(new_room.id)

            # get any neighbors to the room to add them to the graph
            for exit_direction in new_room.get_exits():

                # get neighboring room
                adjoining_room = new_room.get_room_in_direction(exit_direction)

                # add a vertex from the current room to the neighboring room
                maze.add_edge(new_room.id, adjoining_room.id, exit_direction)
                
                # push all neighbors onto the stack to visit later
                rooms_to_visit.push(adjoining_room)

            # update previous room
            previous_room = new_room
    
    # convert traversal_path to a sequence of directions
    traversal_directions = []

    for i in range(0, len(traversal_path) - 1):

        previous_room = traversal_path[i]
        current_room = traversal_path[i + 1]

        neighbor_data = maze.get_neighbors(previous_room)

        for direction in neighbor_data:

            if neighbor_data[direction] == current_room:
                traversal_directions.append(direction)
        
    print(traversal_path)
    print(traversal_directions)
    print("done")

    return (traversal_path, traversal_directions)

    # for room_ID in visited_rooms:

    #     print(room_ID, maze.get_neighbors(room_ID))

    '''

        if new_room.id not in visited_rooms:

            # add room to graph
            maze.add_vertex(new_room.id)

            # check if new room is reachable from the current room
            # check only if this is not the starting room
            if len(traversal_path) > 0:
                current_room_data = traversal_path[-1]
                current_room = current_room_data[1]

                # print("the current room is", current_room.id)

                # get exits from current room to see if the new room is one room away
                exit_directions_from_current_room = current_room.get_exits()
                adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_current_room]
                adjoining_room_IDs = [room.id for room in adjoining_rooms]

                # if the new room is not directly accessible, need to backtrack to get there
                index_of_nth_from_last_room_in_traversal_path = -2

                # keep track of rooms backtracked from
                rooms_backtracked_through = []

                # set the previous room's direction to the current room' direction in preparation for potential backtracking
                previous_room_data = traversal_path[-1]
                # previous_room_direction = previous_room_data[0]

                # # compute the opposite direction (if it is not None for the first room)
                # if previous_room_direction is not None:
                #     opposite_of_previous_room_direction = opposite_directions[previous_room_direction]

                #     print("to leave the previous room, you would need to go", opposite_of_previous_room_direction)

                # print("Is", new_room.id, "accesible from", current_room.id, "?", new_room.id in adjoining_room_IDs)

                while new_room.id not in adjoining_room_IDs:
                    
                    # get next most recent room from traversal_path
                    current_room_data = traversal_path[index_of_nth_from_last_room_in_traversal_path]
                    current_room = current_room_data[1]

                    # get neighbors from this room
                    exit_directions_from_current_room = current_room.get_exits()
                    adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_current_room]
                    adjoining_room_IDs = [room.id for room in adjoining_rooms]

                    # add room to list of rooms backtracked through
                    # use the opposite direction of what was used to enter the previous room
                    previous_room_direction = previous_room_data[0]
                    rooms_backtracked_through.append((opposite_directions[previous_room_direction], current_room))

                    # update previous room info to that of the current room
                    previous_room_data = current_room_data

                    # update index to point to the room before the current one
                    index_of_nth_from_last_room_in_traversal_path -= 1

                # add the sequences of moves used for backtracking to the end of traversal_path
                traversal_path.extend(rooms_backtracked_through)

            # add room to set containing already-visited rooms
            visited_rooms.add(new_room.id)

            # add movement to traversal path
            traversal_path.append((direction_to_new_room, new_room))

            # get exits from new room
            exit_directions_from_room = new_room.get_exits()
            adjoining_rooms = [new_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
            adjoining_room_IDs = [room.id for room in adjoining_rooms]

            # represent exits from this room as tuples (direction, Room)
            # add each tuple to rooms_to_visit
            for exit_direction in exit_directions_from_room:
                rooms_to_visit.push((exit_direction, new_room.get_room_in_direction(exit_direction)))
    '''
    # return traversal_path