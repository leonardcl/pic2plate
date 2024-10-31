import requests
from bs4 import BeautifulSoup
import json

class RecipeScraper:
    def __init__(self, query):
        self.query = query
        self.recipes = []  # To store basic recipe info (title and link)
        self.all_recipes_details = []  # To store detailed recipe info
    
    def search_recipes(self):
        """Search for recipes on Cookpad using the provided query."""
        url = f'https://cookpad.com/us/search/{self.query.replace(" ", "%20")}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to retrieve data. Status code:", response.status_code)
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for recipe in soup.select('a.block-link__main'):
            if recipe:
                title = recipe.text.strip()
                link = 'https://cookpad.com' + recipe['href']
                self.recipes.append({'title': title, 'link': link})
        
        print(f"Found {len(self.recipes)} recipes for query '{self.query}'.")

    def get_recipe_details(self, url):
        """Fetch detailed recipe information from a given recipe link."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve recipe details. Status code: {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract introduction
        intro_elem = soup.select_one('.text-cookpad-14')  # Adjust based on actual page structure
        introduction = intro_elem.text.strip() if intro_elem else "No introduction available"
        
        # Extract ingredients
        ingredients = [ingredient.text.strip() for ingredient in soup.select('.ingredient-list')]
        
        # Extract instructions (steps to cook)
        instructions = [step.text.strip() for step in soup.select('.step')]
        
        return {
            'introduction': introduction,
            'ingredients': ingredients,
            'instructions': instructions
        }

    def fetch_all_recipe_details(self):
        """Loop through all recipes found and fetch detailed information."""
        for idx, recipe in enumerate(self.recipes):
            print(f"Fetching details for {idx+1}: {recipe['title']}")
            details = self.get_recipe_details(recipe['link'])
            
            if details:
                recipe_data = {
                    "title": recipe['title'],
                    "introduction": details['introduction'],
                    "ingredients": details['ingredients'],
                    "instructions": details['instructions']
                }
                self.all_recipes_details.append(recipe_data)
    
    def save_all_recipes_to_json(self, filename="all_recipes.json"):
        """Save all recipes with details to a single JSON file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.all_recipes_details, file, indent=4, ensure_ascii=False)
        
        print(f"All recipes saved to {filename}")

# Example usage
if __name__ == "__main__":
    query = "japanese onion pork"
    scraper = RecipeScraper(query)
    
    scraper.search_recipes()
    scraper.fetch_all_recipe_details()
    scraper.save_all_recipes_to_json()
