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
    parentsToVisit = Stack()
    parentsToVisit.push(starting_node)
    visited = set()

    # parents used below ot track 
    # current parents for each iteration
    parents= None

    while parentsToVisit.size() > 0:
        cur = parentsToVisit.pop()

        if cur not in visited:
            # store 'visited'
            visited.add(cur)

            # get cur's parents
            for g in get_parents(cur, ancestors):
                if g: #if parent was returned from get_parents
                    # reset the parents list
                    parents= set()
                    # add parents
                    parents.add(g)
                    parentsToVisit.push(g)

    return min(parents) if parents else -1


def get_parents(child, ancestors):
    # go through ancestor data list
    parents = set()
    for ancestor in ancestors:
        # parent
        par = ancestor[0]
        # child
        ch = ancestor[1]
        if ch == child:
            # add the parent from that pair as one of 'child's' parents
            parents.add(par)
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
