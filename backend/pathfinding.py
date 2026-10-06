import heapq

# Sample campus graph — replace with your real map data later
campus_graph = {
    "nodes": [
        {"id": "N1", "name": "Main Gate"},
        {"id": "N2", "name": "Library"},
        {"id": "N3", "name": "Canteen"},
        {"id": "N4", "name": "Block A"},
        {"id": "N5", "name": "Block B"},
    ],
    "edges": [
        {"from": "N1", "to": "N2", "distance": 40},
        {"from": "N1", "to": "N3", "distance": 30},
        {"from": "N2", "to": "N4", "distance": 25},
        {"from": "N3", "to": "N4", "distance": 35},
        {"from": "N4", "to": "N5", "distance": 20},
    ]
}

def neighbors_of(graph, node_id):
    result = []
    for e in graph["edges"]:
        if e["from"] == node_id:
            result.append((e["to"], e["distance"]))
        elif e["to"] == node_id:
            result.append((e["from"], e["distance"]))  # paths are two-way
    return result

def find_route(graph, start_id, end_id):
    distances = {n["id"]: float("inf") for n in graph["nodes"]}
    previous = {}
    distances[start_id] = 0

    queue = [(0, start_id)]
    visited = set()

    while queue:
        current_dist, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)

        if current == end_id:
            break

        for neighbor_id, distance in neighbors_of(graph, current):
            if neighbor_id in visited:
                continue
            new_dist = current_dist + distance
            if new_dist < distances[neighbor_id]:
                distances[neighbor_id] = new_dist
                previous[neighbor_id] = current
                heapq.heappush(queue, (new_dist, neighbor_id))

    # Rebuild path by walking backwards
    path = []
    step = end_id
    while step:
        path.insert(0, step)
        step = previous.get(step)

    # If start node was not reachable or invalid
    if distances[end_id] == float("inf"):
        return {"path": [], "distance": float("inf"), "error": "No path found"}

    return {"path": path, "distance": distances[end_id]}

if __name__ == "__main__":
    # Test it
    result = find_route(campus_graph, "N1", "N5")
    print(result)
    # {'path': ['N1', 'N2', 'N4', 'N5'], 'distance': 85}
