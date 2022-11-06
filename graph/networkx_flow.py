import networkx as nx
import numpy as np
import json

def get_partition(file_path='../grid_contracted_units.json'):
    graph = None
    with open(file_path) as infile:
        graph = nx.node_link_graph(json.loads(infile.read()))
    
        # make a digraph
        graph = nx.DiGraph(graph)
        graph.add_node(0,power=0) # source
        graph.add_node(1,power=0) # sink
        # make the source and the sink at index 0 and 1
        for n in graph:
            if graph.nodes[n]['power'] > 0:
                graph.add_edge(0, n, capacity=3*graph.nodes[n]['power'])
            elif graph.nodes[n]['power'] < 0:
                graph.add_edge(n, 1, capacity=-graph.nodes[n]['power'])
        '''
        prod = 0
        con = 0
        for n in graph:
            if graph.nodes[n]['power'] > 0:
            prod += 3*graph.nodes[n]['power']
            else:
                con += -graph.nodes[n]['power']
        '''
        flow_value, part = nx.minimum_cut(graph, _s=0, _t=1, capacity='capacity', flow_func=nx.algorithms.flow.dinitz)
    
        par = nx.minimum_edge_cut(graph, s=0, t=1, flow_func=nx.algorithms.flow.dinitz)
    
        fixed = []
        for p in par:
            if p[0] != 0 and p[1] != 1:
                fixed.append(p)
    return fixed, flow_value
