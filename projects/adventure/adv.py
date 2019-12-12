from collections import deque
from room import Room
from player import Player
from world import World
from graph import roomGraph
import random

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.

world.load_graph(roomGraph)

# UNCOMMENT TO VIEW MAP
world.print_rooms()

player = Player("Name", world.startingRoom)


# Fill this out
def traverse(start_room):
    print('Searching for path...')
    path = ((start_room, ''),)
    paths = set(path)
    queue = deque([path])
    while queue:
        path = queue.popleft()
        if path not in paths:
            paths.add(path)
            if all([room in [room.id_ for room, d in path] for room in range(len(world.rooms))]):
                return [direction for _, direction in path if direction]
            room = path[-1][0]
            neighbors = get_neighbors(room.id_)
            # Toggle commenting on following lines to implement shortest path (long time to compute)
            # or any path (much shorter compute time)(but still a long, long time).
            # if len(neighbors) > 0:  # Uncomment to find the shortest path.
            if any([x[0].id_ not in [room.id_ for room, _ in path] for x in neighbors]):  # Uncomment to find any path.
                for neighbor in neighbors:
                    new_path = (*path, neighbor)
                    queue.append(new_path)
            else:
                i = len(path)
                new_path = (*path,)
                while i > 1:
                    i -= 1
                    neighbors = get_neighbors(path[i][0].id_)
                    if any([room[0].id_ not in [room.id_ for room, _ in path] for room in neighbors]):
                        break
                    reverse_dir = {'n': 's', 'w': 'e', 's': 'n', 'e': 'w'}
                    new_path = (*new_path, (path[i][0], reverse_dir[path[i][1]]))
                for neighbor in [(room, direction) for room, direction in neighbors
                                 if room.id_ not in [room.id_ for room, _ in path]]:
                    new_path_ = (*new_path, neighbor)
                    queue.append(new_path_)


def get_neighbors(room):
    room = world.rooms[room]
    neighbors = []
    if room.n_to is not None:
        neighbors.append((room.n_to, 'n'))
    if room.w_to is not None:
        neighbors.append((room.w_to, 'w'))
    if room.s_to is not None:
        neighbors.append((room.s_to, 's'))
    if room.e_to is not None:
        neighbors.append((room.e_to, 'e'))
    return neighbors


traversalPath = traverse(world.startingRoom)
print(traversalPath)
# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)

for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
