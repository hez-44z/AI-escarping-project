from flask import Blueprint, request, jsonify
from utils.scraper import scrape_all_platforms


search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400


    try:
        # Call the unified scraper
        results = scrape_all_platforms(query)
        return jsonify({"query": query, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

