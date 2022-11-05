import sys
sys.setrecursionlimit(100000)

def dfs(visited,G_orig,u):
    visited.add(u)

    for neighbor in G_orig.neighbors(u):
        if (neighbor not in visited):
            if (G_orig.nodes[neighbor]['power'] == 0):
                dfs(visited,G_orig,neighbor)
            if (G_orig.nodes[neighbor]['power'] != 0):
                # other node to keep
                #print(start, neighbor)
                cap = G_orig.edges[u,neighbor]['capacity']
                create_new_edge(start,neighbor,cap)
        if (neighbor in visited) and (G_orig.nodes[neighbor]['power'] != 0) and (neighbor != start):
            cap = G_orig.edges[u,neighbor]['capacity']
            update_edge(start,neighbor,cap)
def create_new_edge(u,v,cap):
    G.add_edge(u,v,capacity=cap)

def update_edge(u,v,cap):
    G[u][v]['capacity'] += cap
with open('grid.json', 'r') as infile1:
    G = nx.node_link_graph(json.loads(infile1.read()))
G_orig = nx.Graph(G)

for n in G_orig:
    if G_orig.nodes[n]['power'] != 0:
        visited = set()
        start = n
        dfs(visited,G_orig,n)
kick=[]
for n in G:
    if G.nodes[n]['power'] == 0:
        kick.append(n)

for n in kick:
    G.remove_node(n)
