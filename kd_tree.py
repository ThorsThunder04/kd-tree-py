

class Node:
    
    def __init__(self, val: list[int], dim: int, left: "Node" = None, right: "Node" = None):
        self.val = val
        self.dim = dim
        self.left = left
        self.right = right

def build_kd_tree(k: int, data: list[list[int]], _depth: int = 0) -> (Node|None):
    """Build a kd-tree for a dataset of points in the given dimension
    

    Parameters
    ----------
    k : int
        The dimension of the kd-tree we want to build
    data : list[list[int]]
        The list of `k` dimensional points we want to insert into the tree
       

    Returns
    -------
    Node|None
        The root of the build kd-tree (None if `data` is empty) 
    """
    
    if len(data) == 0:
        return None
    if len(data) == 1:
        return Node(data[0], k, None, None)
    
    # Calculate the axis used at this depth
    axis = _depth % k
    median = len(data) // 2

    # we sort all the data to have a balanced subtree
    data.sort(key = lambda x: x[axis])

    # create node for the median point
    curr_node = Node(data[median], k)

    # repeat process for both child subtrees
    curr_node.left = build_kd_tree(k, data[:median], _depth + 1)
    curr_node.right = build_kd_tree(k, data[median+1:], _depth + 1)

    return curr_node

def find_NN(point: tuple[int,...], tree: Node) -> tuple[int,...] :
    """Find the nearest neighbor in the kd-tree to the given point

    Parameters
    ----------
    point : tuple[int,...]
        The reference point to which we want to find the nearest neighbor for
    tree : Node
        kd-tree containing point we are searching for
    
    
    Returns
    -------
    tuple[int,...]
        The nearest point in `tree` to `point`
    """
    pass 


if __name__ == "__main__":
    import random as r
    
    SEED = 123
    K = 3
    SIZE = 10
    bounds = (0, 256)

    r.seed(SEED)
    dataset = [[r.randint(*bounds) for _ in range(K)] for _ in range(SIZE)]
    
    tree = build_kd_tree(K, dataset)