import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# -----------------------------
# 1️⃣ Setup OSM network
# -----------------------------
ox.settings.log_console = False
ox.settings.use_cache = True

place = "Hyderabad, India"
G = ox.graph_from_place(place, network_type="drive")

nodes = list(G.nodes)
start = nodes[100]
end = nodes[2000]

# -----------------------------
# 2️⃣ Add congestion to edges
# -----------------------------
for u, v, k, data in G.edges(keys=True, data=True):
    data["congestion"] = random.uniform(0.2, 1.0)
    base_speed = data.get("speed_kph", 40)  # default 40 km/h
    data["effective_speed"] = max(base_speed * (1 - 0.7 * data["congestion"]), 5)
    # travel time in seconds
    data["travel_time"] = data["length"] / data["effective_speed"] * 3600

# -----------------------------
# 3️⃣ Compute normal route (distance only)
# -----------------------------
normal_route = nx.shortest_path(G, start, end, weight="length")

# Normal travel time
normal_time = 0
for i in range(len(normal_route) - 1):
    u, v = normal_route[i], normal_route[i + 1]
    edge_data = list(G.get_edge_data(u, v).values())[0]
    normal_time += edge_data["travel_time"]

# -----------------------------
# 4️⃣ Compute emergency route (congestion-aware)
# -----------------------------
emergency_route = nx.shortest_path(G, start, end, weight="travel_time")

# -----------------------------
# 5️⃣ Setup simulated traffic lights
# -----------------------------
traffic_lights = {node: "RED" for node in emergency_route}

def update_signals(current_index, lookahead=2):
    for i, node in enumerate(emergency_route):
        if i <= current_index + lookahead:
            traffic_lights[node] = "GREEN"
        else:
            traffic_lights[node] = "RED"

# -----------------------------
# 6️⃣ Animate emergency vehicle
# -----------------------------
emergency_time = 0
plt.ion()  # interactive mode
fig, ax = plt.subplots(figsize=(8,8))

for i in range(len(emergency_route)-1):
    u, v = emergency_route[i], emergency_route[i+1]
    edge_data = list(G.get_edge_data(u, v).values())[0]
    speed = edge_data["effective_speed"]
    travel_time = edge_data["travel_time"]

    emergency_time += travel_time

    update_signals(i)

    ax.clear()
    ox.plot_graph(
        G,
        node_size=0,
        edge_color="lightgray",
        bgcolor="white",
        show=False,
        close=False,
        ax=ax
    )

    # Highlight the emergency vehicle route so far
    ox.plot_graph_route(
        G,
        emergency_route[:i+1],
        route_color="green",
        route_linewidth=4,
        node_size=0,
        ax=ax,
        show=False,
        close=False
    )

    # Show traffic light status at next node
    current_node = emergency_route[i]
    status = traffic_lights[current_node]
    plt.title(f"Emergency Green Corridor | Node {i+1}/{len(emergency_route)} | Light: {status} | Speed: {int(speed)} km/h")
    plt.pause(0.05)

plt.ioff()
plt.show()

# -----------------------------
# 7️⃣ Results
# -----------------------------
print("✅ Simulation Complete")
print(f"Normal travel time: {normal_time:.2f} s")
print(f"Emergency travel time: {emergency_time:.2f} s")
print(f"Time saved with green corridor: {normal_time - emergency_time:.2f} s")

