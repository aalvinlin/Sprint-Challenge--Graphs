from ast import literal_eval

maps = ["test_line", "test_cross", "test_loop", "test_loop_fork", "main_maze"]
# maps = ["test_line"]

# create first part of HTML document
def make_html_header(map):

    html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '    <title>' + map + '</title>\n'
    html += '    <link rel="stylesheet" src="maze.css" />\n'
    html += '</head>\n<body>'

    return html

# create final part of HTML document
def make_html_footer():

    html = '</body>\n</html>'

    return html

# create HTML version of map
for map in maps:
    map_file = "maps/" + map + ".txt"

    # evaluate contents of text file as a Python dictionary of rooms
    room_graph = literal_eval(open(map_file, "r").read())

    # determine dimensions of grid
    largest_row = 0
    largest_col = 0

    for room_ID in room_graph:
        room_data = room_graph[room_ID]

        room_row, room_col = room_data[0]

        if room_row > largest_row:
            largest_row = room_row
        
        if room_col > largest_col:
            largest_col = room_col

    print(map, largest_row, largest_col)

    # create an array to hold the map
    maze = []
    row = [[]] * (largest_col + 1)

    for _ in range(0, largest_row + 1):
        maze.append(row)
    
    # add all rooms to maze
    for room_ID in room_graph:
        room_data = room_graph[room_ID]

        room_row, room_col = room_data[0]

        # maze[room_row][room_col] = room_data

    print(maze)

    # with open("maps/" + map + ".html", "w") as html:

    #     html.write(make_html_header(map))
    #     html.write("test")
    #     html.write(make_html_footer())
        
    #     print("Created " + map + ".html")