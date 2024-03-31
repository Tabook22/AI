import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

class ScraperTool():
  @tool("Scraper Tool")
  def scrape(url: str):
    "Useful tool to scrap a website content, use to learn more about a given url."

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        ## here we are going to extract the article based upon its "class name", but if there is many classes we need to ietrate and show each one of them
        #articles = soup.find_all(class_='gc__content')
        # Iterate over all found elements and concatenate their text
        #for article in articles:
         # text += article.get_text(separator=' ', strip=True) + "\n\n"

        #here am using https://www.aljazeera.com/tag/science-and-technology/
        article=soup.find(class_='gc__content') # here we are going to extract the article based upon its "class name", but if there is many classes with this name it will grap the first one only
        #article = soup.find(id='content') #this is the div id in the website where i want to extract the text, you can change to whatever id in the website you are trying to scrap text
        
        if article:
            # Extract and print the text from the article
            text = (article.get_text(separator=' ', strip=True))
        else:
            print("Article with specified ID not found.")
        
        return text
    else:
        print("Failed to retrieve the webpage")
    