class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def earliest_ancestor(ancestors, starting_node):
    s = Stack()
    visited = set()
    parents = []

    s.push(starting_node)
    while s.size() > 0:
        curNode = s.pop()
        if curNode not in visited:
            visited.add(curNode)
            tempParents = get_parents(curNode, ancestors)
            if tempParents:
                parents = tempParents
                for p in parents:
                    s.push(p)
    if len(parents) == 0:
        return -1
    return min(parents)

def get_parents(child, ancestors):
    parents = []
    # 1st int is parent, second is child
    # loop over ancestors at 0 index
    for a in ancestors:
        # check to see if its child == child
        if a[1] == child:
            parents.append(a[0])
    # return all parents
    return parents


if __name__ == "__main__":
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

    # print(earliest_ancestor(test_ancestors, 1))  # 10
    # print('')
    # print(earliest_ancestor(test_ancestors, 2))  # -1
    # print('')
    # print(earliest_ancestor(test_ancestors, 3))  # 10
    # print('')
    # print(earliest_ancestor(test_ancestors, 4))  # -1
    # print('')
    # print(earliest_ancestor(test_ancestors, 5))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 6))  # 10
    # print('')
    # print(earliest_ancestor(test_ancestors, 7))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 8))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 9))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 10))  # -1
    # print('')
    # print(earliest_ancestor(test_ancestors, 11))  # -1
    # print('')
