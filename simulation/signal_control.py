import time
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

# Simulated traffic lights at intersections
traffic_lights = {node: "RED" for node in route}

def update_signals(current_index):
    for i, node in enumerate(route):
        if i <= current_index + 2:
            traffic_lights[node] = "GREEN"
        else:
            traffic_lights[node] = "RED"

# Simulation
for i, node in enumerate(route):
    update_signals(i)

    fig, ax = ox.plot_graph(
        G,
        node_size=0,
        edge_color="lightgray",
        bgcolor="white",
        show=False,
        close=False
    )

    ox.plot_graph_route(
        G,
        route[:i+1],
        route_color="green",
        route_linewidth=4,
        node_size=0,
        ax=ax,
        show=False,
        close=False
    )

    plt.title("Autonomous Green Corridor (Simulated)")
    plt.pause(0.5)
    plt.clf()

plt.show()

