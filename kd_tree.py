

class Node:
    
    def __init__(self, val: list[float], dim: int, left: "Node" = None, right: "Node" = None):
        self.val = val
        self.dim = dim
        self.left = left
        self.right = right

def build_kd_tree(k: int, data: list[list[float]], _depth: int = 0) -> (Node|None):
    """Build a kd-tree for a dataset of points in the given dimension
    

    Parameters
    ----------
    k : int
        The dimension of the kd-tree we want to build
    data : list[list[float]]
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

def k_dist(pt1: tuple[float,...], pt2: tuple[float,...], k: int) -> float:
    
    square_sum = sum((pt1[i] - pt2[i])**2 for i in range(k))
    return square_sum**0.5
    

def find_NN(point: tuple[float,...], tree: Node, _mindist: float = -1, _depth: int = 0) -> tuple[float,...] :
    """Find the nearest neighbor in the kd-tree to the given point

    Parameters
    ----------
    point : tuple[float,...]
        The reference point to which we want to find the nearest neighbor for
    tree : Node
        kd-tree containing point we are searching for
    
    
    Returns
    -------
    tuple[int,...]
        The nearest point in `tree` to `point`
    """
    
    minpt = None
    # basically just rejects this case
    if tree is None:
        return (minpt, _mindist + 1) # if it returns a bigger minimum, it's never gonna be good
    
    # set an initial distance to use in future comparisons
    if _mindist == -1:
        _mindist = k_dist(point, tree.val, tree.dim)
        minpt = tree.val
    
    axis = _depth % tree.dim
    went_left = True # used to know which branch to go down in case there is possible nearer point down other branch
    
    
    # go through tree until a leaf is reached
    if point[axis] < tree.val[axis] and tree.left is not None:
        minpt, this_mindist = find_NN(point, tree.left, _mindist, _depth + 1)
        if this_mindist < _mindist: _mindist = this_mindist
    elif point[axis] > tree.val[axis] and tree.right is not None:
        went_left = False
        minpt, this_mindist = find_NN(point, tree.right, _mindist, _depth + 1)
        if this_mindist < _mindist: _mindist = this_mindist
    
    
    # calc if the current point is also the current nearest
    d = k_dist(tree.val, point, tree.dim)
    if d < _mindist:
        minpt = tree.val
        _mindist = d
    
    # if possible nearer point in other branch, do a NN search down that branch
    if abs(point[axis] - tree.val[axis]) < _mindist:
        other_minpt, other_mindist = find_NN(point, tree.right if went_left else tree.left, _mindist, _depth + 1)   
        if other_mindist < _mindist:
            _mindist = other_mindist
            minpt = other_minpt
    
    return (minpt, _mindist)
            

if __name__ == "__main__":
    import random as r
    
    SEED = None
    r.seed(SEED)
    K = 3
    SIZE = 10000 
    bounds = (0, 2560)

    def linear_closest(point: tuple[float,...], points: list[list[float]], k: int) -> tuple[tuple[float,...], float]:
        
        curr_best = (points[0], k_dist(point, points[0], K))

        for pt in points:
            d = k_dist(point, pt, k)
            if d < curr_best[1]:
                curr_best = (pt, d)
        
        return curr_best

    def gen_n_rand_pts(n, dim, bounds):
        return [[r.randint(*bounds) for _ in range(dim)] for _ in range(n)]
    
    

    dataset = gen_n_rand_pts(SIZE, K, bounds)
    
    tree = build_kd_tree(K, dataset)

    for _ in range(50):
        test_pt = gen_n_rand_pts(1, K, bounds)[0]
        res1 = find_NN(test_pt, tree) 
        res2 = linear_closest(test_pt, dataset, K)
        print(res2)
        print(res1)
        assert res1 == res2
        print()

    