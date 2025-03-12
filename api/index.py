from duckduckgo_search import DDGS
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import re
from google.generativeai import genai
app = Flask(__name__)

CORS(app, origins=["https://search-beta-six.vercel.app"])

client = genai.Client(api_key="AIzaSyDwduC5DYRNBlGCwbTofvPfXUHSl3gORZY")



urls = []

scraped = []

def cleaning_data(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces & newlines
    text = re.sub(r'[^a-zA-Z0-9.,!? ]+', '', text)  # Remove special characters
    return text.strip()
    

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
        
            urls.append( result["href"] )

        print(urls)
        first_url = urls[3]
        print("\n\n",first_url)
        response = requests.get(first_url)
        soup = BeautifulSoup(response.text, "lxml")
        content = soup.find(["div" or "p" or "span" ])
        for para in content:
            hello = cleaning_data(para.get_text(strip=True))
            print("".join(hello)) 
            scraped.append(hello);
            print("scraped successfull")
             
        
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents= f"explain in 100 words and any time dont say that the data is scrap bro only give the correct knowledge to user:  {scraped} ")
        
        print("\nWritten via AI: " , response.text)   
        print("Ai successfull") 
        
        # for url in urls:
        #      response = requests.get(url)
        #      soup = BeautifulSoup(response.text, "html.parser")
        #      content = soup.find_all("h1","h2","h3","h4","p")
             

        # print(content);
        return jsonify(Request_List, response.text);





        
if __name__ == '__main__':
    app.run(debug=True);


