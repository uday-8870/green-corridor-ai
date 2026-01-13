import time
import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

ox.settings.log_console = False
ox.settings.use_cache = True

place = "Hyderabad, India"
G = ox.graph_from_place(place, network_type="drive")

for u, v, k, data in G.edges(keys=True, data=True):
    data["congestion"] = random.uniform(0.2, 1.0)
    base_speed = data.get("speed_kph", 40)
    data["effective_speed"] = base_speed * (1 - 0.7 * data["congestion"])

nodes = list(G.nodes)
start = nodes[100]
end = nodes[2000]
route = nx.shortest_path(G, start, end, weight="length")

for i in range(len(route) - 1):
    u = route[i]
    v = route[i + 1]

    edge_data = list(G.get_edge_data(u, v).values())[0]
    speed = max(edge_data["effective_speed"], 5)

    delay = 1 / speed  

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

    plt.title(f"Congestion-aware Green Corridor | Speed: {int(speed)} km/h")
    plt.pause(delay)
    plt.clf()

plt.show()

