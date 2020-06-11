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

    visited_rooms = set()

    current_room = player.current_room

    print("now in room", current_room.id)
    
    exit_directions_from_room = current_room.get_exits()
    adjoining_rooms = [current_room.get_room_in_direction(direction) for direction in exit_directions_from_room]
    adjoining_room_IDs = [room.id for room in adjoining_rooms]

    print("exits:", exit_directions_from_room)
    print("adjoining room IDs:", adjoining_room_IDs)

    return traversal_path