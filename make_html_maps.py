maps = ["test_line", "test_cross", "test_loop", "test_loop_fork", "main_maze"]

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

    with open("maps/" + map + ".html", "w") as html:

        html.write(make_html_header(map))
        html.write("test")
        html.write(make_html_footer())
        
        print("Created " + map + ".html")