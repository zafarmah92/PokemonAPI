import psycopg2
from psycopg2 import sql
import click

class PokemonDB:
    def __init__(self, dbname, user, password, host="host.docker.internal", port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()
        self.create_schema()
        self.create_table()

    def create_schema(self):
        create_schema_sql = """
        CREATE SCHEMA IF NOT EXISTS pokeapi;
        """
        self.cur.execute(create_schema_sql)
        self.conn.commit()
        #click.echo("Info: Create schema pokeapi.")



    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS pokeapi.pokemondata (
            id SERIAL PRIMARY KEY,
            pokemon_id integer,
            name VARCHAR(255),
            types TEXT[],
            height DECIMAL,
            weight DECIMAL,
            base_experience INTEGER,
            abilities TEXT[]
        );
        """
        self.cur.execute(create_table_sql)
        self.conn.commit()
        #click.echo("Info: Create schema pokemonData.")


    def ingest_data(self, data):
        insert_data_sql = """
        INSERT INTO pokeapi.pokemondata (pokemon_id, name, types, height, weight, base_experience, abilities)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        for index, record in enumerate(data):
            self.cur.execute(
                insert_data_sql,
                (
                    record['id'],
                    record['name'],
                    record['types'],
                    record['height'],
                    record['weight'],
                    record['base_experience'],
                    record['abilities']
                )
            )
        self.conn.commit()
        click.echo(f"Info: Ingested {len(data)} records.")

    def close(self):
        self.cur.close()
        self.conn.close()


def db_init():
    ## Here these credential fetching can be imporved
    ## user name and passwords can be pulled from AWS parameter store
    db = PokemonDB(dbname='postgres', user='postgres', password='secret')
    return db 

