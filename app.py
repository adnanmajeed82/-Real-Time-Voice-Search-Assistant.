from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def google_search_scrape(query):
    """Perform Google search by scraping the search results page."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    search_results = []

    # Parse search result items
    for item in soup.select('div.g'):
        title = item.select_one('h3')
        link = item.select_one('a')['href']
        if title and link:
            search_results.append({
                "title": title.text,
                "link": link
            })

    return search_results[:5]  # Return top 5 results

@app.route("/search", methods=["POST"])
def search():
    """Endpoint to handle the search query from the frontend."""
    data = request.get_json()
    query = data.get("query")
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    # Get Google search links by scraping
    search_results = google_search_scrape(query)
    
    return jsonify({"query": query, "results": search_results})

@app.route("/")
def index():
    """Render the main HTML page for voice search."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
