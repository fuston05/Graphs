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
    if cameFrom != direction:
        print('rand dir: ', direction)
        return direction
    return direction

def chooseDir(cameFrom):
    possibleDirs= player.current_room.get_exits()
    for dir in possibleDirs:
        if backTracking == True:
            if cameFrom != dir:
                return randomDir(cameFrom)
        if traversal_graph[curRoom.id][dir] == '?':
            # check if it's the way we came or not
            # cameFrom is a list of directions we've been from curRoom
            if cameFrom != dir:
                return dir

    return False

def getDirectionOpposite(dir, backTracking):
    backTracking= True
    if dir == 'n':
        opposite = 's'
    elif dir == 's':
        opposite = 'n'
    elif dir == 'e':
        opposite = 'w'
    elif dir == 'w':
        opposite = 'e'
    return opposite

# def movePlayer(direction, curRoom, prevRoom):
#     # move the player in the chosen direction, and show room info
#     player.travel(direction, show_rooms=True)
#     if traversal_graph[prevRoom.id][(direction)] == '?':
#         traversal_graph[prevRoom.id][direction]= curRoom.id
#     # update our tracking vars for each move
#     traversal_path.append(direction)
#     # curRoom= player.current_room
#  *************************************
traversal_graph={}
# build the traversal_graph as a parallel to track visited rooms and their dir's
for i in range(len(room_graph)):
    traversal_graph[i]= {'n': '?', 's': '?', 'e': '?', 'w': '?'}

traversal_path = []

# track visited room id's
visited = set()

# if we're back tracking
backTracking= False

# players starting current room object
curRoom = player.current_room
print('starting room: ', curRoom.id)
prevRoom= curRoom
# current room exits list
curExits = curRoom.get_exits()

# track most recent dir we came from: 'n', 's', etc
cameFrom= None
count= 40
while len(visited) != len(room_graph):
# temporary loop counter during testing to avoid the inf loop
# while count > 0:
    print('backtracking: ', backTracking)
    # current room exits list
    curExits = curRoom.get_exits()

    # figure out a direction to go
    direction = chooseDir(cameFrom)
    # returns False if no directions from current room 
    # that are NOT 'cameFrom'
    if direction == False:
        # then we're at a dead end
        print('dead-end, Time to turn around')
        direction= getDirectionOpposite(traversal_path[-1], backTracking)
        backTracking= True

    # is there a room in that direction?
    if player.current_room.get_room_in_direction(direction):

        # current 'came from' dir: 'n', 's', etc
        cameFrom= (getDirectionOpposite(direction, backTracking))
        # track prev room so we can update traversal_graph
        prevRoom= player.current_room


        # update graph to track where we've explored
        # travel to room
        player.travel(direction, show_rooms=True)
        curRoom= player.current_room

        if traversal_graph[prevRoom.id][direction] == '?':
            # if we find a NEW room, we're no longer backtracking
            backTracking= False
            traversal_graph[prevRoom.id][direction]= player.current_room.id
            # track visited to control the loop
            visited.add(curRoom.id)

        # update our tracking vars for each move
        traversal_path.append(direction)
    else:
        print('no room in that direction')
    # used for temporary loop counter for testing to avoid the inf loop
    print('prevRoom: ', prevRoom.id)
    print('new current room: ', curRoom.id)
    count-= 1



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


# OLD CODE ***********************************
# generate a parallell of the room graph, for -
# traversal of unexplored rooms that have a '?'
# populate this as we go
# for i in range(len(room_graph)):
#     traversal_graph[i] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}

# q = Queue()
# q.enqueue({player.current_room.id: traversal_graph[player.current_room.id]})

# # Create a Set to store visited rooms
# visited = set()
# print('Q: ', q)
# while q.size() > 0:
# # Dequeue the first PATH
# path = q.dequeue()
# # Grab the last vertex from the PATH
# lastRoom = path[-1]
# print('last room: ', lastRoom)
# # If that vertex has not been visited...
# if lastRoom not in visited:
#     visited.add(lastRoom)
#     # Then add A PATH TO its neighbors to the back of the queue
#     for neighbor in player.current_room.get_exits():
#         # COPY THE PATH
#         tempPath = list(path)
#         # APPEND THE NEIGHOR TO THE BACK
#         tempPath.append(neighbor)
#         q.enqueue(tempPath)


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
