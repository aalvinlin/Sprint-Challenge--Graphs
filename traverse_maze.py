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
    
    # use a dictionary to look up opposite directions (used for backtracking)
    opposite_directions = dict()
    opposite_directions["n"] = "s"
    opposite_directions["s"] = "n"
    opposite_directions["e"] = "w"
    opposite_directions["w"] = "e"

    # use a list of tuples to keep track of directions travelled and the room number at each step
    traversal_path = []

    # keep track of rooms already visited
    visited_rooms = set()
    rooms_to_visit = Stack()

    # add current room to rooms to visit
    new_room = player.current_room
    rooms_to_visit.push((None, new_room))

    # keep track of previous room for backtracking
    previous_room = None

    while rooms_to_visit.size() > 0:

        # visit current room
        new_room_data = rooms_to_visit.pop()
        direction_to_new_room, new_room = new_room_data

        if new_room.id not in visited_rooms:

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

    return traversal_path