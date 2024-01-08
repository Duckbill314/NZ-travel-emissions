from pyvis.network import Network
import networkx as nx

# scrubbing to ensure uniqueness of nodes
index_dict = {}

with open('Network_Data.csv', 'r') as network_data:
  lines = network_data.readlines()
  i = 0
  for line in lines[1:]:
    strings = line.strip().split(",")
    if strings[0] not in index_dict:
      index_dict[strings[0]] = i
      i += 1

# generating graph and nodes

g = nx.Graph()

labels = list(index_dict.keys())
ids = list(index_dict.values())

for i in range(len(labels)):
  g.add_node(labels[i], id=ids[i])

# populating a set with the data whilst scrubbing

data_set = set()

with open('Network_Data.csv', 'r') as network_data:
  lines = network_data.readlines()
  for line in lines[1:]:
    strings = line.strip().split(",")
    edge = (strings[0], strings[1], strings[2])
    reverse_edge = (strings[1], strings[0], strings[2])
    weight = float(strings[2])
    if (edge not in data_dict) and (reverse_edge not in data_dict) and (edge != reverse_edge):
      data_set.add(edge)

# generating edges from data set

g.add_weighted_edges_from(list(data_set))

# populating title fields with neighbour data for each node

for node, neighbours in g.adj.items():
  g.nodes[node]['title'] = 'Emissions [kg]'
  g.nodes[node]['size'] = len(neighbours)
  for neighbour, edge_attributes in neighbours.items():
    weight = edge_attributes['weight']
    g.nodes[node]['title'] += '<br>{}: {}'.format(neighbour, weight)

# creating the network

nt = Network('500px', '500px')
nt.from_nx(g)

# showing the network

nt.show('emissions.html')