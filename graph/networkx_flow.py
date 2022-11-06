import networkx as nx
import numpy as np
import json

graph = None
with open('../grid_contracted_nonan.json') as infile:
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
        if graph.nodes[n]['power'] > 0:
            graph.add_edge(0, n, capacity=3*graph.nodes[n]['power'])
        elif graph.nodes[n]['power'] < 0:
            graph.add_edge(n, 1, capacity=-graph.nodes[n]['power'])


    prod = 0
    con = 0
    for n in graph:
        if graph.nodes[n]['power'] > 0:
            prod += 3*graph.nodes[n]['power']
        else:
            con += -graph.nodes[n]['power']

    print('power balance', prod, con)

    print(nx.get_edge_attributes(graph, 'capacity'))

    #flow_value, part = nx.maximum_flow_value(graph, _s=0, _t=1, capacity='capacity', flow_func=nx.algorithms.flow.dinitz)
    flow_value, part = nx.minimum_cut(graph, _s=0, _t=1, capacity='capacity', flow_func=nx.algorithms.flow.dinitz)
    print(flow_value)

    print(part)
