import numpy as np

class Network:
    def __init__(self, C):

        # 1D matrix to hold the supply/demand values of all the nodes
        # demand is negative, supply is positive (per network flow traditiion)
        #
        # This will be filled in with the real nodes and two additional 
        # theoretical nodes at position n-2 (source) and n-1 (sink)
        self.node_demand = np.zeros((len(C)))
        
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
    if s == network.node_demand.shape[0] - 1:
        return sub_flow

    dfs_flow = 0

    # check all nodes
    for d in range(network.node_demand.shape[0]):
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
    num_nodes = network.node_demand.shape[0]

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