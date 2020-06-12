from room import Room
from player import Player
from world import World

from traverse_maze import traverse_maze

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path_data = traverse_maze(player)

# return just the directions for traversal_path
# remove the first placeholder direction used to get to the starting room
traversal_path = [room[0] for room in traversal_path_data if room[0] is not None]

# get map name from map file
parts_without_txt = map_file.split(".")
parts_without_slash = parts_without_txt[0].split("/")
map_name = parts_without_slash[1]

with open("traversals/" + map_name + "_traversal.txt", "w") as traversal_record:
    
    for room in traversal_path_data:

        direction = room[0] or "None"
        room_ID = room[1].id

        traversal_record.write(direction + " " + str(room_ID) + "\n")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
