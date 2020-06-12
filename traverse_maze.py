class Queue():
    def __init__(self):
        self.queue = []
    def push(self, value):
        self.queue.append(value)
    def pop(self):
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

# use a dictionary to look up opposite directions (used for backtracking)
opposite_directions = dict()
opposite_directions["n"] = "s"
opposite_directions["s"] = "n"
opposite_directions["e"] = "w"
opposite_directions["w"] = "e"

def traverse_maze(player):
    
    # use a graph to store visited rooms and their neighbors
    maze = Graph()

    # use a list of tuples to keep track of directions travelled and the room number at each step
    traversal_path = []

    # keep track of rooms already visited
    # each entry in rooms_to_visit will be a Room object
    visited_rooms = dict()
    rooms_to_visit = Stack()

    # add current room to rooms to visit
    new_room = player.current_room
    rooms_to_visit.push(new_room)

    while rooms_to_visit.size() > 0:

        # visit current room
        current_room = rooms_to_visit.pop()

        if current_room.id not in visited_rooms:

            # add room to dictionary
            visited_rooms[current_room.id] = current_room

            # add room to graph
            maze.add_vertex(new_room.id)

            # get any neighbors to the room to add them to the graph
            for exit_direction in current_room.get_exits():

                # get neighboring room
                adjoining_room = current_room.get_room_in_direction(exit_direction)

                # add a vertex from the current room to the neighboring room
                maze.add_edge(current_room.id, adjoining_room.id, exit_direction)
                
                # push all neighbors onto the stack to visit later
                rooms_to_visit.push(adjoining_room)

                # print(current_room.id, adjoining_room.id, exit_direction)
    
    print("done")

    for room_ID in visited_rooms:

        print(room_ID, maze.get_neighbors(room_ID))

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
    return traversal_path