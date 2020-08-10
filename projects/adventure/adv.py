from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# *********************************************************** #
# *********************************************************** #

# ************** functions ***************


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

# players starting current room object
curRoom = player.current_room

# current room exits list
curExits = curRoom.get_exits()


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
