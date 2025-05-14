from duckduckgo_search import DDGS
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import re
from google import genai

app = Flask(__name__)


CORS(app, origins=["https://www.fondpeace.com"])

# client = genai.Client(api_key="AIzaSyDwduC5DYRNBlGCwbTofvPfXUHSl3gORZY")




    

@app.route("/search", methods=['GET'])



def search():
        # # Initialize DDGS
        # query = request.args.get('q')
        # # print("This is query dear : ", query)

        # # QueryQuestions = client.models.generate_content(
        # #      model= 'gemini-2.0-flash',
        # #      contents=f"Generate exactly 10 short questions about {query} in JSON format. "
        # #      "Output example: {{'questions': ['What is X?', 'How does X work?', ...]}}"
        # # )
           
             

    
        # # print("Search Queryies: ", QueryQuestions.text);



        # with DDGS() as ddgs:
        # # Perform a text search
        #     results = ddgs.text(query, region="wt-wt", safesearch="moderate", timelimit="y")

    
           
    # Print results

    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
    }

    Request_List = []
    urls = []
    scraped = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, region="wt-wt", safesearch="moderate", timelimit="y")

            for result in results:
                Request_List.append({
                    "title": result['title'],
                    "url": result['href'],
                    "snippet": result['body']
                })
                urls.append(result["href"])
                time.sleep(1)

        urls = list(set(urls))  # Remove duplicate URLs

        for i, url in enumerate(urls[:8]):  # Limit scraping to first 8 results
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"Failed to fetch {url} with status code: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, "lxml")
                for tag in soup(["script", "style"]):
                    tag.decompose()

                content_blocks = soup.find_all(["p", "main", "div", "article", "section", "h1", "title", "table"])
                for block in content_blocks:
                    text = block.get_text(separator=" ").strip()
                    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text)
                    cleaned = re.sub(r"\s+", " ", cleaned)
                    if cleaned:
                        scraped.append(cleaned)

                scraped.append(f"URL: {url}")

            except Exception as e:
                print(f"Error scraping {url}: {e}")
            time.sleep(1.5)  # Delay to avoid being blocked

        pure_scraped = list(set(scraped))

        return jsonify({
            "query": query,
            "search_results": Request_List,
            "scraped_data": pure_scraped[:100]  # Limit output size
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#         for result in results:
#             # print(f"Title: {result['title']}")
#             # print(f"URL: {result['href']}")
#             # print(f"Snippet: {result['body']}")
#             # print("-" * 1)
#             Request_List.append({"title": result['title'], "url": result['href'], "snippet": result['body']})
#             time.sleep(2)
#             urls.append( result["href"] )

#         urls = list(set(urls))
#         # print(urls)

#         # first_url = urls[6]
#         # print("\n\n",first_url)

        
# #         headers = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
# #     "Accept-Language": "en-US,en;q=0.5",
# #     "Accept-Encoding": "gzip, deflate, br",
# #     "Connection": "keep-alive",
# #     "Referer": "https://www.google.com/",
# # }

#         headers = {
#                 "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
#             }


#         for i,url in enumerate(urls[:8]):
        

            
#             response = requests.get(url,headers=headers, verify=True )
#             # print(url);
#             soup = BeautifulSoup(response.text, "lxml")
#             for script in soup(["script", "style"]):
#                 script.extract()
            

#             content = soup.find_all(["p", "main", "div", "article", "section", "h1", "title","table"]) 
            
            

#             for para in content:
#                 hello = (para.get_text(separator=" ").strip())
#                 cleaning_data = re.sub(r"[^a-zA-Z0-9\s]", "", hello) # Keep Only Letters and Numbers
#                 cleaning_data = re.sub(r"\s+", " ", cleaning_data).strip() # Removed Extra Spaces

#                 # print("".join(cleaning_data)) 
#                 scraped.append(cleaning_data);
#             # print("Scraped Data Successfull")
#             # print(url, "\t\t", i)
#             scraped.append(url)
#             pure_scraped = list(set(scraped))
#             # print("\n\n\n Pure Scraped Data: ", pure_scraped)

            


            try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        images = []

        # ✅ 1. og:image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            images.append(urljoin(url, og_image["content"]))

        # ✅ 2. twitter:image
        twitter_image = soup.find("meta", property="twitter:image")
        if twitter_image and twitter_image.get("content"):
            images.append(urljoin(url, twitter_image["content"]))

        # ✅ 3. link rel="image_src"
        image_src = soup.find("link", rel="image_src")
        if image_src and image_src.get("href"):
            images.append(urljoin(url, image_src["href"]))

        # ✅ 4. All <img> tags
        img_tags = soup.find_all("img")
        for img in img_tags:
            img_src = img.get("src")
            if img_src:
                images.append(urljoin(url, img_src))

        # ✅ Remove duplicates
        images = list(set(images))
        return images

    except Exception as e:
        print(f"Error scraping images from {url}: {e}")
        return []
        
                
            
        
     # #    print(scraped)

     #    for url in urls:
     #                response = requests.get(url)
     #                soup = BeautifulSoup(response.text, "html.parser")
     #                content = soup.find_all("h1","h2","h3","h4","p")
                    

     #    print(content);
        


      #   if  'create image' in query.lower() or 'generate image' in query.lower():
      #        response = client.models.generate_content(
      #             model="gemini-2.0-flash",
      #            contents=f"Generate a high-quality image based on this prompt: {query}. "
      #                "Ensure it is detailed, visually appealing, and matches the description accurately."
      #        )
             
      #        # print("Image URL: ", response.text);
      #     #    jsonify("Image URL: ", response.text)
        
      # #   elif "code" in query.lower() or "create code for" in query.lower() or "generate code" in query.lower():
             
      # #        response = client.models.generate_content(
      # #        model="gemini-2.0-flash",
      # #        contents=f"Write a well-commented, optimized code snippet for: {query}. "
      # #                "Ensure the code is efficient, uses best practices, and is properly structured. "
      # #                "Use proper indentation, function-based approach, and security best practices."
      # # ) 
      # #        # print("Code Genrated: ",response.text)
      # #     #    jsonify("Code Genrated: ", response.text)
        
        
      # #   elif "resume" in query.lower():
      # #       response = client.models.generate_content(
      # #            model="gemini-2.0-flash",
      # #            contents=f"Create a modern, well-structured resume tailored for {query}. "
      # #                "Include an engaging summary, skills, experience, education, and achievements. "
      # #                "Ensure ATS (Applicant Tracking System) optimization with professional formatting."
       
      # #       )
      # #       # print("Resume: ", response.text)
      # #     #   jsonify("Resume: ", response.text);
        
      #   # elif "define" in query.lower() or "explain" in query.lower() or "latest" in query.lower():
      #   #      response = client.models.generate_content(
      #   #           model='gemini-2.0-flash',
      #   #           contents=f"Provide a clear, well-explained, and factually correct answer for: {query}. "
      #   #              "Include structured paragraphs, headings, bullet points, and references to latest updates. "
      #   #              "If the topic requires up-to-date information, fetch the latest web results."
       
      #   #      )
      #   #      # print("Explaination: ", response.text)
      #   #   #    print("Explaination: ", response.text)
        
      #   else:
             
      #       try:
      #           response = client.models.generate_content(
      #           model="gemini-2.0-flash",
      #           contents=f"""
      #           Provide a **concise and well-structured** answer for: "{query}" (max 200 words).  
      #           Use **Gemini AI** if available; otherwise, summarize the latest **{scraped}** data.  
            
      #           Include:  
      #           - **Headings & bullet points** for clarity.  
      #           - **Bold text** for key points.  
      #           - **Avoid any source links in the main content.**  
      #           - Mention **all sources** only under the "Sources" section.  
            
      #           Format for sources:  
            
      #           <b>Sources:</b> 
      #           <ul style="list-style-type: disc; padding-left: 20px;">
      #             <li><b><a href="{{url1}}" target="_blank" style="color: blue; text-decoration: none;">{{domain1}}</a></b></li>
      #             <li><b><a href="{{url2}}" target="_blank" style="color: blue; text-decoration: none;">{{domain2}}</a></b></li>
      #             <li><b><a href="{{url3}}" target="_blank" style="color: blue; text-decoration: none;">{{domain3}}</a></b></li>
      #           </ul>
      #           """
      #       )

      #       except Exception as e:
      #           response = None
            





             
             # print("Scraped Data AI Written Update: ", response.text);
          #    print("Scrap Data AI: ", response.text);
        
        # print(urls)  

        
        
        return jsonify(Request_List, images);

        
if __name__ == '__main__':
    app.run(debug=True);




