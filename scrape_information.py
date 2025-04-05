from bs4 import BeautifulSoup, Comment
import requests


def scrape_information(name: str):
    url = 'https://www.bing.com/search?q=' + name.lower().replace(' ', '+')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        body = soup.find('body')

        for a in ('script', 'style', 'link', 'img', 'svg', 'canvas', 'video', 'audio',  'iframe', 'object', 'embed', 'form', 'span'):
            for tag in body.find_all(a):
                tag.decompose()
        
        for tag in body.find_all(string=lambda text: isinstance(text, Comment)):
            tag.decompose()


        information = [r.getText() for r in body.find_all('p')]
        return '\n'.join(information)
    else:
        print(f"Failed to retrieve information for {name}. Status code: {response.status_code}")
        return ''
