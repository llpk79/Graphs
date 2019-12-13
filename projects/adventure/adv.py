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
class PathFinder:
    """Find a path that visits all rooms in <world>.

    """

    def __init__(self, world: World):
        self.world = world
        self.start = self.world.startingRoom
        self.path = []

    @ staticmethod
    def get_neighbors(room: Room) -> list:
        """Find all neighbors of <room>.
        Return a list of tuples (neighbor, direction taken to reach neighbor)"""
        neighbors = []
        if room.n_to is not None:
            neighbors.append((room.n_to, 'n'))
        if room.w_to is not None:
            neighbors.append((room.w_to, 'w'))
        if room.e_to is not None:
            neighbors.append((room.e_to, 'e'))
        if room.s_to is not None:
            neighbors.append((room.s_to, 's'))
        return neighbors

    def DFT(self, room: Room) -> list:
        """Return a path from <room> to a room with no unexplored exits by depth first traversal."""
        path = [room]
        stack = [path]
        visited = set()

        while stack:
            # Get a candidate path and the last room in it.
            path = stack.pop()
            rm = path[-1][0]

            # Check that this room hasn't already been seen.
            if rm.id_ not in visited:
                visited.add(rm.id_)

                # If all of the neighboring rooms are on this path, this is a dead end. Return the path to this room.
                neighbors = self.get_neighbors(rm)
                if all([neighbor_room.id_ in [path_room.id_ for path_room, _ in path]
                        for neighbor_room, _ in neighbors]):
                    return path[1:]  # The start of this path is already a part of the main path.

                # Otherwise, keep exploring this path.
                for neighbor in neighbors:
                    # Only add neighbors that aren't yet on the main path.
                    if neighbor[0].id_ not in [room.id_ for room, _ in self.path]:
                        new_path = [*path, neighbor]
                        stack.append(new_path)
        return path

    def BFT(self, room: Room) -> list:
        """Returns a path from a dead-end <room> to the nearest room with an unexplored neighbor."""
        path = [room]
        visited = set()
        queue = deque()
        queue.append(path)

        while queue:
            # Get a candidate path and the last room in it.
            path = queue.popleft()
            rm = path[-1][0]

            # Check that this room hasn't been seen.
            if rm.id_ not in visited:
                visited.add(rm.id_)

                # If any neighbor of this room is not yet on the main path, return the path to this room.
                neighbors = self.get_neighbors(rm)
                if any([neighbor_room.id_ not in [path_room.id_ for path_room, _ in self.path]
                        for neighbor_room, _ in neighbors]):
                    return path[1:]  # The start of this path is already a part of the main path.

                # Otherwise, continue looking for a room with an unexplored neighbor.
                for neighbor in neighbors:
                    new_path = [*path, neighbor]
                    queue.append(new_path)

    def traverse(self) -> list:
        """Traverse the graph, alternating from a dft to a dead-end and a bft to a new, open path.

        1. Start the path at the start.
        2. DFT to a dead end.
        3. Append that path to the main path.
        4. BFT back to nearest room with an unexplored neighbor.
        5. Append that path to the main path.
        6. Repeat 2-5 until BFT doesn't find anything.
        7. Return the path.
        """
        print('Finding path...')
        # Initialize path with a tuple (starting room, empty string).
        self.path = [(self.start, '')]  # 1.

        while True:  # 6.
            # Create a new reference for this loop.
            main_path = self.path.copy()

            # Find a dead-end.
            dft_path = self.DFT(main_path[-1])  # 2.
            main_path = [*main_path, *dft_path]  # 3.

            # Update for BFT
            self.path = main_path
            bft_path = self.BFT(main_path[-1])  # 4.

            # If BFT finds no unexplored rooms, the graph has been traversed.
            if not bft_path:
                return [direction for _, direction in self.path[1:]]  # 7.

            # Update for next loop.
            main_path = [*main_path, *bft_path]  # 5.
            self.path = main_path


finder = PathFinder(world=world)
traversalPath = finder.traverse()
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
