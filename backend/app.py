from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq

app = Flask(__name__)
CORS(app)

campus_graph = {
    "nodes": [
        {"id": "N1", "name": "Entrance Gate"},
        {"id": "N2", "name": "Parking"},
        {"id": "N3", "name": "Hostel 1 (Himalaya)"},
        {"id": "N4", "name": "Canteen"},
        {"id": "N5", "name": "Hostel 3 (Karakoram)"},
        {"id": "N6", "name": "Hostel 2 (Purvanchal)"},
        {"id": "N7", "name": "FET"},
        {"id": "N8", "name": "Core Block"},
        {"id": "N9", "name": "Aerospace Block"}
    ],
    "edges": [
        {"from": "N1", "to": "N2", "distance": 385},
        {"from": "N1", "to": "N7", "distance": 390},
        {"from": "N1", "to": "N3", "distance": 815},
        {"from": "N1", "to": "N4", "distance": 545},
        {"from": "N1", "to": "N6", "distance": 582},
        {"from": "N1", "to": "N5", "distance": 620},
        {"from": "N1", "to": "N9", "distance": 470},
        {"from": "N1", "to": "N8", "distance": 550},
        {"from": "N2", "to": "N7", "distance": 30},
        {"from": "N2", "to": "N3", "distance": 160},
        {"from": "N2", "to": "N4", "distance": 200},
        {"from": "N2", "to": "N6", "distance": 230},
        {"from": "N2", "to": "N5", "distance": 270},
        {"from": "N7", "to": "N9", "distance": 760},
        {"from": "N7", "to": "N8", "distance": 900},
        {"from": "N9", "to": "N8", "distance": 140},
        {"from": "N7", "to": "N3", "distance": 180},
        {"from": "N7", "to": "N4", "distance": 185},
        {"from": "N5", "to": "N6", "distance": 15},
        {"from": "N6", "to": "N4", "distance": 22},
        {"from": "N4", "to": "N3", "distance": 35}
    ]
}

def neighbors_of(graph, node_id):
    result = []
    for e in graph["edges"]:
        if e["from"] == node_id:
            result.append((e["to"], e["distance"]))
        elif e["to"] == node_id:
            result.append((e["from"], e["distance"]))
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

    path = []
    step = end_id
    while step:
        path.insert(0, step)
        step = previous.get(step)

    return {"path": path, "distance": distances[end_id]}

@app.route("/route", methods=["GET"])
def get_route():
    start = request.args.get("from")
    end = request.args.get("to")

    if not start or not end:
        return jsonify({"error": "Please provide 'from' and 'to' node IDs"}), 400

    valid_ids = {n["id"] for n in campus_graph["nodes"]}
    if start not in valid_ids or end not in valid_ids:
        return jsonify({"error": "Invalid node ID"}), 404

    result = find_route(campus_graph, start, end)
    return jsonify(result)

@app.route("/locations", methods=["GET"])
def get_locations():
    return jsonify(campus_graph["nodes"])
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    