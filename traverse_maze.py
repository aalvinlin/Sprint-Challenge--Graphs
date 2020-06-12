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

def traverse_maze(player):
    
    # use a list of tuples to keep track of directions travelled and the room number at each step
    traversal_path = []

    # keep track of rooms already visited
    visited_rooms = set()
    rooms_to_visit = Stack()

    # keep track of rooms already in the queue so they are not added over and over again
    # rooms_in_queue = set()

    # add current room to rooms to visit
    new_room = player.current_room
    rooms_to_visit.push((None, new_room))

    # keep track of previous room for backtracking
    previous_room = None

    print("starting room is", new_room)

    steps = 0

    # while rooms_to_visit.size() > 0:

    #     # get ID of next room to visit
    #     next_unvisited_room = rooms_to_visit.pop()

    #     # # determine if the next room is reachable from the current location
    #     # # backtrack until able to do so (ignore this step if this is the starting room)
    #     # exit_directions_from_room = current_room.get_exits()
    #     # adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
    #     # adjoining_room_IDs = [room.id for room in adjoining_rooms]

    #     # # use traversal_path to backtrack
    #     # while steps > 0 and next_unvisited_room.id not in adjoining_room_IDs:

    #     if next_unvisited_room.id not in adjoining_room_IDs:
    #         print(next_unvisited_room.id, "is unreachable from", )


        
    #     if next_unvisited_room.id not in visited_rooms:

    #         # print("current room is", current_room.id)
    #         # print("  visited:", visited_rooms)
    #         # print("  rooms_to_visit:", rooms_to_visit.queue)

    #         # add room to set containing already-visited rooms
    #         visited_rooms.add(next_unvisited_room.id)

    #         steps += 1

    #         exit_directions_from_room = next_unvisited_room.get_exits()
    #         adjoining_rooms = [next_unvisited_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
    #         adjoining_room_IDs = [room.id for room in adjoining_rooms]

    #         # print("exits:", exit_directions_from_room)
    #         # print("adjoining room IDs:", adjoining_room_IDs)

    #         for adjoining_room in adjoining_rooms:

    #             # if adjoining_room not in visited_rooms:
    #             rooms_to_visit.push(adjoining_room)
    #             # print("added", adjoining_room.id, "to the queue")

    #         # print(len(visited_rooms), "rooms left")

        
    #     # check if the next ID in the queue is an exit from the current room.
    #     # while it is not reachable, backtrack via traversal_path until the requested room is directly reachable.

    # Standard, working depth-first search
    
    while rooms_to_visit.size() > 0:

        # visit current room and update previous room
        previous_room = new_room
        new_room_data = rooms_to_visit.pop()
        direction_to_new_room, new_room = new_room_data

        # print("🛑new room!", new_room.id)

        # print("data contains", new_room_data, new_room_data[0])
        # direction_to_new_room, new_room_ID

        if new_room.id not in visited_rooms:

            print("new room is", new_room.id)
            # print("  visited:", visited_rooms)
            # print("  rooms_to_visit:", rooms_to_visit.queue)

            # check if new room is reachable from the current room
            # check only if this is not the starting room
            if len(traversal_path) > 0:
                current_room_data = traversal_path[-1]
                current_room = current_room_data[1]

                exit_directions_from_current_room = current_room.get_exits()
                adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_current_room]
                adjoining_room_IDs = [room.id for room in adjoining_rooms]

                if new_room.id in adjoining_room_IDs:
                    print("new room", new_room.id, "is accessible from", current_room.id, ".")
                else:
                    print("need to teleport to get here.")

            # add room to set containing already-visited rooms
            visited_rooms.add(new_room.id)

            # add movement to traversal path
            traversal_path.append((direction_to_new_room, new_room))

            # print("path so far:")
            # print("  ", traversal_path)

            # print("previous room was", previous_room.id)
            # print("current room is", new_room.id, "\n")

            steps += 1

            exit_directions_from_room = new_room.get_exits()
            adjoining_rooms = [new_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
            adjoining_room_IDs = [room.id for room in adjoining_rooms]

            adjoining_rooms_data = []

            # create a list of tuples (direction, Room) to represent exits from this room
            for exit_direction in exit_directions_from_room:
                adjoining_rooms_data.append((exit_direction, new_room.get_room_in_direction(exit_direction)))

            # store the direction to be used in order to enter the adjoining room


            # print("exits:", exit_directions_from_room)
            # print("adjoining room IDs:", adjoining_room_IDs)

            for adjoining_room_info in adjoining_rooms_data:

                direction = adjoining_room_info[0]
                adjoining_room_ID = adjoining_room_info[1].id

                # if adjoining_room not in visited_rooms:
                rooms_to_visit.push(adjoining_room_info)
                # print("added", adjoining_room_ID, "to the queue")

            # print(len(visited_rooms), "rooms left")

        
        # check if the next ID in the queue is an exit from the current room.
        # while it is not reachable, backtrack via traversal_path until the requested room is directly reachable.
    
    print(steps, "steps taken.")

    return traversal_path