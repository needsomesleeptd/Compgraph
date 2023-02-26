EPS = 1e-1



def find_graph_node(node,graphs:list):
    for graph_index in range(len(graphs)):
        ind = find_node(node,graphs[graph_index])
        if (ind != None):
            return graph_index,ind
    return None,None

def find_node(node, list_of_nodes):
    for i in range(len(list_of_nodes)):
        if (are_eq_nodes(node,list_of_nodes[i])):
            return i
    return None


def almost_equal(value_1, value_2, accuracy = 10**-2):
    return abs(value_1 - value_2) < accuracy
def are_eq_nodes(first_dot,second_dot,accuracy = 10**-2):
    if almost_equal(first_dot[0],second_dot[0],accuracy) and almost_equal(first_dot[1],second_dot[1],accuracy):
        return True
    else:
        return False




def get_dot_index(graphs:list,nodes_count:int):
    graph_index = 0
    graphs_nodes_count = 0
    while (nodes_count > len(graphs[graph_index])):
       nodes_count -= len(graphs[graph_index])
       graph_index += 1
    node_index = nodes_count
    return graph_index,node_index

def get_dot_index(graphs:list,graph_index:int):
   nodes_count = 1
   for i in range(graph_index):
       nodes_count += len(graphs[i]) + 1
   return nodes_count








def vector_scalar_product(first_vector,second_vector):
    scalar_sum = 0
    for i in range(len(first_vector.coords)):
        scalar_sum += first_vector.coords[i] * second_vector.coords[i]
    return scalar_sum

def vector_angle_cos(first_vector,second_vector):
    return vector_scalar_product(first_vector,second_vector)/(first_vector.len() * second_vector.len())


def find_similar_graphs_with_max_nodes(nodes:list):
    max_n = 0
    first_graph_index = -1
    second_graph_index = -1
    for i in range(len(nodes) - 1):
        for j in range(i + 1,len(nodes)):
            if (len(nodes[i]) != len(nodes[j])):
                continue
            cos_angles_first = set()
            cos_angles_second = set()
            len_nodes_first = []
            len_nodes_second = []
            len_graph = len(nodes[i])
            for node_index in range(len_graph):
                first_vector_first_graph = Vector(nodes[i][node_index],nodes[i][node_index - 1])
                second_vector_first_graph = Vector(nodes[i][(node_index + 1) % len_graph],nodes[i][node_index])
                cos_angles_first_graph = vector_angle_cos(first_vector_first_graph,second_vector_first_graph)
                cos_angles_first.add(cos_angles_first_graph)
                first_vector_second_graph = Vector(nodes[j][node_index], nodes[j][node_index - 1])
                second_vector_second_graph = Vector(nodes[j][(node_index + 1) % len_graph], nodes[j][node_index])
                cos_angles_second_graph = vector_angle_cos(first_vector_second_graph, second_vector_second_graph)
                cos_angles_second.add(cos_angles_second_graph)

                len_nodes_first.append(first_vector_first_graph.len())
                len_nodes_second.append(first_vector_second_graph.len())


            cos_angles_first = sorted(cos_angles_first)
            cos_angles_second = sorted(cos_angles_first)
            len_nodes_first.sort()
            len_nodes_second.sort()
            relation_coefficients = set(len_first/len_second for len_first,len_second  in zip(len_nodes_first,len_nodes_second))
            if (all(almost_equal(*values) for values in zip(cos_angles_first, cos_angles_second)) and len(relation_coefficients) == 1):
                max_n = len_graph
                first_graph_index = i
                second_graph_index = j
    if (max_n == 0):
        return None
    return first_graph_index,second_graph_index,max_n


def are_polygons_valid(polygons:list):
    for polygon in polygons:
        if (not is_polygon_valid(polygon)):
            return  False
    return True

def is_polygon_valid(polygon:list):
    if (len(polygon) < 3):
        return False

    for i in range(1,len(polygon) - 1):
        first_vector = Vector(polygon[i - 1], polygon[i])
        second_vector = Vector(polygon[i], polygon[i + 1])
        if (almost_equal(first_vector.len(),0.0) or almost_equal(second_vector.len(),0.0)):
            return False
        cos_angle = vector_angle_cos(first_vector,second_vector)
        if (almost_equal(1.0,abs(cos_angle))):
            return False
    return True












class Vector:
    def __init__(self,first_dot,second_dot):
        self.coords = [first_dot[0] - second_dot[0],first_dot[1] - second_dot[1]]
    def len(self):
        return (self.coords[0]**2 + self.coords[1] **2)**0.5


