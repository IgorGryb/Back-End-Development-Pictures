"""Pictures microservice - Flask REST API (IBM Back-End Development Capstone, Exercise 1-6)."""
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory store (seed data)
pictures = {}
_next_id = 1


def _seed():
    global _next_id
    seeds = [
        {"title": "Sunset over the lake", "url": "https://example.com/pics/sunset.jpg"},
        {"title": "City skyline at night", "url": "https://example.com/pics/city.jpg"},
    ]
    for s in seeds:
        pictures[_next_id] = {"id": _next_id, **s}
        _next_id += 1


_seed()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200


@app.route("/pictures", methods=["GET"])
def list_pictures():
    return jsonify(list(pictures.values())), 200


@app.route("/pictures/count", methods=["GET"])
def count_pictures():
    return jsonify({"count": len(pictures)}), 200


@app.route("/pictures/<int:picture_id>", methods=["GET"])
def get_picture(picture_id):
    pic = pictures.get(picture_id)
    if pic is None:
        abort(404)
    return jsonify(pic), 200


@app.route("/pictures", methods=["POST"])
def create_picture():
    global _next_id
    data = request.get_json(force=True, silent=True) or {}
    if "title" not in data or "url" not in data:
        return jsonify({"error": "title and url are required"}), 400
    pic = {"id": _next_id, "title": data["title"], "url": data["url"]}
    pictures[_next_id] = pic
    _next_id += 1
    return jsonify(pic), 201


@app.route("/pictures/<int:picture_id>", methods=["PUT"])
def update_picture(picture_id):
    pic = pictures.get(picture_id)
    if pic is None:
        abort(404)
    data = request.get_json(force=True, silent=True) or {}
    pic.update({k: v for k, v in data.items() if k in ("title", "url")})
    return jsonify(pic), 200


@app.route("/pictures/<int:picture_id>", methods=["DELETE"])
def delete_picture(picture_id):
    if picture_id not in pictures:
        abort(404)
    del pictures[picture_id]
    return jsonify({"deleted": picture_id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
