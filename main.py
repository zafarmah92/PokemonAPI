from API_interaction.API import api_init
from IO.postgres_db import db_init
import click

@click.command()
@click.option('--id', default=None, help='Pokemon ID to fetch data for a specific Pokemon.')
@click.option('--save_dir', default=None , help='Directory path to save. Defeault will be saved in project root path')
@click.option('--db', is_flag=True, default=False, help='DB integration as boolean command.')
def get_id(id,save_dir,db):
    api = api_init()
    #while True:
        #api = api_init()
        #user_input = input("Enter a command ")
    #click.echo(f"You entered: {user_input}")
    data = api.fetch_pokemon_data(pokemon_id=id)
    api.save_pokemon_data_to_json(data, dir=save_dir)
    #print(api.fetch_pokemon_data(pokemon_id=1))
    if db:
        postgres_init = db_init() 
        postgres_init.ingest_data(data)
        postgres_init.close()
    
        #print(data)


if __name__ == '__main__':
    #api = PokemonAPI()
    get_id()

