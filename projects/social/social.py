import random

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

class User:
    def __init__(self, name):
        self.name = name

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
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users): #O(n) over all users
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users: # O(n) over all users
            # O(n) over  range of 1 - len all users?
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        # O(n) over users* avg friendships
        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])

    def populate_graph2(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users): #O(n) over all users
            self.add_user(f"User {i}")

    def get_friends(self, user_id):
        friends= self.friendships[user_id]
        return friends

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        q= Queue()
        q.enqueue([user_id])
        sepDegrees= []

        while q.size() > 0:
            curPath= q.dequeue()
            curUser= curPath[-1]

            if curUser not in visited:
                visited[curUser]= curPath

                for friend in self.get_friends(curUser):
                    tempPath= curPath.copy()
                    tempPath.append(friend)
                    sepDegrees.append(len(tempPath))
                    q.enqueue(tempPath)
        print('\n********\naverage degrees of separeation: ', round(sum(sepDegrees) / len(sepDegrees), 2), '\n********\n')
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(20, 2)
    print('sg.friendships: ', sg.friendships)
    print('')
    connections = sg.get_all_social_paths(1)
    print('Connections:', connections)
    print('')
    print('total users: ', len(sg.users))
    print('')
    print('# of Connections: ', len(connections))
    print('')
    # calculate the % of other users that will -
    # be in a given user's extended network
    print('connections %: ', len(connections)/len(sg.users))
