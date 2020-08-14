from room import Room
from player import Player
from world import World
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# *********************************************************** #
# *********************************************************** #

# ************** functions ***************


def reverseDir(dir):
    if dir == 'n':
        opposite = 's'
    elif dir == 's':
        opposite = 'n'
    elif dir == 'e':
        opposite = 'w'
    elif dir == 'w':
        opposite = 'e'
    return opposite


def randomDir():
    ranNum = random.randrange(0, 4)
    if ranNum == 0:
        dir = 'n'
    elif ranNum == 1:
        dir = 's'
    elif ranNum == 2:
        dir = 'e'
    else:
        dir = 'w'
    return dir


#  *************************************
traversal_graph = {}

# build the traversal_graph as a parallel to track visited rooms and their dir's
for i in range(len(room_graph)):
    traversal_graph[i] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}

# tracks dir for every single move we make (n, s, e, w)
traversal_path = []

# track visited room id's
# used to control the main loop below
visited = set()
visited.add(player.current_room)

# track return path to last room that still has unexplored exits
returnPath = Stack()

# switch that denotes when we're 'backtracking'
backTracking = False

# ************************************************
# ************************************************
# ****************** START  **********************

def checkAvailableExits(exits):
    global backTracking
    rm = player.current_room.name.split(' ')
    ind = int(rm[1])
    availablePaths = []

    # find all paths not yet explored
    for e in exits:
        if traversal_graph[ind][e] == '?':
            availablePaths.append(e)

    if len(availablePaths) == 0:
        backTracking = True
        return returnPath.pop()

    if backTracking:
        for path in availablePaths:
            if path:
                backTracking = False
                return path
            else:
                backTracking = True
                return returnPath.pop()

    # not backtracking
    else:
        if len(traversal_path) != 0:
            if player.current_room not in visited:
                for path in availablePaths:
                    # if path is not the dir we just came from
                    if traversal_graph[ind][path] != reverseDir(traversal_path[-1]):
                        backTracking = False
                        return path

            # if cur room IS in visited: turn around
            else:
                backTracking = True
                return returnPath.pop()

        # if no traversal path yet
        # meaning we just started
        else:
            for path in availablePaths:
                backTracking = False
                return path


def visitRoom(room):
    if prevRoom not in visited:
        visited.add(prevRoom)
    # grab the int part of the prev room name
    # curRoom has not been updated to 'new room' yet
    prevRmSplit = prevRoom.name.split(' ')
    prevInd = int(prevRmSplit[1])

    # grab the int part of the curren room name
    curRmSplit = room.name.split(' ')
    curInd = int(curRmSplit[1])
    # add last visited room's ('traversal_path' last entry) dir to traversal 'graph' as curRoom
    lastDir = traversal_path[-1]

    # connect the 2 rooms together
    # add cur path to traversal_graph
    traversal_graph[prevInd][lastDir] = room
    # add the reversed path to traversal_graph
    traversal_graph[curInd][reverseDir(lastDir)] = prevRoom

while len(visited) != len(room_graph):
    # players starting current room object
    curRoom = player.current_room

    # grab the int part of the room name
    rmSplit = curRoom.name.split(' ')
    ind = int(rmSplit[1])

    # all exits for cur room
    curExits = curRoom.get_exits()

    # when player moves:
    travelDir = checkAvailableExits(curExits)
    if travelDir is not None:

        # add to traversal_path
        traversal_path.append(travelDir)

        # tracks path back to last room that still
        # has unvisited exits
        if not backTracking:
            returnPath.push(reverseDir(travelDir))

        prevRoom = curRoom
        # MOVE
        player.travel(travelDir)
        # visit next room
        visitRoom(player.current_room)

# check room exits:

    # if cur room not visited
    # if returnPath is empty
    # && still has unvisited exits:
    # add cameFrom dir to returnPath

    # if returnPath is empty & cur room unexplored exits > 1
    # add unexplored exits to returnPath

    # loops?
    # if unvisited exit == 'cameFrom' and backTracking == False
    # mark that exit as visited

    # if cur room has only 1 unexplored exit thats not == cameFrom:
    # mark as visited


#  ***************
# test prints:
# print('traversal_path: ', traversal_path)
# print('')
# print('visited: ', visited)
# print('')
# print('traversal_graph: ', traversal_graph)
# print('')
# print('traversal_graph len: ', len(traversal_graph))
# print('')
# print('room graph len: ', len(room_graph))


# print('traversal graph: ', traversal_graph)
# print('traversal_path', traversal_path)
# print('randomDir: ', randomDir())
# print('# of rooms: ', len(room_graph))
# print('room id: ', player.current_room.id)
# print('room name: ', player.current_room.name)
# print('current room: ', player.current_room)
# print('travel N:', player.travel('n'))
# print('current room: ', player.current_room)
# print('travel N:', player.travel('n'))
# print('current room: ', player.current_room)
# print('travel N:', player.travel('n'))
# print('')
# print('get exits', player.current_room.get_exits())
# print('current room: ', player.current_room)
# # print('travel S:', player.travel('s'))
# print('travel S:', player.travel('s'))
# print('get exits', player.current_room.get_exits())
# print('')
# print('travel E:', player.travel('e'))
# print('get exits', player.current_room.get_exits())
# print('')
# print('travel W:', player.travel('w'))
# print('get exits', player.current_room.get_exits())


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
