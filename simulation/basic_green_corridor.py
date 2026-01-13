import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

ox.settings.log_console = False
ox.settings.use_cache = True

place = "Hyderabad, India"
G = ox.graph_from_place(place, network_type="drive")

nodes = list(G.nodes)
start = nodes[100]
end = nodes[2000]

route = nx.shortest_path(G, start, end, weight="length")

fig, ax = ox.plot_graph_route(
    G,
    route,
    route_color="green",
    route_linewidth=4,
    node_size=0,
    bgcolor="white"
)

plt.show()

