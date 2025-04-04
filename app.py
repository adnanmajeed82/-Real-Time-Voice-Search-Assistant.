from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def duckduckgo_search_scrape(query):
    """Perform DuckDuckGo search by scraping the HTML results page."""
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    search_results = []

    # Parse search result items
    for result in soup.find_all('a', class_='result__a', limit=5):
        title = result.get_text()
        link = result['href']
        search_results.append({
            "title": title,
            "link": link
        })

    return search_results

@app.route("/search", methods=["POST"])
def search():
    """Endpoint to handle the search query from the frontend."""
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    # Get DuckDuckGo search results
    search_results = duckduckgo_search_scrape(query)

    return jsonify({"query": query, "results": search_results})

@app.route("/")
def index():
    """Render the main HTML page for voice search."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
