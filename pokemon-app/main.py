from flask import Flask, render_template_string
import requests

app = Flask(__name__)

html_file = open("public/index.html")
template = html_file.read()

@app.route("/")
def index():
    url = "https://pokeapi.co/api/v2/pokemon?limit=20"
    response = requests.get(url).json()

    pokemons = []
    for result in response["results"]:
        poke_data = requests.get(result["url"]).json()
        pokemons.append({
            "id": poke_data["id"],
            "name": poke_data["name"],
            "sprite": poke_data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in poke_data["types"]]
        })

    return render_template_string(template, pokemons=pokemons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
