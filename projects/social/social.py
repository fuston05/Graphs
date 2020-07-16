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

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # !!!! IMPLEMENT ME
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # Shuffle the possible friendships
        random.shuffle(possible_friendships)

        # Add friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def bft(self, user_id):
        q = Queue()
        visited = set()
        # initial state
        q.enqueue(user_id)

        while q.size() > 0:
            curUser = q.dequeue()

            if curUser not in visited:
                visited.add(curUser)
                # get curUser's friends
                curFriends = self.friendships[curUser]
                for friend in curFriends:
                    q.enqueue(friend)

        return visited

    def bfs(self, user_id, target):
        q = Queue()

        # initial state
        q.enqueue([user_id])

        visited = set()

        while q.size() > 0:
            path = q.dequeue()

            lastFriend = path[-1]

            if lastFriend not in visited:
                if lastFriend is target:
                    # IF SO, RETURN PATH
                    return path

                # Mark as visited...
                visited.add(lastFriend)
                # Then add A PATH TO its friends to the back of the queue
                for friend in self.friendships[lastFriend]:
                    # COPY THE PATH
                    tempPath = list(path)
                    # APPEND THE NEIGHOR TO THE BACK
                    tempPath.append(friend)
                    q.enqueue(tempPath)
        return None

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # build a list of in-network friends in 'added'
        # bft returns a list of ALL user_id's friends
        added = self.bft(user_id)

        # separationDegree = list()

        for user in added:
            # path to each 'user' from starting user_id
            path = self.bfs(user_id, user)
            if user not in visited:
                # separationDegree.append(len(path))
                visited[user] = path

        # calculate the average degree of separation
        # tempSum = 0
        # for d in separationDegree:
        #     tempSum += d
        # aveSeparation = tempSum//len(separationDegree)

        # test print for average degree of separation
        # print('degrees of separation: ', aveSeparation)
        # print('')
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 10)
    print('sg.friendships: ', sg.friendships)
    print('')
    connections = sg.get_all_social_paths(1)
    # print('Connections:', connections)
    print('')
    # print('total users: ', len(sg.users))
    # print('')
    print('# of Connections: ', len(connections))
    # print('')
    # calculate the % of other users that will -
    # be in a given user's extended network
    # print('connections %: ', len(connections)/len(sg.users))
