import requests
import json
from datetime import datetime
import click
import os 

class PokemonAPI:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"

    
    def fetch_pokemon_data(self, pokemon_id=None):
        pokemon_data = []

        if pokemon_id is not None:
            url = f"{self.base_url}{pokemon_id}/"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_data.append(self.extract_pokemon_data(data))
            else:
                click.echo(f"Error: Unable to fetch data for Pokemon with ID {pokemon_id}. Status code: {response.status_code}")
        else:
            ## Default it fetches 20 records.
            ## Howerver there are 1 million pokemons that are only fetched by changing the limit
            ## The response rate is slow so lets fetch only 50 pokemons to demonstrate
            url = f"{self.base_url}?limit=50"    
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for pokemon in data['results']:
                    pokemon_url = pokemon['url']
                    response = requests.get(pokemon_url)
                    if response.status_code == 200:
                        pokemon_data.append(self.extract_pokemon_data(response.json()))
                    else:
                        click.echo(f"Error: Unable to fetch data for {pokemon['name']}. Status code: {response.status_code}")
            else:
                click.echo(f"Error: Unable to fetch the list of Pokemon. Status code: {response.status_code}")

        click.echo(f"Info: fetch {len(pokemon_data)} records from the API.")
        return pokemon_data

    
    def extract_pokemon_data(self,data):
        return {
            'id': data['id'],
            'name': data['name'],
            'types': [t['type']['name'] for t in data['types']],
            'height': data['height'],
            'weight': data['weight'],
            'base_experience': data['base_experience'],
            'abilities': [ability['ability']['name'] for ability in data['abilities']]
        }

    def save_pokemon_data_to_json(self,data,dir=None):
        timestamp = datetime.now()
        filename = f"pokemon_data_{timestamp}.json"
        
        if dir: 
            dir_with_partition = os.path.join(
                dir,
                timestamp.strftime('%Y'),
                timestamp.strftime("%m"),
                timestamp.strftime("%d")
        )
            if not os.path.exists(dir_with_partition):
                os.makedirs(dir_with_partition)

            file_path = os.path.join(dir_with_partition, filename)    
        else:
            file_path = filename
            click.echo("Info: saving in project root directory")
        
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        click.echo(f'Info: File successfully saved at {file_path}')

def api_init():
    return PokemonAPI()
