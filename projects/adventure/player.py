class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.currentRoom = starting_room

    def travel(self, direction, show_rooms=False):
        next_room = self.currentRoom.get_room_in_direction(direction)
        if next_room is not None:
            self.currentRoom = next_room
            if show_rooms:
                next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")
