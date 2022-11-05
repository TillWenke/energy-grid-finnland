import networkx as nx
import numpy as np
import json

graph = None
with open('../grid_contracted.json') as infile:
    graph = nx.node_link_graph(json.loads(infile.read()))

    print(nx.is_connected(graph))


    # make a digraph
    graph = nx.DiGraph(graph)
    print(graph.number_of_nodes())
    graph.add_node(0,power=0) # source
    graph.add_node(1,power=0) # sink
    print(graph.number_of_nodes())
    # make the source and the sink at index 0 and 1
    for n in graph:
        graph.add_edge(0, n, capacity=graph.nodes[n]['power']) if graph.nodes[n]['power'] > 0 else graph.add_edge(n, 1, capacity=graph.nodes[n]['power'])

    print(graph.nodes[9510316607])
    print(graph.nodes[0]['power'])
    print(graph.nodes[1])
    res = nx.algorithms.flow.dinitz(graph, s=0, t=1, capacity='capacity')
    #flow, cut = nx.minimum_cut(graph, _s=graph.nodes[0], _t=graph.nodes[1])

    flow_value = nx.maximum_flow_value(graph, _s=0, _t=1, capacity='capacity')
    print(flow_value)

    print(res.graph['flow_value'])

    #print(graph.nodes)

    print(graph.edges['capacity'])
