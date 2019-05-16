
import pprint
import os
import json

printer = pprint.PrettyPrinter(indent=4, width=120)
failedPokemon = {}

files = os.listdir("pokemonListings/")

for file in files:
    f = open("pokemonListings/" + file, 'r')
    data = json.loads(f.read())
    f.close()

    f = open("pokemonListings/" + file, 'w')
    pprint.pprint(data, stream=f, indent=4, width=120)
    f.close()
