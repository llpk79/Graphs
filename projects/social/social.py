import random
from collections import deque


class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User({repr(self.name)})"


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()
        self.last_id += 1  # automatically increment the ID to assign the new user

    def populate_graph(self, num_users, avg_friendships):
        """
        Creates <num_user> of users and randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        :param num_users: int number of users to create
        :param avg_friendships: int average number of friendships a user should have.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        if num_users <= avg_friendships:
            print("Warning! num_users must be greater than avg_friendships.")
            return
        # Add users.
        for i in range(num_users):
            self.add_user(i)
        # Friendships come in pairs.
        friendships = (num_users * avg_friendships) // 2
        for _ in range(friendships):
            # Create unique, random friendships.
            while True:
                user = random.randint(0, self.last_id - 1)
                friend = random.randint(0, self.last_id - 1)
                # Be sure friendships aren't repeating.
                if (friend != user
                        and friend not in self.friendships[user]
                        and user not in self.friendships[friend]):
                    break
            self.add_friendship(user, friend)
        # # Check that our average is correct.
        # friends = [len(x) for x in self.friendships.values()]
        # print('average friends', sum(friends)/len(friends))

    def get_all_social_paths(self, user_id):
        """
        Use BFS to create a path from the <user_id> to all points in the extended network.

        :param user_id: Id of user whose extended network we want to examine.

        :returns network: a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.

        """
        # Start the path at the given id.
        path = [user_id]
        # Populate a queue with the starting path.
        queue = deque([path])
        # Create a dict to track the extended network.
        network = {}
        while queue:
            # Get a path from the queue.
            path = queue.popleft()
            # Get the last friend from the queue.
            id_ = path[-1]
            # Make sure they're not already in the network.
            if id_ not in network:
                # Add the friend and the path to the network.
                network[id_] = path
                # Find new friends to add.
                for friend in self.friendships[id_]:
                    # Add the new friend to the current path and add it to the queue.
                    new_path = [*path, friend]
                    queue.append(new_path)
        return network


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(100, 20)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
