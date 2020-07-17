from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

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

def randomDir(curExits):
    randomDir= random.randrange(0, curExits)
    if randomDir == 0:
        direction= 'n'
    elif randomDir == 1:
        direction= 's'
    elif randomDir == 2:
        direction= 'e'
    elif randomDir == 3:
        direction= 'w'
    print('rand dir: ', direction)
    return direction

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_graph= {}

# generate a parallell of the room graph, for -
# traversal of unexplored rooms that have a '?'
# populate this as we go
for i in range(len(room_graph)):
    traversal_graph[i]= {'n': '?', 's': '?', 'w': '?', 'e': '?'}

q= Queue()
q.enqueue(player.current_room.id)

while q.size() > 0:
    curRoom= q.dequeue()
    prevRoom= curRoom
    print('curRoom id: ', curRoom)

    # get exits
    exits= player.current_room.get_exits()
    print('current exits: ', exits)
    if exits:
        # if rand direction exists in current room's exits
        direction= randomDir(len(exits))
        print('dir: ', direction)
    #else: if there are no exits: dead-end
    # walk back
    # if no exits
    else: 
        print('This room is a dead-end')

    if traversal_graph[prevRoom][direction] == '?':
        # move to new room in new 'direction
        player.travel(direction, show_rooms= True)
        # pick an exit, and GO there.. IF it has a '?' as a value for that dir
        q.enqueue(player.current_room.id)
        print('new room: ', player.current_room.id)
        # log this room into path and graph
        traversal_path.append(direction)
        traversal_graph[prevRoom][direction]= player.current_room.id
        



print('traversal graph: ', traversal_graph)
print('traversal_path', traversal_path)
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
