import requests
from bs4 import BeautifulSoup
import markdownify 

class URLConverter:
    def convert(self, url: str, options: dict):
        if not url or not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL provided")

        try:
            response = requests.get(url.strip(), timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                if options['headers']:
                    for header in soup.find_all(['header']):
                        header.decompose()
                if options['footers']:
                    for footer in soup.find_all('footer'):
                        footer.decompose() 
                if options['tables']:
                    for table in soup.find_all('table'):
                        table.decompose() 
                if options['images']:
                    for img in soup.find_all('img'):
                        img.decompose()
                if options['ads']:
                    for ad in soup.find_all('ad'):
                        ad.decompose()
                if options['buttons']:
                    for button in soup.find_all('button'):
                        button.decompose() 

                markdown = markdownify.markdownify(str(soup), heading_style="ATX")
                return markdown
            
            else:
                return f"Error: Received status code {response.status_code}"
            
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
 