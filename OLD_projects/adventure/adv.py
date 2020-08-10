from room import Room
from player import Player
from world import World

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
# not currently using randomDir ******


def randomDir(camefrom):
    randomDir = random.randrange(0, 4)  # exclusive
    if randomDir == 0:
        direction = 'n'
    elif randomDir == 1:
        direction = 's'
    elif randomDir == 2:
        direction = 'e'
    elif randomDir == 3:
        direction = 'w'
        
    # if it's not the dir we just came from
    if cameFrom != direction:
        print('rand dir: ', direction)
        return direction
    return direction


def chooseDir(cameFrom):
    possibleDirs = player.current_room.get_exits()
    for dir in possibleDirs:
        if backTracking == True:
            print('random dir: ', dir)
            randDir = randomDir(cameFrom)
            return randDir

        elif traversal_graph[curRoom.id][dir] == '?':
            # check if it's the way we came or not
            # cameFrom is a list of directions we've been from curRoom
            if cameFrom != dir:
                print('choose dir: ', dir)
                return dir

    return False


def getDirectionOpposite(dir):
    if dir == 'n':
        opposite = 's'
    elif dir == 's':
        opposite = 'n'
    elif dir == 'e':
        opposite = 'w'
    elif dir == 'w':
        opposite = 'e'

    print('opposite dir: ', opposite)
    return opposite

#  *************************************
traversal_graph = {}

# build the traversal_graph as a parallel to track visited rooms and their dir's
for i in range(len(room_graph)):
    traversal_graph[i] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}

# tracks dir for every single move we make (n, s, e, w)
traversal_path = []

# track visited room id's 
# used to control loop below
visited = set()

# if we're back tracking
backTracking = False

# players starting current room object
curRoom = player.current_room
print('starting room: ', curRoom.id)
prevRoom = curRoom

# current room exits list
curExits = curRoom.get_exits()

# track most recent dir we came from: 'n', 's', etc
cameFrom = None
count = 30
while len(visited) != len(room_graph):
    # temporary loop counter during testing to avoid the inf loop
    # while count > 0:
    print('backtracking at loop start: ', backTracking)
    # current room exits list
    curExits = curRoom.get_exits()

    # figure out a direction to go
    direction = chooseDir(cameFrom)
    # returns False if no directions from current room
    # that are NOT 'cameFrom'
    if direction == False:
        # then we're at a dead end
        print('dead-end, Time to turn around')
        direction = getDirectionOpposite(traversal_path[-1])
        backTracking = True
        print('backtracking: ', backTracking)

    # current 'came from' dir: 'n', 's', etc
    cameFrom = (getDirectionOpposite(direction))

    # is there a room in that direction?
    if player.current_room.get_room_in_direction(direction):

        # track prev room so we can update traversal_graph
        prevRoom = player.current_room

        # travel to room
        player.travel(direction, show_rooms=True)
        curRoom = player.current_room

        if traversal_graph[prevRoom.id][direction] == '?':
            # if we find a NEW room, we're no longer backtracking
            backTracking = False
            traversal_graph[prevRoom.id][direction] = player.current_room.id
            # track visited to control the loop
            visited.add(curRoom.id)

        # update our tracking vars for each move
        traversal_path.append(direction)
    else:
        print('no room in that direction')

    print('prevRoom: ', prevRoom.id)
    print('new current room: ', curRoom.id)
    # used for temporary loop counter for testing to avoid the inf loop
    count -= 1


#  ***************
# test prints:
print('traversal_path: ', traversal_path)
print('')
print('visited: ', visited)
print('')
print('traversal_graph: ', traversal_graph)
print('')
print('traversal_graph len: ', len(traversal_graph))
print('')
print('room graph len: ', len(room_graph))


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
