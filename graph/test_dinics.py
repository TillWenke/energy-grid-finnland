from dinics import Network, dinics, find_min_cut 
C = [[ 0, 3, 3, 0, 0, 0 ],  # s
     [ 0, 0, 2, 3, 0, 0 ],  # o
     [ 0, 0, 0, 0, 2, 0 ],  # p
     [ 0, 0, 0, 0, 4, 2 ],  # q
     [ 0, 0, 0, 0, 0, 2 ],  # r
     [ 0, 0, 0, 0, 0, 3 ]]  # t
'''
C = [[ 0, 2, 3, 0, 0, 0 ],  # o
     [ 0, 0, 0, 2, 0, 0 ],  # p
     [ 0, 0, 0, 4, 0, 2 ],  # q
     [ 0, 0, 0, 0, 0, 2 ],  # r
     [ 3, 3, 0, 0, 0, 0 ],  # s
     [ 0, 0, 0, 0, 0, 3 ]]  # t
'''
net = Network(C)
dinics(net)
print(net.flow)

visited, cut_edges = find_min_cut(net)
print(visited)
print(cut_edges)

#     0   1   2   3   4   5
C = [[0, 16, 23,  0,  0,  0], # 0
     [0,  0, 10, 12,  0,  0], # 1
     [0,  4,  0,  0, 14,  0], # 2
     [0,  0,  9,  0,  0, 20], # 3
     [0,  0,  0,  7,  0,  4], # 4
     [0,  0,  0,  0,  0,  0]] # 5

net = Network(C)
dinics(net)
print(net.flow)

visited, cut_edges = find_min_cut(net)
print(visited)
print(cut_edges)

#     0   1   2   3   4   5
C = [[0,  3,  7,  0, 10,  0], # 0
     [0,  0,  0,  9,  9,  0], # 1
     [0,  9,  0,  0,  9,  4], # 2
     [0,  0,  0,  0,  0,  3], # 3
     [0,  0,  0,  0,  0,  7], # 4
     [0,  0,  0,  0,  0,  0]] # 5

net = Network(C)
dinics(net)
print(net.flow)

visited, cut_edges = find_min_cut(net)
print(visited)
print(cut_edges)

#     0   1   2   3   4   5
C = [[0, 10, 10,  0,  0,  0], # 0
     [0,  2,  0,  4,  8,  0], # 1
     [0,  0,  0,  0,  9,  0], # 2
     [0,  0,  0,  0,  0, 10], # 3
     [0,  0,  0,  6,  0, 10], # 4
     [0,  0,  0,  0,  0,  0]] # 5

net = Network(C)
dinics(net)
print(net.flow)

visited, cut_edges = find_min_cut(net)
print(visited)
print(cut_edges)

import networkx as nx
import numpy as np

graph = nx.from_numpy_matrix(np.array(C))




'''
G = nx.DiGraph()
G.add_edge("x", "a", capacity=3.0)
G.add_edge("x", "b", capacity=1.0)
G.add_edge("a", "c", capacity=3.0)
G.add_edge("b", "c", capacity=5.0)
G.add_edge("b", "d", capacity=4.0)
G.add_edge("d", "e", capacity=2.0)
G.add_edge("c", "y", capacity=2.0)
G.add_edge("e", "y", capacity=3.0)

G = nx.to_numpy_matrix(G, weight='capacity')
print(G)

G = nx.from_numpy_matrix(G)

print(G.adj[0])
print(G.nodes)

res = nx.algorithms.flow.dinitz(G, s=0, t=6, capacity='weight')

print('flow', res.graph['flow_value'])

print(graph.adj[0])

print(graph.edges.data())

exit

'''
res = nx.algorithms.flow.dinitz(graph, s=0, t=5, capacity='weight')
#flow, cut = nx.minimum_cut(graph, _s=graph.nodes[0], _t=graph.nodes[1])

flow_value = nx.maximum_flow_value(graph, 0, 5, capacity='weight')
print(flow_value)

print(res.graph['flow_value'])

