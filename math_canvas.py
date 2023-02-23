EPS = 1e-1



def find_node(node, list_of_nodes):
    for i in range(len(list_of_nodes)):
        if (are_eq_nodes(node,list_of_nodes[i])):
            return i
    return None


def almost_equal(value_1, value_2, accuracy = 10**-2):
    return abs(value_1 - value_2) < accuracy
def are_eq_nodes(first_dot,second_dot):
    if almost_equal(first_dot[0],second_dot[0]) and almost_equal(first_dot[1],second_dot[1]):
        return True
    else:
        return False



def vector_scalar_product(first_vector,second_vector):
    scalar_sum = 0
    for i in range(len(first_vector.coords)):
        scalar_sum += first_vector.coords[i] * second_vector.coords[i]
    return scalar_sum

def vector_angle_cos(first_vector,second_vector):
    return vector_scalar_product(first_vector,second_vector)/(first_vector.len() + second_vector.len())


def find_similar_graphs_with_max_nodes(nodes:list):
    max_n = 0
    first_graph_index = -1
    second_graph_index = -1
    for i in range(len(nodes) - 1):
        for j in range(i,len(nodes)):
            if (len(nodes[i]) != len(nodes[j])):
                continue
            cos_angles_first = set()
            cos_angles_second = set()
            len_graph = len(nodes[i])
            for node_index in range(len_graph):
                vector_first = Vector(nodes[i][node_index],nodes[i][node_index - 1])
                vector_second = Vector(nodes[i][(node_index + 1) % len_graph],nodes[i][(node_index - 1) % len_graph])
                cos_angle = vector_angle_cos(vector_first,vector_second)
                cos_angles_first.add(cos_angle)

            for node_index in range(len_graph):
                vector_first = Vector(nodes[i][node_index], nodes[i][node_index - 1])
                vector_second = Vector(nodes[i][(node_index + 1) % len_graph], nodes[i][(node_index - 1) % len_graph])
                cos_angle = vector_angle_cos(vector_first, vector_second)
                cos_angles_second.add(cos_angle)
            if (all(almost_equal(*values) for values in zip(cos_angles_first, cos_angles_second))):
                max_n = len_graph
                first_graph_index = i
                second_graph_index = j
    if (first_graph_index == -1):
        return None
    return first_graph_index,second_graph_index,max_n




class Vector:
    def __init__(self,first_dot,second_dot):
        self.coords = [first_dot[0] - second_dot[0],first_dot[1] - second_dot[0]]
    def len(self):
        return (self.coords[0]**2 + self.coords[1] **2)**0.5









