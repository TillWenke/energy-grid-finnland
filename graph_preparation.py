import json

with open('grid.json', 'r') as infile1:
    F = nx.node_link_graph(json.loads(infile1.read()))
D = nx.DiGraph(F)
D.add_node(0,power=0) # source
D.add_node(1,power=0) # sink

for n in D:
    power = D.nodes[n]['power']
    if power > 0:
        # producers
        D.add_edge(0,n,capacity=power)
    if power < 0:
        # consumers
        D.add_edge(n,1,capacity=power)
