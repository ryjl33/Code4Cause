from flask import Flask, request
from guidance import models, gen, system, user, assistant

from scrape_information import scrape_information
from flask_cors import CORS
import orjson

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

lm = models.OpenAI('gpt-4o-mini', echo=False)
with system():
    lm += "You are a helpful assistant. You will answer the user's questions."
with user():
    lm += 'From the following prompt, summarize information about the ballot politition:'

@app.route('/')
def index():
    return 'hi'
    global lm
    with user():
        lm += 'Access the web to give me a summary about' + 'Mike DeWine' + "'s ballot information."
    with assistant():
        lm += gen(name='resp', temperature=0.3, max_tokens=500)

    resp = lm['resp']
    print(f'Assistant response: {resp}')

    return resp

def get_list_names(c):
    # This function should return a list of names to be used in the conversation.
    # For demonstration purposes, we'll return a static list.
    return ['Donna M.C. Baringer', 'Mike DeWine', 'Joe Biden', 'Donald Trump']

@app.route('/ask/<string:city_location>', methods=['GET'])
def ask(city_location):
    global lm

    print(f'Location: {city_location}')

    names = get_list_names(city_location)
    resps = []

    for name in names:
        person_info = scrape_information(name)
        with user():
            lm += f'Using the following information, summarize the ballot information about {name}:\n{person_info}'

        with assistant():
            lm += gen(name='resp', temperature=0.3, max_tokens=500)
        
        resps.append(lm['resp'])

    return orjson.dumps(resps).decode()
