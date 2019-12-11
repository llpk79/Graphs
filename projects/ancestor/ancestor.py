from collections import deque


def earliest_ancestor(ancestors, starting_node):
    anc = {}
    for a1, a2 in ancestors:
        if a2 not in anc:
            anc[a2] = {a1}
        else:
            anc[a2].add(a1)
    path = [starting_node]
    q = deque([path])
    while q:
        parents = []
        parent = q.popleft()[-1]
        if parent != starting_node and parent not in anc:
            parents.append(parent)
            continue
        if parent not in anc:
            break
        for child in anc[parent]:
            path = [*path, child]
            q.append(path)
    if parents:
        return min(parents)
    return -1
