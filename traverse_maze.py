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

def traverse_maze(player):
    
    # use a list of tuples to keep track of directions travelled and the room number at each step
    traversal_path = []

    # keep track of rooms already visited
    visited_rooms = set()
    rooms_to_visit = Queue()

    # keep track of rooms already in the queue so they are not added over and over again
    rooms_in_queue = set()

    # add current room to rooms to visit
    current_room = player.current_room
    rooms_to_visit.enqueue(current_room)

    print("starting room is", current_room)

    steps = 0

    while rooms_to_visit.size() > 0:

        # visit current room
        current_room = rooms_to_visit.dequeue()

        if current_room.id not in visited_rooms:

            # print("current room is", current_room.id)
            # print("  visited:", visited_rooms)
            # print("  rooms_to_visit:", rooms_to_visit.queue)

            # add room to set containing already-visited rooms
            visited_rooms.add(current_room.id)

            steps += 1

            exit_directions_from_room = current_room.get_exits()
            adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
            adjoining_room_IDs = [room.id for room in adjoining_rooms]

            # print("exits:", exit_directions_from_room)
            # print("adjoining room IDs:", adjoining_room_IDs)

            for adjoining_room in adjoining_rooms:

                # if adjoining_room not in visited_rooms:
                rooms_to_visit.enqueue(adjoining_room)
                # print("added", adjoining_room.id, "to the queue")

            # print(len(visited_rooms), "rooms left")
        
    print(steps, "steps taken.")

    return traversal_path