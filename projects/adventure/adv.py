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


def randomDir():
    randomDir = random.randrange(0, 3)
    if randomDir == 0:
        direction = 'n'
    elif randomDir == 1:
        direction = 's'
    elif randomDir == 2:
        direction = 'e'
    elif randomDir == 3:
        direction = 'w'
    print('rand dir: ', direction)
    return direction


def getDirectionOpposite(dir):
    if dir == 'n':
        opposite = 's'
    elif dir == 's':
        opposite = 'n'
    elif dir == 'e':
        opposite = 'w'
    elif dir == 'w':
        opposite = 'e'
    return opposite


def chooseDirection():
    exits = player.current_room.get_exits()
    for e in exits:
        if traversal_graph[player.current_room.id][e] == '?':
            direction = e
            return direction
    # id all exites have been explored
    return False


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_graph = {}

# generate a parallell of the room graph, for -
# traversal of unexplored rooms that have a '?'
# populate this as we go
for i in range(len(room_graph)):
    traversal_graph[i] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}

q = Queue()
q.enqueue([player.current_room.id])
# Create a Set to store visited rooms
visited = set()

while q.size() > 0:
    # Dequeue the first PATH
    path = q.dequeue()
    # Grab the last vertex from the PATH
    lastRoom = path[-1]
    print('last room: ', lastRoom)
    # If that vertex has not been visited...
    if lastRoom not in visited:
       
        visited.add(lastRoom)
        # Then add A PATH TO its neighbors to the back of the queue
        for neighbor in player.current_room.get_exits():
            # COPY THE PATH
            tempPath = list(path)
            # APPEND THE NEIGHOR TO THE BACK
            tempPath.append(neighbor)
            q.enqueue(tempPath)






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
