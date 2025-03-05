from duckduckgo_search import DDGS
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS


 
app = Flask(__name__)

CORS(app, origins=["https://search-beta-six.vercel.app"])

@app.route("/", methods=['GET'])
def home():
    """Returns a welcome message as JSON."""
    return jsonify({"message": "Hello, welcome on homepage"})


@app.route("/search", methods=['GET'])

def search():
        # Initialize DDGS
        query = request.args.get('q')
        with DDGS() as ddgs:
        # Perform a text search
            results = ddgs.text(query, region="wt-wt", safesearch="moderate", timelimit="y")

            Request_List = []
    # Print results
        for result in results:
            # print(f"Title: {result['title']}")
            # print(f"URL: {result['href']}")
            # print(f"Snippet: {result['body']}")
            # print("-" * 1)
            Request_List.append({"title": result['title'], "url": result['href'], "snippet": result['body']})

        return jsonify(Request_List);



        
if __name__ == '__main__':
    app.run(debug=True);


