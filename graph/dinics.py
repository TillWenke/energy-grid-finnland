import numpy as np
import networkx as nx
import json

class Network:
    def __init__(self, C):

        # 1D matrix to hold the supply/demand values of all the nodes
        # demand is negative, supply is positive (per network flow traditiion)
        #
        # This will be filled in with the real nodes and two additional 
        # theoretical nodes at position n-2 (source) and n-1 (sink)
        self.node_demand = np.zeros((len(C)))
        
        self.num_nodes = self.node_demand.shape[0]

        self.levels = np.zeros_like(self.node_demand)

        # we are going to use a dense matrix even though it will probably be sparse
        # this could be improved using COO format or a hash table in the future
        #
        # ideally the edge matrices are a single (n,n,2) matrix with decorator
        # aliases but whatever this is easier to implement
        #
        #
        #
        # 2D matrix to hold the capacities of the edges (and defines connectivity)
        #
        # It is important to add in an edge from all producers to the source 
        # of infinite capacity. Additionally an edge from all consumers to 
        # the sink of infinite capacity.
        self.edge_capacity = np.array(C)
        # matrix to hold the current flows of the edges (also defines connectiviy)
        self.edge_flow = np.zeros_like(self.edge_capacity)

        # Integer value of the flow across the network, if this value is -1
        # that implies that the flow algorithm has not been run on this 
        # network. A value of 0 implies that Dinics has run but no solution 
        # has been found and there is no satisfying flow.
        #
        # Therefore, any changes to the network must also reset this value to
        # -1
        self.flow = -1

    # TODO: function/decorator to return producers (negative node demand)

    # TODO: function/decorator to return consumers (positive node demand)



def depth_first(network, s, sub_flow):
    # terminate if the source and dest are the same, i.e. if both are sink
    if s == network.num_nodes - 1:
        return sub_flow

    dfs_flow = 0

    # check all nodes
    for d in range(network.num_nodes):
        # check if the path out along an edge has capacity and add it
        if network.levels[s] + 1 == network.levels[d] and  \
                network.edge_flow[s][d] < network.edge_capacity[s][d]:

            send_flow = depth_first(network, d, 
                    min(sub_flow, network.edge_capacity[s][d] - network.edge_flow[s][d]))

            network.edge_flow[s][d] += send_flow
            network.edge_flow[d][s] -= send_flow

            dfs_flow += send_flow

    return dfs_flow

def breadth_first(network):
    num_nodes = network.num_nodes

    # get the index of the source and the sinks
    #source = num_nodes - 2
    source = 0
    sink = num_nodes - 1

    # add the source to the queue
    queue = [source]

    # zero out the network levels
    network.levels = np.zeros_like(network.levels)

    network.levels[source] = 1  
    while queue:
        # pop off a new source node
        s = queue.pop()
        # examine all other nodes as destination nodes
        for d in range(num_nodes):
            # check if there is capacity in the link and if it has been visited
            if network.edge_flow[s][d] < network.edge_capacity[s][d] and network.levels[d] == 0:
                # update the destinations level and enqueue it
                network.levels[d] = network.levels[s] + 1
                queue.append(d)

    return network.levels[sink] > 0

def dinics(network):
    # set the flag that we ran the network flow
    network.flow = 0

    # set the flow matrix to be all zeros
    network.edge_flow = np.zeros_like(network.edge_flow)

    # while there is a (non-capacity) path from the source to the sink
    # we continue to increase the flow
    while(breadth_first(network)):
        #network.flow += depth_first(network, network.node_demand.shape[0] - 2, 1E16)
        network.flow += depth_first(network, 0, 1E10)

def find_min_cut(network):
    # create a list of visited nodes
    visited = np.zeros_like(network.levels)

    # create array denoting S and R cuts
    min_cut_dfs(network, 0, visited)

    # do another DFS on all visited nodes to find cross cut edges
    cut_edges = find_cut_edges(network, visited)

    return visited, cut_edges

def min_cut_dfs(network, s, visited):
    # mark the node as visited
    visited[s] = 1

    for d in range(network.num_nodes):
        # traverse only the edges that are unsaturated
        if network.edge_flow[s][d] < network.edge_capacity[s][d] and visited[d] == 0:
            min_cut_dfs(network, d, visited)

def find_cut_edges(network, visited):
    cross_cut_edges = np.zeros_like(network.edge_capacity)
    for s in range(network.num_nodes):
        if visited[s] == 1:
            for d in range(network.num_nodes):
                if visited[d] == 0:
                    cross_cut_edges[s][d] = network.edge_flow[s][d]
    return cross_cut_edges

def to_dense(json_filename='../grid_contracted.json'):
    # make the graph bi-directional and make it dense
    with open(json_filename, 'r') as infile:
        graph = nx.node_link_graph(json.loads(infile.read()))
        graph = nx.DiGraph(graph)
        graph.add_node(0,power=0) # source
        graph.add_node(1,power=0) # sink

        for n in graph:
            graph.add_edge(0, n, capacity=graph.nodes[n]['power']) if graph.nodes[n]['power'] > 0 else graph.add_edge(n, 1, capacity=graph.nodes[n]['power'])

        # replace all nan's with 0's (ex line #269)


        print(graph.adj[0])
        graph = nx.to_numpy_matrix(graph, weight="capacity", nonedge=0.0)
    return graph
