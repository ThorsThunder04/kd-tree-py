

class Node:
    
    def __init__(self, val: tuple[int,...], dim: int, left: "Node" = None, right: "Node" = None):
        self.val = val
        self.dim = dim
        self.left = left
        self.right = right

def build_kd_tree(dim: int, data: list[tuple], _depth: int = 0) -> (Node|None):
    
    if len(data) == 0:
        return None
    if len(data) == 1:
        return Node(data[0], dim, None, None)
    
    axis = _depth % dim
    median = len(data) // 2

    data.sort(key = lambda x: x[axis])

    curr_node = Node(data[median], dim)

    curr_node.left = build_kd_tree(dim, data[:median], _depth + 1)
    curr_node.right = build_kd_tree(dim, data[median+1:], _depth + 1)

    return curr_node



if __name__ == "__main__":
    import random as r
    
    SEED = 123
    K = 3
    SIZE = 10
    bounds = (0, 256)

    r.seed(SEED)
    dataset = [[r.randint(*bounds) for _ in range(K)] for _ in range(SIZE)]
    
    tree = build_kd_tree(K, dataset)