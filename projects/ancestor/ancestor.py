from collections import deque


def earliest_ancestor(ancestors, starting_node):
    ancestor_dict = {}
    for parent, child in ancestors:
        if child not in ancestor_dict:
            ancestor_dict[child] = {parent}
        else:
            ancestor_dict[child].add(parent)
    path = [starting_node]
    queue = deque([path])
    while queue:
        parents = []
        parent = queue.popleft()[-1]
        if parent not in ancestor_dict:
            if parent == starting_node:
                break
            parents.append(parent)
            continue
        for child in ancestor_dict[parent]:
            path = [*path, child]
            queue.append(path)
    if parents:
        return min(parents)
    return -1
